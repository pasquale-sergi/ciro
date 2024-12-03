import torch
import os
from main import WakeWordDetector, AudioPreprocessor, WakeWordDataset
from torch.utils.data import DataLoader
import librosa
import numpy as np
import matplotlib.pyplot as plt


def analyze_test_set():
    test_dir = "./data/dataset/test"
    pos_dir = os.path.join(test_dir, "positive")
    neg_dir = os.path.join(test_dir, "negative")

    print("\nTest Set Analysis:")
    print(f"Positive samples: {len(os.listdir(pos_dir))}")
    print(f"Negative samples: {len(os.listdir(neg_dir))}")

    # Analyze audio properties
    print("\nAnalyzing audio properties...")
    for dirname, label in [(pos_dir, "Positive"), (neg_dir, "Negative")]:
        durations = []
        sr_values = []
        for f in os.listdir(dirname):
            if f.endswith('.wav'):
                audio_path = os.path.join(dirname, f)
                y, sr = librosa.load(audio_path, sr=None)
                duration = len(y) / sr
                durations.append(duration)
                sr_values.append(sr)

        print(f"\n{label} samples:")
        print(
            f"Duration - Mean: {np.mean(durations):.2f}s, Min: {min(durations):.2f}s, Max: {max(durations):.2f}s")
        print(f"Sample rates: {set(sr_values)}")


def evaluate_model(model, test_loader, device):
    model.eval()
    correct = 0
    total = 0
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    print("\nDetailed Test Analysis:")
    with torch.no_grad():
        for specs, labels in test_loader:
            specs, labels = specs.to(device), labels.to(device)
            outputs = model(specs)
            predicted = (outputs > 0.5).float()

            # Update metrics
            total += labels.size(0)
            correct += (predicted.squeeze() == labels).sum().item()

            # Update confusion matrix
            true_positives += ((predicted.squeeze() == 1) &
                               (labels == 1)).sum().item()
            false_positives += ((predicted.squeeze() == 1)
                                & (labels == 0)).sum().item()
            true_negatives += ((predicted.squeeze() == 0) &
                               (labels == 0)).sum().item()
            false_negatives += ((predicted.squeeze() == 0)
                                & (labels == 1)).sum().item()

    # Calculate metrics
    accuracy = 100 * correct / total
    precision = true_positives / \
        (true_positives + false_positives) if (true_positives +
                                               false_positives) > 0 else 0
    recall = true_positives / \
        (true_positives + false_negatives) if (true_positives +
                                               false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision +
                                     recall) if (precision + recall) > 0 else 0

    print(f"\nTest Results:")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")
    print("\nConfusion Matrix:")
    print(f"True Positives: {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"True Negatives: {true_negatives}")
    print(f"False Negatives: {false_negatives}")


def visualize_predictions(model, test_loader, device, n_samples=5):
    model.eval()
    specs_to_plot = []
    predictions = []
    true_labels = []

    with torch.no_grad():
        for specs, labels in test_loader:
            specs, labels = specs.to(device), labels.to(device)
            outputs = model(specs)

            for i in range(min(len(specs), n_samples - len(specs_to_plot))):
                specs_to_plot.append(specs[i].cpu().numpy())
                predictions.append(outputs[i].item())
                true_labels.append(labels[i].item())

            if len(specs_to_plot) >= n_samples:
                break

    # Plot spectrograms
    plt.figure(figsize=(15, 3))
    for i in range(len(specs_to_plot)):
        plt.subplot(1, len(specs_to_plot), i+1)
        plt.imshow(specs_to_plot[i].squeeze(), aspect='auto', origin='lower')
        plt.title(f'True: {"Ciro" if true_labels[i] == 1 else "Not Ciro"}\n' +
                  f'Pred: {predictions[i]:.2f}')
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('test_spectrograms.png')
    plt.close()


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Initialize preprocessor and model
    preprocessor = AudioPreprocessor(target_length=416)
    model = WakeWordDetector()

    # Load the trained model
    try:
        checkpoint = torch.load('wake_word_detector.pth')
        model.load_state_dict(checkpoint['model_state_dict'])
        print(
            f"Loaded model from epoch {checkpoint['epoch']} with validation accuracy {checkpoint['accuracy']:.2f}%")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    model = model.to(device)
    model.eval()

    # Analyze test set
    analyze_test_set()

    # Load test data
    test_dataset = WakeWordDataset(
        "./data/dataset/test", preprocessor, is_training=False)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    # Evaluate model
    evaluate_model(model, test_loader, device)

    # Visualize some predictions
    visualize_predictions(model, test_loader, device)


if __name__ == "__main__":
    main()
