# 6-Stage Director Protocol

Follow this protocol end-to-end whenever a new `input/song.mp3` and `input/lyrics.txt` are provided.

## Stage 0-1: Alignment
- Set `pipeline_task.json` to `{"mode": "align"}`.
- Create an empty file named `.run_kaggle` in the root.
- Wait for Windows watcher to generate `data/word-timestamps.json`, `data/phrases.json`, and `data/beat-map.json`.

## Stage 2: Sync Test
- Set `pipeline_task.json` to `{"mode": "sync_test"}`.
- Create an empty file named `.run_kaggle`.
- Retrieve `data/sync-test.mp4` locally for verification.

## Stage 3: Creative Direction & Screenplay
- Analyze lyrics (Hindi/Hinglish/English) and beat-map.
- Author `data/creative-direction.md` and `data/visual-screenplay.json`.
- Focus on motivated transitions and semantic visual metaphors.

## Stage 4-5: Sequence Coding & Hero Proof
- Code custom Remotion sequences in `video/src/sequences/`.
- Render a 5-15s `"hero-proof"` clip by setting `pipeline_task.json` mode `"render"` and creating `.run_kaggle`.

## Stage 6: Full Render
- Once approved, render the full song locally by triggering the pipeline with `mode: "render"` and no frame limits via `.run_kaggle`.

---
## Workspace Rules
1. Never touch GitHub or Kaggle manually; use `trigger_kaggle.py`.
2. All scripts must be self-contained and list requirements on line 1.
3. Keep visual elements inside the safe frame (1080x1920).
4. Use standard fonts for Devanagari to ensure no breaking.
5. **No Network Access in Sandbox**: Because this environment has no outbound network access, whenever a pipeline stage (`align`, `sync_test`, or `render`) is ready to execute on Kaggle, update `pipeline_task.json` and create an empty trigger file `.run_kaggle` in the repo root. The Windows background watcher (`auto_push.bat` -> `windows_bootstrap_and_run.py`) will immediately detect `.run_kaggle`, install/verify Kaggle CLI, push the kernel, run the GPU job, and download the output automatically.
