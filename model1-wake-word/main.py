import numpy as np
import processAudio as pa
from sklearn.model_selection import train_test_split
import loadImages as li
import tensorflow as tf
from tensorflow.keras import Sequential, layers
import model
import os
from datetime import datetime
from tensorflow.keras.callbacks import EarlyStopping


early_stopping = EarlyStopping(
    monitor='val_loss',   # Metric to monitor
    patience=5,           # Number of epochs with no improvement to wait before stopping
    verbose=1,            # Verbosity level, set to 1 to print messages
    # Restore model weights from the epoch with the best value of the monitored metric
    restore_best_weights=True
)
# Define your directories
positive_dir = os.path.join("data/audio/positive")
negative_dir = os.path.join("data/audio/negative")
spectrogram_pos_save_dir = os.path.join("data/spectrograms/positiveSpectr")
spectrogram_neg_save_dir = os.path.join("data/spectrograms/negativeSpectr")

# Process and save audio files as spectrograms
pa.process_audio_files(positive_dir, negative_dir,
                       spectrogram_pos_save_dir, spectrogram_neg_save_dir)

# Load the spectrograms and labels for training
spectrogram_paths = []
labels = []

# Load spectrograms and labels for training
for filename in os.listdir(spectrogram_pos_save_dir):
    if filename.endswith('.png'):
        spectrogram_path = os.path.join(spectrogram_pos_save_dir, filename)
        spectrogram_paths.append(spectrogram_path)
        labels.append(1)  # Positive label

for filename in os.listdir(spectrogram_neg_save_dir):
    if filename.endswith('.png'):
        spectrogram_path = os.path.join(spectrogram_neg_save_dir, filename)
        spectrogram_paths.append(spectrogram_path)
        labels.append(0)  # Negative label

# Convert to numpy arrays
spectrogram_paths = np.array(spectrogram_paths)
labels = np.array(labels)
# Split the data into training and validation sets
X_train, X_val, Y_train, Y_val = train_test_split(
    spectrogram_paths, labels, test_size=0.2, random_state=42)

# Load the training and validation sets through the loadImages function
X_train_images = li.loadImages(X_train)
X_val_images = li.loadImages(X_val)

# Print quick check of samples
print(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}")

# Data augmentation for training
data_augmentation = Sequential([
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# Build the model
the_model = model.buildModel()

# Train the model
history = the_model.fit(X_train_images, Y_train, epochs=100,
                        batch_size=32, validation_data=(X_val_images, Y_val), callbacks=[early_stopping])

# Save the model
model_filename = f"wake-word-detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.h5"
the_model.save(model_filename)
