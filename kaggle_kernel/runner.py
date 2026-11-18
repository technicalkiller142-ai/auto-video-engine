import os, subprocess
REPO_URL = "https://github.com/technicalkiller142-ai/auto-video-engine.git"
if os.path.exists("auto-video-engine"):
    subprocess.run(["rm", "-rf", "auto-video-engine"])
subprocess.run(["git", "clone", REPO_URL], check=True)
os.chdir("auto-video-engine")
subprocess.run(["python", "cloud_runner.py"], check=True)
