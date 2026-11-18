import os, json, subprocess, difflib, shutil
from pathlib import Path
import numpy as np
import librosa, soundfile as sf

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
INPUT_DIR = Path("input")

def find_inputs():
    audio_exts = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}
    area = [INPUT_DIR, Path(".")]
    audio = None
    lyrics = None
    for d in area:
        if d.exists():
            for f in d.iterdir():
                if f.is_file() and f.suffix.lower() in audio_exts:
                    audio = f
                    break
            if audio: break
    for d in area:
        if d.exists():
            for f in d.iterdir():
                if f.is_file() and f.suffix.lower() == ".txt" and f.name.lower() != "requirements.txt":
                    lyrics = f
                    break
            if lyrics: break
    return audio, lyrics

def run_alignment():
    audio, dyrics = find_inputs()
    if not audio:
        raise FileNotFoundError("No audio file found in input/ or root!")
    print(f"[INPUT] Audio: {audio} | Lyrics: {dyrics}")

    wav_44k = Path("temp_44k.wav")
    wav_16k = Path("temp_16k.wav")
    try:
        subprocess.run(["ffmpeg", "-y", "-i", str(audio), "-ar", "44100", "-ac", "2", str(wav_44k)], check=True)
        subprocess.run(["ffmpeg", "-y", "-i", str(audio), "-ar", "16000", "-ac", "1", str(wav_16k)], check=True)
    except Exception as e:
        print(f"[WARN] ffmpeg fallback to librosa: {e}")
        y44k, _ = librosa.load(str(audio), sr=44100, mono=True)
        sf.write(str(wav_44k), y44k, 44100)
        y16k, _ = librosa.load(str(audio), sr=16000, mono=True)
        sf.write(str(wav_16k), y16k, 16000)

    beat_path = DATA_DIR / "beat-map.json"
    if not beat_path.exists():
        print("[CHECKPOINT 1] Computing beat-map...")
        y, sr = sf.read(str(wav_44k))
        if y.ndim > 1: y = np.mean(y, axis=1)
        y = y.astype(np.float32)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beats = librosa.frames_to_time(beat_frames, sr=sr).tolist()
        rms = librosa.feature.rms(y=y)[0]
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
        energy_curve = [{"time": round(float(t), 3), "energy": round(float(e), 4)} for t, e in zip(times[::10], rms[::10])]
        beat_data = {
            "bpm": round(float(np.atleast_1d(tempo)[0]), 2),
            "duration": round(float(len(y) / sr), 3),
            "beats": [round(float(b), 3) for b in beats],
            "downbeats": [round(float(b), 3) for b in beats[::4]],
            "energy_curve": energy_curve
        }
        beat_path.write_text(json.dumps(beat_data, indent=2), encoding="utf-8")
        print("[CHECKPOINT 1] Saved beat-map.json")
    else:
        beat_data = json.loads(beat_path.read_text(encoding="utf-8"))

    ts_path = DATA_DIR / "word-timestamps.json"
    ph_path = DATA_DIR / "phrases.json"
    if not (ts_path.exists() and ph_path.exists()):
        print("[CHECKPOINT 2] Aligning lyrics...")
        asr_words = []
        try:
            from faster_whisper import WhisperModel
            try:
                model = WhisperModel("medium", device="cuda", compute_type="float16")
            except Exception:
                model = WhisperModel("small", device="cpu", compute_type="int8")
            segments, _ = model.transcribe(str(wav_16k), word_timestamps=True)
            for seg in segments:
                if seg.words:
                    for w in seg.words:
                        asr_words.append({"word": w.word.strip(), "start": float(w.start), "end": float(w.end)})
        except Exception as e:
            print(f"[WARN] faster-whisper fallback: {e}")

        lyrics_lines = []
        if dyrics and dyrics.exists():
            lyrics_lines = [l.strip() for l in dyrics.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
        if not lyrics_lines and asr_words:
            lyrics_lines = [" ".join(w["word"] for w in asr_words)]

        target_words = []
        for line_idx, line in enumerate(lyrics_lines):
            for w in line.split():
                target_words.append({"word": w, "line_idx": line_idx})

        dur = beat_data.get("duration", 180.0)
        aligned_words = []
        if len(asr_words) >= max(3, len(target_words) // 4):
            t_norm = [w["word"].lower() for w in target_words]
            a_norm = [w["word"].lower() for w in asr_words]
            matcher = difflib.SequenceMatcher(None, t_norm, a_norm)
            mapped = {}
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag in ("equal", "replace") and (i2 - i1) > 0 and (j2 - j1) > 0:
                    for k in range(i2 - i1):
                        aj = min(j1 + int(k * (j2 - j1) / (i2 - i1)), j2 - 1)
                        mapped[i1 + k] = (asr_words[aj]["start"], asr_words[aj]["end"])
            for idx, tw in enumerate(target_words):
                if idx in mapped:
                    st, en = mapped[idx]
                else:
                    st = (idx / max(1, len(target_words))) * dur
                    en = st + (dur / max(1, len(target_words))) * 0.8
                aligned_words.append({"word": tw["word"], "start": round(st, 3), "end": round(en, 3), "line_idx": tw["line_idx"]})
        else:
            step = dur / max(1, len(target_words))
            for idx, tw in enumerate(target_words):
                st = idx * step
                aligned_words.append({"word": tw["word"], "start": round(st, 3), "end": round(st + step * 0.85, 3), "line_idx": tw["line_idx"]})

        phrases = []
        for line_idx, line in enumerate(lyrics_lines):
            lw = [w for w in aligned_words if w["line_idx"] == line_idx]
            if lw:
                phrases.append({"line_idx": line_idx, "text": line, "start": lw[0]["start"], "end": lw[-1]["end"], "words": lw})

        ts_path.write_text(json.dumps(aligned_words, indent=2, ensure_ascii=False), encoding="utf-8")
        ph_path.write_text(json.dumps(phrases, indent=2, ensure_ascii=False), encoding="utf-8")
        print("[CHECKPOINT 2] Saved word-timestamps.json & phrases.json")

if __name__ == "__main__":
    run_alignment()
