import torch
import shutil
import random
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torchaudio
import librosa
import numpy as np
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import ReduceLROnPlateau
from pathlib import Path
from sklearn.model_selection import train_test_split


def analyze_audio_lengths(data_dir):
    """Analyze the length of audio files to determine optimal padding."""
    import librosa
    import numpy as np

    durations = []
    n_frames = []

    for split in ['train', 'val']:
        for label in ['positive', 'negative']:
            path = Path(data_dir) / split / label
            for audio_file in path.glob('*.wav'):
                y, sr = librosa.load(str(audio_file), sr=16000)
                duration = len(y) / sr
                durations.append(duration)

                # Calculate number of frames in mel spectrogram
                # Using n_fft=2048, hop_length=512
                n_frame = 1 + (len(y) - 2048) // 512
                n_frames.append(n_frame)

    return max(n_frames)


class AudioPreprocessor:
    def __init__(self, sample_rate=16000, n_mels=128, n_fft=2048,
                 hop_length=512, fmin=20, fmax=8000, target_length=416):
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.fmin = fmin
        self.fmax = fmax
        self.target_length = target_length

        # Initialize mel spectrogram transform
        self.mel_transform = torchaudio.transforms.MelSpectrogram(
            sample_rate=sample_rate,
            n_mels=n_mels,
            n_fft=n_fft,
            hop_length=hop_length,
            f_min=fmin,
            f_max=fmax
        )

        # SpecAugment
        self.freq_masking = torchaudio.transforms.FrequencyMasking(
            freq_mask_param=30)
        self.time_masking = torchaudio.transforms.TimeMasking(
            time_mask_param=20)

    def preprocess(self, input_data, augment=False):
        if isinstance(input_data, str):
            waveform, sr = torchaudio.load(input_data)
            if sr != self.sample_rate:
                waveform = torchaudio.functional.resample(
                    waveform, sr, self.sample_rate)
        else:
            # For real-time audio, find the segment with highest energy
            input_data = np.array(input_data)
            frame_length = 1024
            energies = [np.sum(np.square(input_data[i:i+frame_length]))
                        for i in range(0, len(input_data)-frame_length, frame_length)]
            max_energy_frame = np.argmax(energies)
            center = max_energy_frame * frame_length

            # Center the window around the highest energy
            half_window = len(input_data) // 4
            start = max(0, center - half_window)
            end = min(len(input_data), center + half_window)
            input_data = input_data[start:end]

            # Convert to tensor
            waveform = torch.tensor(input_data).float()
            if waveform.dim() == 1:
                waveform = waveform.unsqueeze(0)
            # Less aggressive normalization for real-time
            max_val = max(abs(waveform.max()), abs(waveform.min()))
            if max_val > 0:
                waveform = waveform / max_val

        mel_spec = self.mel_transform(waveform)
        mel_spec = torch.log(mel_spec + 1e-9)
        # Gentler normalization
        mel_spec = (mel_spec - mel_spec.mean()) / (mel_spec.std() + 1e-9)
        # Wider clipping range
        mel_spec = mel_spec.clip(-4.0, 1.0)

        if augment:
            if torch.rand(1) < 0.5:
                mel_spec = self.freq_masking(mel_spec)
            if torch.rand(1) < 0.5:
                mel_spec = self.time_masking(mel_spec)

        if self.target_length is not None:
            n_frames = mel_spec.shape[-1]
            if n_frames < self.target_length:
                pad_length = self.target_length - n_frames
                mel_spec = torch.nn.functional.pad(mel_spec, (0, pad_length))
            elif n_frames > self.target_length:
                mel_spec = mel_spec[..., :self.target_length]

        return mel_spec

    def pad_to_length(self, mel_spec, target_length):
        n_frames = mel_spec.shape[-1]
        if n_frames < target_length:
            # Pad shorter sequences
            pad_length = target_length - n_frames
            mel_spec = torch.nn.functional.pad(mel_spec, (0, pad_length))
        elif n_frames > target_length:
            # Trim longer sequences
            mel_spec = mel_spec[..., :target_length]
        return mel_spec


class WakeWordDataset(Dataset):
    def __init__(self, root_dir, preprocessor, is_training=True):
        self.root_dir = Path(root_dir)
        self.preprocessor = preprocessor
        self.is_training = is_training
        self.samples = []

        # load positive samples
        pos_path = self.root_dir / "positive"
        for audio_file in pos_path.glob('*.wav'):
            self.samples.append((str(audio_file), 1))

        # load negative samples
        neg_path = self.root_dir / "negative"
        for audio_file in neg_path.glob('*wav'):
            self.samples.append((str(audio_file), 0))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        audio_path, label = self.samples[idx]
        mel_spec = self.preprocessor.preprocess(
            audio_path, augment=self.is_training)
        return mel_spec, torch.tensor(label, dtype=torch.float32)


class WakeWordDetector(nn.Module):
    def __init__(self):
        super().__init__()

       # convolutional layers with batch normalization
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)

        # pooling
        self.pool = nn.MaxPool2d(2, 2)

        # adaptive pooling to handle variable input sizes
        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))

        # fully connected layers with dropout
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, 1)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))

        x = self.adaptive_pool(x)

        x = x.view(-1, 128 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.sigmoid(self.fc2(x))
        return x


def train_model(model, train_loader, val_loader, device, num_epochs=50):
    model = model.to(device)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = ReduceLROnPlateau(
        optimizer, mode='min', patience=5, factor=0.5)

    best_val_loss = float('inf')

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        for specs, labels in train_loader:
            specs, labels = specs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(specs)
            loss = criterion(outputs, labels.unsqueeze(1))

            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        model.eval()
        val_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for specs, labels in val_loader:
                specs, labels = specs.to(device), labels.to(device)
                outputs = model(specs)
                val_loss += criterion(outputs, labels.unsqueeze(1)).item()

                predicted = (outputs > 0.5).float()

                total += labels.size(0)
                correct += (predicted.squeeze() == labels).sum().item()

        train_loss /= len(train_loader)
        val_loss /= len(val_loader)
        accuracy = 100 * correct / total

        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'Train Loss: {train_loss:.4f}')
        print(f'Val Loss: {val_loss:.4f}')
        print(f'Val Accuracy: {accuracy:.2f}%')

        scheduler.step(val_loss)

        if val_loss < best_val_loss:
            print(f"\nImprovement detected:")
            print(f"Previous best val_loss: {best_val_loss:.4f}")
            print(f"New best val_loss: {val_loss:.4f}")
            best_val_loss = val_loss
            try:
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_loss': val_loss,
                    'accuracy': accuracy
                }, "wake_word_detector.pth")
                print("Saved best model!")
            except Exception as e:
                print(f"Error saving model: {e}")
    return model


def prepare_dataset(
    source_dir: str,
    output_dir: str,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    random_seed: int = 42
):
    """
    Prepares dataset by organizing and splitting audio files into train/val/test sets.

    Args:
        source_dir: Directory containing 'positive' and 'negative' subdirectories
        output_dir: Where to save the split dataset
        train_ratio: Proportion of data for training
        val_ratio: Proportion of data for validation
        test_ratio: Proportion of data for testing
        random_seed: Random seed for reproducibility
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)

    # Create output directories
    splits = ['train', 'val', 'test']
    for split in splits:
        for label in ['positive', 'negative']:
            (output_path / split / label).mkdir(parents=True, exist_ok=True)

    # Process positive and negative samples
    for label in ['positive', 'negative']:
        # Get all wav files
        files = list((source_path / label).glob('*.wav'))
        print(f"Found {len(files)} {label} samples")

        # Split files into train, val, and test sets
        train_files, temp_files = train_test_split(
            files,
            train_size=train_ratio,
            random_state=random_seed
        )

        # Split remaining files into val and test
        relative_ratio = val_ratio / (val_ratio + test_ratio)
        val_files, test_files = train_test_split(
            temp_files,
            train_size=relative_ratio,
            random_state=random_seed
        )

        # Copy files to their respective directories
        for file, split_dir in zip(
            [train_files, val_files, test_files],
            ['train', 'val', 'test']
        ):
            for src_file in file:
                dst_file = output_path / split_dir / label / src_file.name
                shutil.copy2(src_file, dst_file)

        print(f"{label} split:")
        print(f"  Train: {len(train_files)}")
        print(f"  Val: {len(val_files)}")
        print(f"  Test: {len(test_files)}")

    # Verify dataset balance
    print("\nDataset balance:")
    for split in splits:
        pos_count = len(list((output_path / split / 'positive').glob('*.wav')))
        neg_count = len(list((output_path / split / 'negative').glob('*.wav')))
        total = pos_count + neg_count
        print(f"\n{split} set:")
        print(f"  Total samples: {total}")
        print(f"  Positive: {pos_count} ({pos_count/total*100:.1f}%)")
        print(f"  Negative: {neg_count} ({neg_count/total*100:.1f}%)")


def main():
    max_frames = analyze_audio_lengths("./data/dataset")

    # Initialize preprocessor with padding only (no trimming)
    preprocessor = AudioPreprocessor(target_length=416)
    prepare_dataset(
        source_dir="/Users/pasquale/Desktop/roboticArm/ai/wake-word-model/data/audio",
        output_dir="./data/dataset",
        train_ratio=0.8,
        val_ratio=0.1,
        test_ratio=0.1
    )
    train_dataset = WakeWordDataset(
        "./data/dataset/train", preprocessor, is_training=True)
    val_dataset = WakeWordDataset(
        "./data/dataset/val", preprocessor, is_training=False)

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = WakeWordDetector()
    best_model = train_model(model, train_loader, val_loader, device)


if __name__ == "__main__":
    main()
