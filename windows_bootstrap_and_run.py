import os
import sys
import subprocess
import shutil
import setup_kaggle_auth
from pathlib import Path

def bootstrap_and_run():
    # 1. Check/Install Kaggle CLI
    if not shutil.which("kaggle"):
        print("Installing kaggle CLI...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kaggle"], check=True)
    else:
        print("Kaggle CLI already installed.")

    # 2. Setup Auth
    setup_kaggle_auth.setup_kaggle()

    # 3. Check for trigger or deploy flag
    trigger_file = Path(".run_kaggle")
    if trigger_file.exists():
        print("Trigger detected, running pipeline...")
        os.remove(trigger_file)
        subprocess.run([sys.executable, "trigger_kaggle.py"], check=True)

if __name__ == "__main__":
    bootstrap_and_run()
