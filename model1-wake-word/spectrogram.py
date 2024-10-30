import librosa
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf
import os

#convert the audio files to spectrograms
def createSpectrogram(audio_path):

    if isinstance(audio_path, str):
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=16000)
    else:
        # Use the numpy array directly
        y = audio_path
        sr = 16000
   
    #create the melspectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=512,n_fft=2048, fmin=20, fmax=8000)
    #convert the melspectrogram in db
    S_db = librosa.power_to_db(S, ref=np.max)

    return S_db

def saveSpectrogram(save_path, spectrogram, audio_filename):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Generate a unique filename based on the original audio filename
    base_filename = os.path.splitext(os.path.basename(audio_filename))[0]
    full_save_path = os.path.join(save_path, f"{base_filename}_spectrogram.png")
    
    plt.figure(figsize=(5,5))
    librosa.display.specshow(spectrogram, sr=16000, x_axis='time', y_axis='mel', fmax=8000)
    plt.axis('off')
    plt.savefig(full_save_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return full_save_path

