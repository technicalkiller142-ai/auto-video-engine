import subprocess
import os
import sys
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

def main():
    # Create output directory if needed
    output_dir = Path("auto-video-engine")
    output_dir.mkdir(exist_ok=True)
    
    # Build Manim command
    script_path = Path(__file__).absolute()
    output_path = output_dir / "output_video"
    
    cmd = [
        sys.executable, "-m", "manim",
        "-p", "-ql", "--leave_progress_bars",
        str(script_path), "PipelineScene",
        "-o",
        "--media_dir", str(output_dir),
        "--output_file_name", "output_video.mp4"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        # Run Manim render
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Manim render completed successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Manim render failed: {e}")
        print(f"Error output: {e.stderr}")
        return 1
    
    # Source and destination paths
    source_video = output_dir / "output_video.mp4"
    dest_video_linux = output_dir / "output_video.mp4"
    dest_video_windows = Path("D:\\VideoAutomationWorkspace\\auto-video-engine\\output_video.mp4")
    
    # Copy video to destination in current working directory (Linux/Kaggle)
    if source_video.exists():
        try:
            import shutil
            shutil.copy2(source_video, dest_video_linux)
            print(f"Video copied to: {dest_video_linux}")
        except Exception as e:
            print(f"Failed to copy to Linux destination: {e}")
    
    # Copy video to Windows destination
    try:
        shutil.copy2(source_video, dest_video_windows)
        print(f"Video copied to Windows destination: {dest_video_windows}")
    except Exception as e:
        print(f"Failed to copy to Windows destination: {e}")
    
    # Clean up temp files
    temp_files = [
        output_dir / "output_video.mp4.json",
        output_dir / "output_video.mp4.tex",
    ]
    
    for temp_file in temp_files:
        if temp_file.exists():
            temp_file.unlink()
            print(f"Cleaned up: {temp_file}")
    
    print("Pipeline completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())