
import torch
import torch.nn as nn
from process_data import CommandDataset, AudioProcessor
from model import SpeechCommandModel, train_epoch, validate
import matplotlib.pyplot as plt
import numpy as np
import torchaudio
from pathlib import Path


class AudioAugmenter:
    def __init__(self):
        pass

    def augment(self, specs, epoch):
        aug_type = np.random.choice(
            ['none', 'freq_mask', 'time_mask', 'noise'])
        aug_strength = 0.01  # You can vary this value based on epoch or model performance

        if aug_type == 'freq_mask':
            mask = torch.ones_like(specs)
            freq_idx = np.random.randint(0, specs.shape[2] - 20)
            mask[:, :, freq_idx:freq_idx + 20, :] = 0
            specs = specs * mask
        elif aug_type == 'time_mask':
            mask = torch.ones_like(specs)
            time_idx = np.random.randint(0, specs.shape[3] - 5)
            mask[:, :, :, time_idx:time_idx + 5] = 0
            specs = specs * mask
        elif aug_type == 'noise':
            noise = torch.randn_like(specs) * aug_strength
            specs = specs + noise

        return specs


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    preprocessor = AudioProcessor()
    dataset = CommandDataset(
        "/Users/pasquale/Desktop/roboticArm/ai/speech-model/data/", preprocessor)

    # Load previous best model (Optional)
    # best_model_path = 'new_best_model.pth'
    model = SpeechCommandModel(n_commands=3).to(device)

    # If you'd like to resume training from the best model
    # if Path(best_model_path).exists():
    #     model.load_state_dict(torch.load(best_model_path))
    #     print("Loaded previous best model")

    # Split dataset into training and validation
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size])

    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=32, shuffle=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=32)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=1e-4, weight_decay=0.01)
    warmup_scheduler = torch.optim.lr_scheduler.LinearLR(
        optimizer, start_factor=0.1, total_iters=5 * len(train_loader))

    augmenter = AudioAugmenter()
    best_acc = 0
    train_accuracies = []
    val_accuracies = []
    best_loss = float('inf')

    n_epochs = 100
    for epoch in range(n_epochs):
        model.train()
        total_loss = 0
        correct = 0
        total = 0

        for batch in train_loader:
            specs = batch['spectrogram'].to(device)
            labels = batch['action_label'].to(device)

            specs = specs.float()  # Ensure float32

            # Apply augmentation after the first epoch
            if epoch > 5:
                specs = augmenter.augment(specs, epoch)

            optimizer.zero_grad()
            outputs = model(specs)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            if epoch < 5:
                warmup_scheduler.step()

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        train_acc = 100. * correct / total
        val_loss, val_acc = validate(model, val_loader, criterion, device)

        train_accuracies.append(train_acc)
        val_accuracies.append(val_acc)

        print(f'Epoch {epoch+1}/{n_epochs}:')
        print(
            f'Train Loss: {total_loss/len(train_loader):.4f} | Train Acc: {train_acc:.2f}%')
        print(f'Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%')

        # Save the best model
        if val_acc > best_acc or (val_acc == best_acc and val_loss < best_loss):
            best_acc = val_acc
            best_loss = val_loss
            torch.save(model.state_dict(), 'more_data_best_model.pth')
            print(
                f'New best model saved with validation accuracy: {val_acc:.2f}% and loss: {val_loss:.4f}')

    # Plot training progress
    plt.figure(figsize=(10, 6))
    plt.plot(train_accuracies, label='Train Accuracy')
    plt.plot(val_accuracies, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Training Progress')
    plt.legend()
    plt.grid(True)
    plt.savefig('training_progress.png')
    plt.close()


if __name__ == "__main__":
    main()
