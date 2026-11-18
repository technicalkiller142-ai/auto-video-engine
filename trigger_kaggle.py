import subprocess
import os
import time
import json
import shutil
import sys
from pathlib import Path
import setup_kaggle_auth

REPO_DIR = Path(r"D:\VideoAutomationWorkspace\auto-video-engine")
os.chdir(REPO_DIR)

def update_status(status, message, stage="Alignment", error_log=""):
    status_file = REPO_DIR / "live_status.json"
    data = {
        "stage": stage,
        "status": status,
        "message": message,
        "error_log": error_log,
        "elapsed_sec": int(time.time() - getattr(update_status, 'start_time', time.time())),
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(status_file, "w") as f:
        json.dump(data, f)

def trigger():
    update_status.start_time = time.time()

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

    result = subprocess.run([sys.executable, "-m", "kaggle.cli", "kernels", "push", "-p", "./kaggle_kernel"], capture_output=True, text=True)

    if result.returncode != 0:
        error_msg = f"Kaggle push failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        update_status("error", error_msg, "Alignment", error_log=error_msg)
        print(f"[KAGGLE] {error_msg}")
        return

    # 4. Poll status
    start_poll = time.time()
    final_status = None
    while True:
        elapsed = int(time.time() - start_poll)
        update_status("running_gpu", f"Status: running... ({elapsed}s elapsed)", "Alignment")
        print(f"[KAGGLE] Status: running... ({elapsed}s elapsed)")

        res = subprocess.run([sys.executable, "-m", "kaggle.cli", "kernels", "status", "vinu07/autorenderworker"], capture_output=True, text=True)
        if "complete" in res.stdout.lower():
            final_status = "complete"
            break
        if "error" in res.stdout.lower():
            final_status = "error"
            break
        time.sleep(15)

    # 5. ALWAYS download outputs (both complete and error)
    update_status("downloading", f"Downloading outputs... (status: {final_status})", "Alignment")
    print("Downloading outputs...")

    out_result = subprocess.run([sys.executable, "-m", "kaggle.cli", "kernels", "output", "vinu07/autorenderworker", "-p", "./kaggle_out"], capture_output=True, text=True)
    if out_result.returncode != 0:
        print(f"Warning: output download partially failed: {out_result.stderr}")

    # Move files from kaggle_out to data/ and output/
    kaggle_out = REPO_DIR / "kaggle_out"
    data_dir = REPO_DIR / "data"
    output_dir = REPO_DIR / "output"
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    if kaggle_out.exists():
        for f in kaggle_out.glob("*"):
            if f.suffix == ".json":
                shutil.copy2(f, data_dir / f.name)
                print(f"Copied {f.name} to data/")
            elif f.suffix == ".mp4":
                shutil.copy2(f, output_dir / f.name)
                shutil.copy2(f, REPO_DIR / f.name)
                print(f"Copied {f.name} to output/ and root")

        # Handle Kaggle error report if present
        err_report = kaggle_out / "kaggle_error_report.json"
        if err_report.exists():
            err_text = err_report.read_text()
            update_status("error", f"Kaggle job reported error: {err_text}", "Alignment", error_log=err_text)
            print(f"[KAGGLE ERROR REPORT] {err_text}")
            return

    if final_status == "error":
        update_status("error", f"Kaggle execution failed: {final_status}", "Alignment", error_log=f"Kernel status: {final_status}. See kaggle_out/ for logs.")
        print("[KAGGLE] Job failed. Logs downloaded to kaggle_out/.")
        return

    update_status("complete", "Files downloaded locally!", "Alignment")
    print("[DONE] Files downloaded locally!")

if __name__ == "__main__":
    trigger()
