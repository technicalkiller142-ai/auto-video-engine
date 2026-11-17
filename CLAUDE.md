# Workspace Rules

These are the strict, unbreakable rules for all future video tasks in this workspace:

1. **Clean Code**: `render_pipeline.py` must ONLY contain valid Python and Manim CE v0.18+ `Scene` classes. Never include `subprocess` CLI runners or deprecated flags (like `--leave_progress_bars`, `--write_to_movie`, or `--renderer=opengl`).
2. **Valid APIs**: Never invent non-existent methods like `.set_glow()`, `.add_glow()`, or use deprecated `ShowCreation`. Always use standard, valid methods like `Create`.
3. **Safe Framing**: Keep all visual elements strictly inside the safe camera frame (`config.frame_width = 14.2`, `config.frame_height = 8.0`) so nothing ever clips off-screen.
4. **Standard Text**: Always use `Text(...)` with standard fonts instead of `Tex`/`MathTex` unless explicitly requested, to avoid LaTeX compilation crashes.
5. **Requirements Tracking**: If any extra Python package is imported, list it on line 1 as `# REQUIREMENTS: pkg1 pkg2`.
