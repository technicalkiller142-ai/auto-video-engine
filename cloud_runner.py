import os, sys, json, shutil, traceback, subprocess
from pathlib import Path

def main():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "faster-whisper", "librosa", "soundfile"], check=False)
        task = json.loads(Path("pipeline_task.json").read_text(encoding="utf-8")) if Path("pipeline_task.json").exists() else {"mode": "align"}
        mode = task.get("mode", "align")
        print(f"=== Running Fast Checkpoint Mode: {mode} ===")
        if mode == "align":
            sys.path.insert(0, str(Path("alignment").resolve()))
            from align_and_beat import run_alignment
            run_alignment()
            for fn in ["beat-map.json", "word-timestamps.json", "phrases.json"]:
                src = Path("data") / fn
                if src.exists():
                    shutil.copy2(src, Path("/kaggle/working") / fn)
            print("=== ALIGNMENT COMPLETE ===")
    except Exception as e:
        err = {"status": "error", "error": str(e), "traceback": traceback.format_exc()}
        Path("/kaggle/working/kaggle_error_report.json").write_text(json.dumps(err, indent=2), encoding="utf-8")
        print(err["traceback"])
        sys.exit(1)

if __name__ == "__main__":
    main()
