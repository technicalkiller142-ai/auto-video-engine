import os
import sys
import subprocess
import shutil
import json
import time
from pathlib import Path
import setup_kaggle_auth

REPO_DIR = Path(r"D:\VideoAutomationWorkspace\auto-video-engine")
os.chdir(REPO_DIR)

def update_status(status, message, stage="Alignment"):
    status_file = REPO_DIR / "live_status.json"
    data = {
        "stage": stage,
        "status": status,
        "message": message,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(status_file, "w") as f:
        json.dump(data, f)

def bootstrap_and_run():
    # 1. Check/Install Kaggle CLI
    if not shutil.which("kaggle"):
        print("Installing kaggle CLI...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kaggle"], check=True)

    # 2. Setup Auth
    setup_kaggle_auth.setup_kaggle()

    # 3. Check for trigger
    trigger_file = REPO_DIR / ".run_kaggle"
    if trigger_file.exists():
        print("[KAGGLE] Trigger detected! Starting job...")
        update_status("running", "Trigger detected! Starting job...")
        os.remove(trigger_file)
        subprocess.run([sys.executable, "trigger_kaggle.py"], check=True)

if __name__ == "__main__":
    bootstrap_and_run()
