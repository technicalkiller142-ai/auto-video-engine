import os
import json
import subprocess
import sys
from pathlib import Path

def cloud_runner():
    task_file = Path("pipeline_task.json")
    if not task_file.exists():
        print("No pipeline_task.json found.")
        return

    with open(task_file, "r") as f:
        task = json.load(f)

    mode = task.get("mode")
    print(f"Running mode: {mode}")

    def ensure_package(pkg):
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            print(f"Installing missing package: {pkg}")
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], check=True)

    if mode == "align":
        ensure_package("demucs")
        ensure_package("whisperx")
        ensure_package("librosa")
        ensure_package("soundfile")
        ensure_package("scipy")
        subprocess.run(["python", "alignment/align_and_beat.py"], check=True)
        # Move outputs to /kaggle/working
        for f in ["word-timestamps.json", "phrases.json", "beat-map.json"]:
            if (Path("data") / f).exists():
                shutil.copy2(Path("data") / f, Path("/kaggle/working") / f)

    elif mode in ["sync_test", "render"]:
        ensure_package("libraqm") # Check Node and FFmpeg separately
        # Install Node.js and Remotion deps (simulated via apt/npm calls)
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "nodejs", "npm", "ffmpeg", "libnss3", "libatk1.0-0", "libgbm1", "libasound2"], check=True)
        subprocess.run(["npm", "install"], cwd="video", check=True)
        
        cmd = ["npx", "remotion", "render", f"video/src/index.ts", 
               "MainVideo" if mode == "render" else "SyncTest", 
               task.get("output_name", "output_video.mp4"),
               "--frames", f"{task.get('start_sec')}-{task.get('end_sec')}" if task.get('start_sec') else "full"]
        subprocess.run(cmd, cwd="video", check=True)
        
        subprocess.run(["rm", "-rf", "/kaggle/working/auto-video-engine"])

if __name__ == "__main__":
    cloud_runner()
