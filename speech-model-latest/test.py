import torch
import pyaudio
import wave
import numpy as np
from pathlib import Path
import time
from model import SpeechCommandModel
from process_data import CommandDataset, AudioProcessor


def test_audio(model, preprocessor, device, action_to_idx):
    # Audio recording parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("\nRecording... Say your command")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    print("Done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Process audio data once
    audio_data = b''.join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    audio_float = audio_array.astype(np.float32) / 32768.0

    print("\nAudio input stats (processed once):")
    print("- Min:", float(np.min(audio_float)))
    print("- Max:", float(np.max(audio_float)))
    print("- Mean:", float(np.mean(audio_float)))
    print("- Std:", float(np.std(audio_float)))

    # Save temporary file
    temp_file = "temp_test.wav"
    with wave.open(temp_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)  # Write original int16 data

    # Get mel spectrogram
    mel_spec = preprocessor.process_file(temp_file)
    mel_spec = mel_spec.unsqueeze(0).to(device)

    print("\nMel spectrogram stats:")
    print("Shape:", mel_spec.shape)

    print("Min/Max:", mel_spec.min().item(), mel_spec.max().item())

    model.eval()

    with torch.no_grad():
        # Get raw outputs before softmax
        output = model(mel_spec)
        raw_outputs = output[0].tolist()
        print("3. Raw model outputs:", raw_outputs)
        print("4. Output shape:", output.shape)

        # Apply softmax for probabilities
        probabilities = torch.nn.functional.softmax(output, dim=1)
        pred = torch.argmax(output, dim=1).item()
        print("5. Predicted index:", pred)

    # Print predictions in both orders for comparison
    idx_to_action = {v: k for k, v in action_to_idx.items()}
    print("\nPredictions by index order:")
    for idx in range(len(idx_to_action)):
        cmd = idx_to_action[idx]
        prob = probabilities[0][idx].item() * 100
        print(f"Index {idx} ({cmd}): {prob:.2f}%")

    print("\nPredictions by command name:")
    for cmd in sorted(action_to_idx.keys()):
        idx = action_to_idx[cmd]
        prob = probabilities[0][idx].item() * 100
        print(f"{cmd} (Index {idx}): {prob:.2f}%")

    predicted_command = idx_to_action[pred]
    confidence = probabilities[0][pred].item() * 100
    print(f"\nBest prediction: {predicted_command}")
    print(f"Confidence: {confidence:.2f}%")
    return predicted_command, confidence


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load data mapping first to see what indices should be
    print("\nLoading dataset to get command mapping...")
    preprocessor = AudioProcessor()
    dataset = CommandDataset("./data/", preprocessor)
    action_to_idx = dataset.action_to_idx

    # Swap the indices to match what the model learned
    action_to_idx = {
        'grab_apple': action_to_idx['put_it_down'],
        'put_it_down': action_to_idx['grab_apple'],
        'in_position': action_to_idx['in_position']
    }
    print("\nDataset command mapping:")
    for cmd, idx in sorted(action_to_idx.items()):
        print(f"{cmd}: {idx}")

    # Load model and verify parameters
    print("\nLoading model...")
    model = SpeechCommandModel(n_commands=3).to(device)

    # Load state dict and inspect
    state_dict = torch.load('more_data_best_model.pth')
    print("\nModel state dict keys:")
    for key in state_dict.keys():
        print(key)

    # Load the state dict
    model.load_state_dict(state_dict)

    # Inspect final layer weights
    classifier_weights = model.classifier[-1].weight.data
    print("\nFinal layer weights shape:", classifier_weights.shape)
    print("Weight statistics per class:")
    for i in range(classifier_weights.shape[0]):
        stats = {
            'mean': torch.mean(classifier_weights[i]).item(),
            'std': torch.std(classifier_weights[i]).item()
        }
        print(f"Class {i}: mean={stats['mean']:.4f}, std={stats['std']:.4f}")

    print("\nTesting prediction order...")
    # Create a dummy input
    dummy_input = torch.randn(1, 1, 128, 63).to(device)
    model.eval()
    with torch.no_grad():
        output = model(dummy_input)
        print("Output shape:", output.shape)
        print("Raw outputs:", output[0].tolist())

    print("\nCommand Mapping:")
    for cmd, idx in action_to_idx.items():
        print(f"- {idx}: {cmd}")

    while True:
        input("\nPress Enter to record a command (or Ctrl+C to exit)")
        test_audio(model, preprocessor, device, action_to_idx)


if __name__ == "__main__":
    main()
