# 6-Stage Director Protocol

Follow this protocol end-to-end whenever a new `input/song.mp3` and `input/lyrics.txt` are provided.

## Stage 0-1: Alignment
- Set `pipeline_task.json` to `{"mode": "align"}`.
- Run `python trigger_kaggle.py`.
- Verify `data/word-timestamps.json`, `data/phrases.json`, and `data/beat-map.json` are downloaded.

## Stage 2: Sync Test
- Set `pipeline_task.json` to `{"mode": "sync_test"}`.
- Run `python trigger_kaggle.py`.
- Deliver `data/sync-test.mp4` locally for verification.

## Stage 3: Creative Direction & Screenplay
- Analyze lyrics (Hindi/Hinglish/English) and beat-map.
- Author `data/creative-direction.md` and `data/visual-screenplay.json`.
- Focus on motivated transitions and semantic visual metaphors.

## Stage 4-5: Sequence Coding & Hero Proof
- Code custom Remotion sequences in `video/src/sequences/`.
- Render a 5-15s `"hero-proof"` clip via `trigger_kaggle.py` with `pipeline_task.json` mode `"render"`.

## Stage 6: Full Render
- Once approved, render the full song into `output_video.mp4` locally by triggering the pipeline with `mode: "render"` and no frame limits.

---
## Workspace Rules
1. Never touch GitHub or Kaggle manually; use `trigger_kaggle.py`.
2. All scripts must be self-contained and list requirements on line 1.
3. Keep visual elements inside the safe frame (1080x1920).
4. Use standard fonts for Devanagari to ensure no breaking.
