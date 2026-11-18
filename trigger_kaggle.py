import subprocess
import os
import time
import json
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

def trigger():
    start_time = time.time()

    # 1. Setup Auth
    setup_kaggle_auth.setup_kaggle()

    # 2. Git sync
    update_status("pushing_git", "Pushing to GitHub...", "Alignment")
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto pipeline update"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

    # 3. Push kernel
    update_status("pushing_kaggle", "Pushing Kaggle kernel...", "Alignment")
    print("[KAGGLE] Pushing kernel to vinu07/autorenderworker...")
    subprocess.run(["kaggle", "kernels", "push", "-p", "./kaggle_kernel"], check=True)

    # 4. Poll status
    start_poll = time.time()
    while True:
        elapsed = int(time.time() - start_poll)
        update_status("running_gpu", f"Status: running... ({elapsed}s elapsed)", "Alignment")
        print(f"[KAGGLE] Status: running... ({elapsed}s elapsed)")

        res = subprocess.run(["kaggle", "kernels", "status", "vinu07/autorenderworker"], capture_output=True, text=True)
        if "complete" in res.stdout.lower():
            break
        if "error" in res.stdout.lower():
            update_status("error", "Kaggle execution failed.", "Alignment")
            print(f"[KAGGLE] Error: {res.stdout}")
            return
        time.sleep(15)

    # 5. Output
    update_status("downloading", "Downloading outputs...", "Alignment")
    print("Downloading outputs...")
    subprocess.run(["kaggle", "kernels", "output", "vinu07/autorenderworker", "-p", "./data"], check=True)

    # Move files
    for f in Path("./data").glob("*"):
        if f.suffix == ".json":
            shutil.copy2(f, REPO_DIR / "data" / f.name)
        elif f.suffix == ".mp4":
            shutil.copy2(f, REPO_DIR / f.name)

    update_status("complete", "Files downloaded locally!", "Alignment")
    print("[DONE] Files downloaded locally!")

if __name__ == "__main__":
    trigger()
