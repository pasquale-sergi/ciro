import torch
import torchaudio
from pathlib import Path
from torch.utils.data import Dataset


class AudioProcessor:
    def __init__(self, sample_rate=16000, duration=3, n_mels=128, n_fft=2048, hop_length=512):
        self.sample_rate = sample_rate
        self.duration = duration
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length

        self.target_length = duration * sample_rate

    def load_audio(self, audio_path):
        waveform, sr = torchaudio.load(audio_path)
        if sr != self.sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.sample_rate)
            waveform = resampler(waveform)

        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        return waveform

    def pad_or_trim(self, waveform):
        if waveform.shape[1] < self.target_length:
            padding = self.target_length - waveform.shape[1]
            waveform = torch.nn.functional.pad(waveform, (0, padding))

        else:
            waveform = waveform[:, :self.target_length]

        return waveform

    def compute_melspectrogram(self, waveform):
        mel_transform = torchaudio.transforms.MelSpectrogram(
            sample_rate=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )

        mel_spec = mel_transform(waveform)

        mel_spec = torchaudio.transforms.AmplitudeToDB()(mel_spec)

        return mel_spec

    def process_file(self, file_path):
        waveform = self.load_audio(file_path)
        waveform = self.pad_or_trim(waveform)
        mel_spec = self.compute_melspectrogram(waveform)
        return mel_spec


class CommandDataset(Dataset):

    def __init__(self, data_dir, preprocessor):
        self.data_dir = Path(data_dir)
        self.preprocessor = preprocessor
        self.samples = []
        self.action_to_idx = {}

        self._build_dataset()

    def _build_dataset(self):
        print("\nBuilding dataset - Command mapping:")
        # Sort the command folders to ensure consistent ordering
        sorted_commands = sorted(path for path in self.data_dir.iterdir() if path.is_dir())
        
        for command_folder in sorted_commands:
            command_name = command_folder.name.replace(".wav", "")
            if command_name not in self.action_to_idx:
                print(f"Assigning index {len(self.action_to_idx)} to command {command_name}")
                self.action_to_idx[command_name] = len(self.action_to_idx)
                
                # Print samples being added for this command
                sample_count = len(list(command_folder.glob("*.wav")))
                print(f"Found {sample_count} samples for command {command_name}")
                
                for audio_path in command_folder.glob("*.wav"):
                    self.samples.append({
                        'path': str(audio_path),
                        'action': command_name
                    })
        
        print("\nFinal command mapping:")
        for cmd, idx in sorted(self.action_to_idx.items()):  # Sort here too for consistent display
            print(f"{cmd}: {idx}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        mel_spec = self.preprocessor.process_file(sample['path'])
        action_label = self.action_to_idx[sample['action']]
        return {
            'spectrogram': mel_spec,
            'action_label': action_label
        }


def main():

    preprocessor = AudioProcessor()

    dataset = CommandDataset(
        "/Users/pasquale/Desktop/roboticArm/ai/speech-model/data/", preprocessor)

    print(f"Total samples: {len(dataset)}")
    print(f"Actions: {dataset.action_to_idx}")

    # Example of loading a single sample
    sample = dataset[0]
    print(f"Spectrogram shape: {sample['spectrogram'].shape}")
    print(f"Action label: {sample['action_label']}")


if __name__ == "__main__":
    main()
