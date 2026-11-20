import os, subprocess
REPO_URL = "https://github.com/technicalkiller142-ai/auto-video-engine.git"
if os.path.exists("auto-video-engine"):
    subprocess.run(["rm", "-rf", "auto-video-engine"])
subprocess.run(["git", "clone", REPO_URL], check=True)
# The cloned repo is in /kaggle/working/auto-video-engine
# Let's list the directory content to be absolutely sure where we are and what was cloned
print(f"DEBUG: Current directory: {os.getcwd()}")
print(f"DEBUG: Contents of /kaggle/working/: {os.listdir('/kaggle/working/')}")
os.chdir("auto-video-engine")
subprocess.run(["python", "cloud_runner.py"], check=True)
