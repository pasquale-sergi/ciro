import os
import spectrogram as spect

def process_audio_files(positive_dir, negative_dir, spectrogram_pos_save_dir, spectrogram_neg_save_dir):
    """
    Process audio files in the specified directories, creating and saving their spectrograms.

    Args:
        positive_dir (str): Directory containing positive audio files.
        negative_dir (str): Directory containing negative audio files.
        spectrogram_pos_save_dir (str): Directory to save positive spectrograms.
        spectrogram_neg_save_dir (str): Directory to save negative spectrograms.
    """
    # Process positive audio files
    for filename in os.listdir(positive_dir):
        if filename.endswith(".wav"):
            audio_path = os.path.join(positive_dir, filename)
            saved_path = process_audio(audio_path, spectrogram_pos_save_dir)
            
            # Check if spectrogram already exists
            if not os.path.exists(saved_path):
                saved_path = process_audio(audio_path, spectrogram_pos_save_dir)
                print(f"Saved positive spectrogram: {saved_path}")
            # else:
                # print(f"Positive spectrogram already exists: {saved_path}")

    # Process negative audio files
    for filename in os.listdir(negative_dir):
        if filename.endswith(".wav"):
            audio_path = os.path.join(negative_dir, filename)
            saved_path = process_audio(audio_path, spectrogram_neg_save_dir)
            
            # Check if spectrogram already exists
            if not os.path.exists(saved_path):
                saved_path = process_audio(audio_path, spectrogram_neg_save_dir)
                print(f"Saved negative spectrogram: {saved_path}")
            # else:
                # print(f"Negative spectrogram already exists: {saved_path}")

def process_audio(audio_path, save_directory):
    """
    Create and save a spectrogram from an audio file.

    Args:
        audio_path (str): Path to the audio file.
        save_directory (str): Directory to save the spectrogram.

    Returns:
        str: Path to the saved spectrogram file.
    """
    spectrogram = spect.createSpectrogram(audio_path)
    saved_path = spect.saveSpectrogram(save_directory, spectrogram, audio_path)
    return saved_path
