import os, subprocess
REPO_URL = "https://github.com/technicalkiller142-ai/auto-video-engine.git"
# Always clean up before cloning
if os.path.exists("auto-video-engine"):
    subprocess.run(["rm", "-rf", "auto-video-engine"])
    
subprocess.run(["git", "clone", REPO_URL], check=True)

# The cloned repo is now at /kaggle/working/auto-video-engine
# cloud_runner.py is inside /kaggle/working/auto-video-engine/cloud_runner.py
# So we need to cd into that directory to run cloud_runner.py

os.chdir("auto-video-engine")
print(f"DEBUG: Working in: {os.getcwd()}")
print(f"DEBUG: Contents: {os.listdir('.')}")

# Now run cloud_runner.py which expects to be in the repo root
subprocess.run(["python", "cloud_runner.py"], check=True)
