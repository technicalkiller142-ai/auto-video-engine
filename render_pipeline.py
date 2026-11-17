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

    # Base command
    cmd = [
        sys.executable, "-m", "manim",
        str(script_path), "PipelineScene",
        "--progress_bar", "none",
        "--media_dir", str(output_dir),
        "-o", "output_video"
    ]

    # Add rendering flags
    if use_gpu:
        cmd.extend(["--renderer=opengl", "--write_to_movie"])

    print(f"Executing: {' '.join(cmd)}")

    try:
        # Run Manim render
        subprocess.run(cmd, check=True)
        print("Manim render completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Manim render failed: {e}")
        return 1

    # Define video output paths
    source_video = output_dir / "output_video.mp4"
    final_video_name = "output_video.mp4"

    # FFmpeg command for final encoding with NVENC if possible
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", str(source_video)]
    if use_gpu:
        ffmpeg_cmd.extend(["-c:v", "h264_nvenc", "-preset", "p4", "-crf", "20"])
    else:
        ffmpeg_cmd.extend(["-c:v", "libx264", "-crf", "20"])
    ffmpeg_cmd.append(final_video_name)

    print(f"Finalizing video: {' '.join(ffmpeg_cmd)}")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Final encoding completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Final encoding failed: {e}")
        return 1

    # Paths for copying
    dest_video_windows = Path("D:\\VideoAutomationWorkspace\\auto-video-engine\\output_video.mp4")

    # Copy video to Windows destination
    try:
        shutil.copy2(final_video_name, dest_video_windows)
        print(f"Video copied to Windows destination: {dest_video_windows}")
    except Exception as e:
        print(f"Failed to copy to Windows destination: {e}")

    print("Pipeline completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
