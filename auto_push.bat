@echo off
cd /d "D:\VideoAutomationWorkspace\auto-video-engine"

:loop
echo [%TIME%] Checking for changes...

:: Check for changes without filtering
git status --porcelain > nul
if %errorlevel% equ 0 (
    echo [%TIME%] No relevant changes detected.
) else (
    echo [%TIME%] [GIT] Pushing...
    git add -A
    git commit -m "Auto-update video pipeline"
    git push origin main
)

:: Run the Windows-side bridge (checks for .run_kaggle automatically)
echo [%TIME%] [KAGGLE] Checking for trigger...
python windows_bootstrap_and_run.py

timeout /t 5 > nul
goto loop
