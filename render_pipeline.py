import subprocess
import os
import sys
import shutil
from pathlib import Path
from manim import *

# Set up Manim configuration
config.pixel_width = 1920  # 1080p
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = WHITE

class PipelineScene(Scene):
    def construct(self):
        # Title text
        title = Text("Auto Video Pipeline Ready!", font_size=48, color=BLUE_D).to_edge(UP)
        self.play(Write(title))

        # Create initial glowing blue circle
        circle = Circle(radius=1, color=BLUE, stroke_width=3).set_glow(
            glow_intensity=0.8, glow_radius=0.2
        )

        # Create target red square
        square = Square(side_length=1.5, color=RED, stroke_width=3).next_to(circle, RIGHT)

        # Animation: Transform circle to square
        self.play(
            Transform(circle, square),
            circle.animate.set_color(RED),
            run_time=5
        )

        # Add glow to square
        square.set_glow(glow_intensity=0.8, glow_radius=0.2)

        # Keep final scene for 1 second
        self.wait(1)

def check_gpu():
    """Checks if NVIDIA GPU is available."""
    try:
        subprocess.run(["nvidia-smi"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    # Create output directory
    output_dir = Path("auto-video-engine")
    output_dir.mkdir(exist_ok=True)

    # Check for GPU
    use_gpu = check_gpu()
    print(f"GPU available: {use_gpu}")

    # Build Manim command
    script_path = Path(__file__).absolute()

    # Standard high-quality render command compatible with headless Linux
    cmd = [
        sys.executable, "-m", "manim",
        "-qh",  # High quality
        str(script_path), "PipelineScene",
        "--progress_bar", "none",
        "--media_dir", str(output_dir),
        "-o", "raw_render"
    ]

    print(f"Executing: {' '.join(cmd)}")

    try:
        # Run Manim render
        subprocess.run(cmd, check=True)
        print("Manim render completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Manim render failed: {e}")
        return 1

    # Find the actual output file (Manim puts it in a nested directory structure)
    # Default path: media/videos/render_pipeline/1080p60/raw_render.mp4
    # But since we set media_dir, it will be relative to that.
    rendered_file = None
    for path in output_dir.rglob("raw_render.mp4"):
        rendered_file = path
        break

    if not rendered_file or not rendered_file.exists():
        print("Could not locate the rendered file.")
        return 1

    final_video_name = "output_video.mp4"

    # FFmpeg command for final encoding with NVENC if possible
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", str(rendered_file)]
    if use_gpu:
        print("Applying NVIDIA GPU acceleration for final encoding...")
        ffmpeg_cmd.extend(["-c:v", "h264_nvenc", "-preset", "p4", "-tune", "hq", "-b:v", "5M"])
    else:
        print("Using software encoding (libx264)...")
        ffmpeg_cmd.extend(["-c:v", "libx264", "-crf", "18", "-preset", "slow"])

    ffmpeg_cmd.append(final_video_name)

    print(f"Finalizing video: {' '.join(ffmpeg_cmd)}")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Final encoding completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Final encoding failed: {e}")
        return 1

    # Paths for copying to Windows
    dest_video_windows = Path("D:\\VideoAutomationWorkspace\\auto-video-engine\\output_video.mp4")

    # Copy video to Windows destination if on Windows
    try:
        shutil.copy2(final_video_name, dest_video_windows)
        print(f"Video copied to Windows destination: {dest_video_windows}")
    except Exception as e:
        # Expected to fail on Linux if path doesn't exist
        pass

    print("Pipeline completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
