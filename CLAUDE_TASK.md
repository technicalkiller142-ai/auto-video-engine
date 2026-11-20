# AUTOPILOT TASK FOR CLAUDE

You are on full creative and technical autopilot for D:/VideoAutomationWorkspace/auto-video-engine. Do NOT ask me for creative choices, edits, or approvals.

## 1. Fix & Verify Stage 2 (sync_test)
- Check data/kaggle_error_report.json and cloud_runner.py.
- Ensure video_dir points to the video/ subfolder (where package.json lives) and Linux Chrome deps (libatk1.0-0 etc.) are installed on Kaggle.
- Trigger sync_test via .run_kaggle and confirm data/sync-test.mp4 succeeds.

## 2. Design & Code Custom Motion Graphics (using .claude/skills/remotion-skills)
- Read input/lyrics.txt, data/beat-map.json, data/phrases.json, and data/word-timestamps.json.
- Design a cohesive, high-energy 1080x1920 (9:16) visual theme matching the song mood and write data/creative-direction.md.
- Upgrade video/src/MainVideo.tsx (and modular components in video/src/sequences/) with beat-synced kinetic typography, spring animations, audio-reactive visualizers, custom SVG/canvas motion elements, and strict 9:16 Reels safe-zone margins.

## 3. Render Hero Proof & Full Song via auto_push.bat
1. Trigger hero-proof.mp4 (mode=render, composition=MainVideo, frames=0-300, output=hero-proof.mp4 + .run_kaggle), verify it succeeds, and auto-fix any build/render issues.
2. Trigger full render (mode=render, composition=MainVideo, output=final-video.mp4 + .run_kaggle).
3. Notify me ONLY when data/final-video.mp4 is ready to watch. Keep all chat messages under 6 lines.