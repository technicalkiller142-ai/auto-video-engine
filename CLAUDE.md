# Workspace Rules

These are the strict instructions for all future tasks in this workspace:

1. **Manim CLI Flags**: Never use deprecated Manim flags like `--leave_progress_bars`, `--write_to_movie`, or `--renderer=opengl` in subprocess commands. Always use clean standard CLI flags: `python -m manim -qh render_pipeline.py -a --progress_bar none`.
2. **Self-Contained Scripts**: Every script must be 100% self-contained. List any extra pip packages needed at the top in a comment `# REQUIREMENTS: pkg1 pkg2` so the cloud runner installs them automatically.
3. **Output Requirements**: Always ensure the final rendered video is copied/saved directly as `output_video.mp4` in the root of the repository folder.
4. **Clean Implementation**: Keep `render_pipeline.py` strictly focused on clean Manim `Scene` classes so it works identically on Windows and headless Linux (Kaggle).
5. **Valid APIs**: Never invent non-existent Manim methods like `.set_glow()`; use only valid Manim Community Edition v0.18+ APIs.
