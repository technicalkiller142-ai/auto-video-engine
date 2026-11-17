import subprocess
import os
import time
from pathlib import Path
import setup_kaggle_auth

def trigger():
    # 1. Setup Auth
    setup_kaggle_auth.setup_kaggle()

    # 2. Git sync
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Auto pipeline update"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

    # 3. Push kernel
    print("Pushing Kaggle kernel...")
    subprocess.run(["kaggle", "kernels", "push", "-p", "./kaggle_kernel"], check=True)

    # 4. Poll status
    while True:
        res = subprocess.run(["kaggle", "kernels", "status", "vinu07/autorenderworker"], capture_output=True, text=True)
        print(res.stdout)
        if "complete" in res.stdout.lower():
            break
        time.sleep(15)

    # 5. Output
    print("Downloading outputs...")
    subprocess.run(["kaggle", "kernels", "output", "vinu07/autorenderworker", "-p", "./data"], check=True)

if __name__ == "__main__":
    trigger()
