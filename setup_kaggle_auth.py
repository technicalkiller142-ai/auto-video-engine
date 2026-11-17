import os
import json
import shutil
import webbrowser
import time
from pathlib import Path

def setup_kaggle():
    home = Path.home()
    kaggle_dir = home / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if kaggle_json.exists():
        try:
            with open(kaggle_json, "r") as f:
                data = json.load(f)
                if "username" in data and "key" in data:
                    print("Kaggle API key already exists and is valid.")
                    return True
        except:
            pass

    # Search common locations
    search_dirs = [
        Path(os.environ.get("USERPROFILE", "")) / "Downloads",
        Path(os.environ.get("USERPROFILE", "")) / "Desktop",
        Path(os.environ.get("USERPROFILE", "")) / "Documents",
        Path("D:/VideoAutomationWorkspace")
    ]
    
    found_file = None
    for d in search_dirs:
        if not d.exists(): continue
        for f in d.glob("kaggle*.json"):
            found_file = f
            break
        if found_file: break

    if found_file:
        kaggle_dir.mkdir(exist_ok=True)
        shutil.copy2(found_file, kaggle_json)
        # Set permissions on Windows
        os.chmod(kaggle_json, 0o600)
        print(f"Found and moved {found_file} to {kaggle_json}")
        return True

    # Check env vars
    user = os.environ.get("KAGGLE_USERNAME")
    key = os.environ.get("KAGGLE_KEY")
    if user and key:
        kaggle_dir.mkdir(exist_ok=True)
        with open(kaggle_json, "w") as f:
            json.dump({"username": user, "key": key}, f)
        print(f"Generated kaggle.json from environment variables.")
        return True

    # Last resort: Browser
    print("Kaggle token not found. Opening settings page...")
    webbrowser.open("https://www.kaggle.com/settings")
    
    downloads_dir = Path(os.environ.get("USERPROFILE", "")) / "Downloads"
    print(f"Waiting for kaggle.json in {downloads_dir}...")
    
    start_time = time.time()
    while time.time() - start_time < 120:
        for f in downloads_dir.glob("kaggle*.json"):
            kaggle_dir.mkdir(exist_ok=True)
            shutil.move(str(f), str(kaggle_json))
            print(f"Detected and moved {f.name} to {kaggle_json}")
            return True
        time.sleep(3)
    
    print("Timeout: No kaggle.json found. Please setup manually.")
    return False

if __name__ == "__main__":
    setup_kaggle()
