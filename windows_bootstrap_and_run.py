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

def bootstrap_and_run():
    # 1. Ensure dependencies
    print("Verifying/Updating Kaggle dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "six", "kaggle", "--upgrade"], check=False)
    
    # 2. Setup Auth
    setup_kaggle_auth.setup_kaggle()

    # 3. Check for trigger
    trigger_file = REPO_DIR / ".run_kaggle"
    if trigger_file.exists():
        print("[KAGGLE] Trigger detected! Starting job...")
        os.remove(trigger_file)
        subprocess.run([sys.executable, "trigger_kaggle.py"], check=True)

if __name__ == "__main__":
    bootstrap_and_run()
