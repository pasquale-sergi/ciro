
import os
import numpy as np
import spectrogram as spect
import loadImages as li
import tensorflow as tf


def test_audio_clips(audio_path, model):
    spectrogram = spect.createSpectrogram(audio_path)

    # Save temp spectrogram
    temp_spect = spect.saveSpectrogram(
        "/Users/pasquale/Desktop/roboticArm/model1-wake-word/data/test/tempSpectr", spectrogram, audio_path)
    spectrogram_image = li.loadImages([temp_spect])

    prediction = model.predict(spectrogram_image)

    predicted_label = 1 if prediction[0] > 0.5 else 0
    confidence = prediction[0][0] if predicted_label == 1 else 1 - \
        prediction[0][0]

    return predicted_label, confidence


def test_audio_folder(folder_path, model):
    results = []

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):  # Ensure it's a .wav file
            audio_clip_path = os.path.join(folder_path, filename)
            predicted_label, confidence = test_audio_clips(
                audio_clip_path, model)
            results.append((filename, predicted_label, confidence))

    return results


# Specify the folder containing unseen audio clips
unseen_audio_folder = "/Users/pasquale/Desktop/roboticArm/model1-wake-word/data/test/unseenAudio"
loaded_model = tf.keras.models.load_model(
    '/Users/pasquale/Desktop/roboticArm/model1-wake-word/wake-word-detection_20241026_155140.h5')

# Test all audio files in the folder
test_results = test_audio_folder(unseen_audio_folder, loaded_model)

# Print results
for filename, label, conf in test_results:
    print(f"File: {filename}, Predicted label: {label} (1: Trigger Word Detected, 0: Not Detected), Confidence: {conf:.2f}")
