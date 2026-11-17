@echo off
cd /d "D:\VideoAutomationWorkspace\auto-video-engine"

:loop
echo Checking for changes...

:: Check for changes, excluding __pycache__ and *.mp4 files.
:: We list changed files, filter out excluded patterns, and count the result.
git status --porcelain | findstr /V "__pycache__ \.mp4$" > nul
if %errorlevel% equ 0 (
    echo Changes detected!
    git add .
    git commit -m "Auto-update video pipeline"
    git push origin main
) else (
    echo No relevant changes detected.
)

timeout /t 5 > nul
goto loop
