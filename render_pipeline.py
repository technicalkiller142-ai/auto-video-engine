# REQUIREMENTS: manim

from manim import *

# Set up Manim configuration
config.pixel_width = 1920  # 1080p
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = WHITE
config.frame_width = 14.2
config.frame_height = 8.0

class PipelineScene(Scene):
    def construct(self):
        # Title text
        title = Text("Auto Video Pipeline Ready!", font_size=48, color=BLUE_D).to_edge(UP)
        self.play(Write(title))

        # Create initial blue circle
        circle = Circle(radius=1, color=BLUE, stroke_width=6)
        circle.set_fill(BLUE, opacity=0.3)

        # Create target red square
        square = Square(side_length=1.5, color=RED, stroke_width=6)
        square.set_fill(RED, opacity=0.3)
        square.next_to(circle, RIGHT)

        # Animation: Create then Transform
        self.play(Create(circle))
        self.play(
            Transform(circle, square),
            run_time=5
        )

        # Keep final scene
        self.wait(2)
        self.play(FadeOut(circle), FadeOut(title))
