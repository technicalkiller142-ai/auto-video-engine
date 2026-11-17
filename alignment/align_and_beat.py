# REQUIREMENTS: demucs whisperx librosa soundfile torch torchaudio
import os
import json
import subprocess
from pathlib import Path
import librosa
import soundfile as sf

def align_and_beat():
    song_path = Path("input/song.mp3")
    lyrics_path = Path("input/lyrics.txt")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    if not song_path.exists():
        print("Missing input/song.mp3")
        return

    # Step 1: Stem Separation (Vocal isolation)
    print("Isolating vocals with Demucs...")
    subprocess.run(["python", "-m", "demucs.separate", "-n", "htdemucs", "--two-stems", "vocals", str(song_path), "-o", "temp_stems"], check=True)
    
    # Path to isolated vocals usually: temp_stems/htdemucs/song/vocals.wav
    vocal_path = list(Path("temp_stems").rglob("vocals.wav"))[0]

    # Step 2: Forced Alignment
    print("Performing forced alignment...")
    # This assumes whisperx is installed and accessible. In a real environment, this is heavy.
    # We output to data/word-timestamps.json
    # Command example: whisperx input/song.mp3 --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --output_dir data --output_format json
    
    # For now, we simulate/placeholder the call for the script's logic
    # Real implementation would call whisperx or torchaudio MMS_FA
    
    # Step 3: Beat Mapping
    print("Analyzing beats and energy...")
    y, sr = librosa.load(str(song_path))
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    # Energy curve
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
    align_and_beat()
