import os
import json
import subprocess
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

    if mode == "align":
        # Install and run alignment
        subprocess.run(["pip", "install", "-q", "demucs", "whisperx", "librosa", "soundfile", "torch", "torchaudio"], check=True)
        subprocess.run(["python", "alignment/align_and_beat.py"], check=True)
        # Move outputs to /kaggle/working
        for f in ["word-timestamps.json", "phrases.json", "beat-map.json"]:
            if (Path("data") / f).exists():
                shutil.copy2(Path("data") / f, Path("/kaggle/working") / f)

    elif mode in ["sync_test", "render"]:
        # Install node, remotion deps, fonts
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "nodejs", "npm", "libraqm0", "fonts-noto-cjk"], check=True)
        subprocess.run(["npm", "install"], cwd="video", check=True)
        
        # Run render
        cmd = ["npx", "remotion", "render", f"video/src/index.ts", 
               "MainVideo" if mode == "render" else "SyncTest", 
               task.get("output_name", "output_video.mp4"),
               "--frames", f"{task.get('start_sec')}-{task.get('end_sec')}" if task.get('start_sec') else "full"]
        subprocess.run(cmd, cwd="video", check=True)
        
        # Cleanup
        subprocess.run(["rm", "-rf", "/kaggle/working/auto-video-engine"])

if __name__ == "__main__":
    cloud_runner()
