import pyaudio
import torch
import numpy as np
import threading
import queue
import time
from collections import deque
from main import WakeWordDetector, AudioPreprocessor
import os
import torchaudio


class RealTimeWakeWordDetector:
    def __init__(self, model_path, preprocessor, threshold=0.85):
        # Load model
        self.model = WakeWordDetector()
        checkpoint = torch.load(model_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

        self.preprocessor = preprocessor
        self.threshold = threshold

        # Compare preprocessing before starting
        self.compare_preprocessing()

        # Audio parameters
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 1  # Window size

        self.p = pyaudio.PyAudio()
        self.audio_queue = queue.Queue()
        self.audio_buffer = deque(maxlen=int(self.RATE * self.RECORD_SECONDS))
        self.running = False
        self.last_detection_time = 0

    def compare_preprocessing(self):
        print("\nPreprocessing Comparison:")
        # Load a training sample
        train_dir = "./data/dataset/train/positive"
        train_file = os.path.join(train_dir, os.listdir(train_dir)[0])

        # Process training sample
        waveform_train, sr = torchaudio.load(train_file)
        mel_spec_train = self.preprocessor.preprocess(train_file)

        # Process simulated real-time audio
        audio_chunk = np.random.rand(16000)  # 1 second of random audio
        mel_spec_realtime = self.preprocessor.preprocess(audio_chunk)

        print(f"Training audio shape: {waveform_train.shape}")
        print(f"Training mel spec shape: {mel_spec_train.shape}")
        print(f"Realtime mel spec shape: {mel_spec_realtime.shape}")
        print(
            f"Training mel spec range: [{mel_spec_train.min():.2f}, {mel_spec_train.max():.2f}]")
        print(
            f"Realtime mel spec range: [{mel_spec_realtime.min():.2f}, {mel_spec_realtime.max():.2f}]")

    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        self.audio_queue.put(audio_data)
        return (in_data, pyaudio.paContinue)

    def process_audio(self):
        COOLDOWN_PERIOD = 0.5
        STRIDE = 0.1
        consecutive_detections = 0
        DETECTION_THRESHOLD = 0.35
        CONSECUTIVE_REQUIRED = 3

        while self.running:
            if not self.audio_queue.empty():
                audio_chunk = self.audio_queue.get()
                self.audio_buffer.extend(audio_chunk)

                if len(self.audio_buffer) >= self.RATE * self.RECORD_SECONDS:
                    current_time = time.time()
                    if current_time - self.last_detection_time > COOLDOWN_PERIOD:
                        # Normalize audio
                        audio_data = np.array(list(self.audio_buffer))
                        energy = np.sqrt(np.mean(np.square(audio_data)))

                        if energy > 0.01:  # Only process if there's significant audio
                            try:
                                mel_spec = self.preprocessor.preprocess(
                                    audio_data)
                                mel_spec = mel_spec.unsqueeze(0)

                                with torch.no_grad():
                                    prediction = self.model(mel_spec)

                                    # Debug output
                                    if prediction.item() > 0.3:
                                        print(f"Debug - Prediction: {prediction.item():.4f}, "
                                              f"Energy: {energy:.4f}, "
                                              f"Buffer max: {np.max(np.abs(audio_data)):.4f}")

                                    # Consecutive detection logic
                                    if prediction.item() > DETECTION_THRESHOLD:
                                        consecutive_detections += 1
                                    else:
                                        consecutive_detections = 0

                                    if consecutive_detections >= CONSECUTIVE_REQUIRED:
                                        print(
                                            f"Wake word detected! Confidence: {prediction.item():.4f}")
                                        consecutive_detections = 0
                                        self.last_detection_time = current_time

                            except Exception as e:
                                print(f"Error processing audio: {e}")

                    # Slide window
                    samples_to_remove = int(self.RATE * STRIDE)
                    for _ in range(samples_to_remove):
                        if self.audio_buffer:
                            self.audio_buffer.popleft()

    def start(self):
        self.running = True

        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )

        self.process_thread = threading.Thread(target=self.process_audio)
        self.process_thread.start()

        print("\nListening for wake word 'Ciro'...")
        print("Press Ctrl+C to stop")

    def stop(self):
        self.running = False
        if hasattr(self, 'process_thread'):
            self.process_thread.join()
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()


def main():
    preprocessor = AudioPreprocessor(target_length=416)

    detector = RealTimeWakeWordDetector(
        model_path='wake_word_detector.pth',
        preprocessor=preprocessor,
        threshold=0.85  # Adjust this based on testing
    )

    try:
        detector.start()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
        detector.stop()


if __name__ == "__main__":
    main()
