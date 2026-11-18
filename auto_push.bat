@echo off
cd /d "D:\VideoAutomationWorkspace\auto-video-engine"

:loop
echo Checking for changes...

:: Check for changes, excluding __pycache__ and *.mp4 files.
git status --porcelain | findstr /V "__pycache__ \.mp4$" > nul
if %errorlevel% equ 0 (
    echo Changes detected!
    git add .
    git commit -m "Auto-update video pipeline"
    git push origin main

    :: Run the Windows-side bridge
    python windows_bootstrap_and_run.py
) else (
    echo No relevant changes detected.
    :: Still run the bridge to check for .run_kaggle trigger
    python windows_bootstrap_and_run.py
)

timeout /t 5 > nul
goto loop
