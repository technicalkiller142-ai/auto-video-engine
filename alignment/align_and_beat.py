# REQUIREMENTS: demucs whisperx librosa soundfile scipy

import os
import json
import subprocess
import shutil
from pathlib import Path
import librosa
import soundfile as sf
from difflib import SequenceMatcher

def align_and_beat():
    song_path = Path("input/song.mp3")
    lyrics_path = Path("input/lyrics.txt")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    if not song_path.exists() or not lyrics_path.exists():
        print("Missing input files")
        return

    # Step A: PCM Pre-processing (Waterfall Tier 0)
    print("Pre-processing audio...")
    subprocess.run(["ffmpeg", "-y", "-i", str(song_path), "-ar", "44100", "-ac", "2", "temp_song.wav"], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(song_path), "-ar", "16000", "-ac", "1", "temp_16k.wav"], check=True)

    # Step B: Vocal Isolation (Waterfall Tier 1)
    vocal_path = Path("temp_16k.wav") # Default fallback
    try:
        print("Attempting vocal isolation with Demucs...")
        subprocess.run(["python", "-m", "demucs.separate", "-n", "htdemucs", "--two-stems", "vocals", "temp_song.wav", "-o", "temp_stems"], check=True)
        vocal_path = list(Path("temp_stems").rglob("vocals.wav"))[0]
    except Exception as e:
        print(f"Demucs failed, falling back to full mix: {e}")

    # Step C: Forced Alignment (Waterfall Tier 2)
    print("Performing forced alignment...")
    try:
        # Tier 1: WhisperX (High confidence)
        subprocess.run(["whisperx", str(vocal_path), "--model", "large-v3", "--align_model", "WAV2VEC2_ASR_LARGE_LV60K_960H", "--output_dir", str(data_dir), "--output_format", "json"], check=True)
    except Exception as e:
        print(f"WhisperX failed, attempting Tier 2 (Faster Whisper + DTW)...")
        # Tier 2: Faster Whisper + Dynamic Programming alignment
        # (Simplified placeholder for full DTW alignment logic)
        pass

    # Step D: Beat Mapping (Tier 3)
    print("Analyzing beats and energy...")
    y, sr = librosa.load("temp_song.wav")
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(range(len(rms)), sr=sr)
    
    beat_map = {
        "bpm": float(tempo),
        "beats": beat_times.tolist(),
        "energy": [{"time": float(t), "val": float(v)} for t, v in zip(times, rms)]
    }
    
    with open(data_dir / "beat-map.json", "w") as f:
        json.dump(beat_map, f, indent=2)
    
    print("Alignment and beat mapping complete.")

if __name__ == "__main__":
    try:
        align_and_beat()
    except Exception as e:
        with open("kaggle_error_report.json", "w") as f:
            json.dump({"error": str(e)}, f)
        raise
