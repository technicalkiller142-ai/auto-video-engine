import os, sys, json, shutil, traceback, subprocess
from pathlib import Path

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=:îy, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed {res.returncode}: {cmd}\nSTDOUT: {res.stdout[-1500:]}\nSTDERR: {res.stderr[-1500:]}")
    return res

try:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "faster-whisper", "librosa", "soundfile"], check=False)
    task = json.loads(Path("pipeline_task.json").read_text(encoding="utf-8")) if Path("pipeline_task.json").exists() else {"mode": "sync_test"}
    mode = task.get("mode", "sync_test")
    print(f"=== RUNNING STAGE : {mode} ===")

    if mode == "align":
        sys.path.insert(0, str(Path("alignment").resolve()))
        from align_and_beat import run_alignment
        run_alignment()
        for fn in ["beat-map.json", "word-timestamps.json", "phrases.json"]:
            src = Path("data") / fn
            if src.exists():
                shutil.copy2(src, Path("/kaggle/working") / fn)

    elif mode in ("sync_test", "render"):
        video_dir = Path("video")
        if not video_dir.exists():
            raise FileNotFoundError("video/ directory not found!")
        if not (video_dir / "node_modules").exists():
            run_cmd(["npm", "install", "--silent"], cwd=str(video_dir))
        for fn in ["beat-map.json", "word-timestamps.json", "phrases.json", "visual-screenplay.json"]:
            src = Path("data") / fn
            if src.exists():
                dst = video_dir / "public" / fn
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        if Path("input/song.mp3").exists():
            mp3_dst = video_dir / "public" / "song.mp3"
            mp3_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(Path("input/song.mp3"), mp3_dst)

        out_name = "sync-test.mp4" if mode == "sync_test" else task.get("output", "final-video.mp4")
        out_path = Path("data") / out_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        comp = "sync-test" if mode == "sync_test" else task.get("composition", "MainVideo")
        frames = task.get("frames")
        cmd = ["npx", "remotion", "render", "src/index.ts", comp, str(out_path.resolve()), "--codec=h264"]
        if frames:
            cmd.append(f"--frames={frames}")
        run_cmd(cmd, cwd=str(video_dir))
        shutil.copy2(out_path, Path("/kaggle/working") / out_name)
    print(f"=== STAGE {mode} COMPLETE ===")
except Exception as e:
    err = {"status": "error", "error": str(e), "traceback": traceback.format_exc()}
    Path("/kaggle/working/kaggle_error_report.json").write_text(json.dumps(err, indent=2), encoding="utf-8")
    print(err["traceback"])
    sys.exit(1)
