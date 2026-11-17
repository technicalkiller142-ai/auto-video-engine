# Auto Video Engine Pipeline

This repository contains an automated video generation pipeline using Manim to create professional animations for video content creation.

## Overview

The pipeline automatically generates a 5-second 1080p 60fps animation that smoothly transforms a glowing blue circle into a red square with the title "Auto Video Pipeline Ready!". The rendered MP4 video is saved both in the script's execution directory and to the main workspace for easy access.

## Files

### `render_pipeline.py`
Main script that:
- Sets up Manim configuration (1920x1080, 60fps)
- Creates a scene with a title text
- Animates transformation from blue circle to red square
- Automatically renders using subprocess
- Copies the output video to multiple locations
- Cleans up temporary files

### `README.md`
This documentation file

## How to Use

1. **Install dependencies**:
   ```bash
   pip install manim numpy
   ```

2. **Run the pipeline**:
   ```bash
   python render_pipeline.py
   ```

The script will:
- Execute the Manim rendering
- Save `output_video.mp4` in the current directory (for Linux/Kaggle)
- Copy `output_video.mp4` to `D:\VideoAutomationWorkspace\auto-video-engine\` (Windows)
- Clean up any temporary files

## Dependencies

- **Manim** (community edition) - For creating animations
- **Python 3.x** - Runtime environment
- **subprocess** - For executing Manim commands
- **pathlib/shutil** - For file management

## Output

The pipeline generates:
- `output_video.mp4` - The final animated video (5 seconds, 1080p, 60fps)
- Cleaned up temporary files (JSON, TEX)

## Notes

- The script is cross-platform and works on both Linux/Kaggle and Windows
- All file paths are relative to the script location
- The transformation animation uses smooth Manim transitions
- The script includes automatic cleanup of temporary files