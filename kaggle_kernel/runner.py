import os, subprocess
REPO_URL = "https://github.com/technicalkiller142-ai/auto-video-engine.git"
# Fix for Kaggle: clone directly into current directory
if os.path.exists("auto-video-engine"):
    subprocess.run(["rm", "-rf", "auto-video-engine"])
subprocess.run(["git", "clone", REPO_URL], check=True)
# The cloned repo is in /kaggle/working/auto-video-engine
# Let's list the directory content to be absolutely sure where we are and what was cloned
print(f"DEBUG: Current directory: {os.getcwd()}")
print(f"DEBUG: Contents of /kaggle/working/: {os.listdir('/kaggle/working/')}")
# We might need to adjust the directory structure. 
# If it's already in /kaggle/working/auto-video-engine, cd to it.
if os.path.exists("auto-video-engine"):
    os.chdir("auto-video-engine")
    print(f"DEBUG: Switched to: {os.getcwd()}")
    print(f"DEBUG: Contents of current: {os.listdir('.')}")
else:
    print(f"DEBUG: Contents of current: {os.listdir('.')}")

subprocess.run(["python", "cloud_runner.py"], check=True)
