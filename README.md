# Codex + FFmpeg Reel Editor

A minimal starting point for making vertical Reels from existing footage with Codex.

## Quick start

1. Install FFmpeg so `ffmpeg -version` and `ffprobe -version` work.
2. Put your source video in `input/` (do not commit private/source footage to GitHub).
3. Run:

```bash
python scripts/edit_reel.py input/source.mp4 --start 0 --duration 25 --output output/reel.mp4
```

Optional burned subtitles (prepare a timed `.srt` file first):

```bash
python scripts/edit_reel.py input/source.mp4 --duration 25 --captions input/captions.srt --output output/reel.mp4
```

Output: 1080 × 1920, 30 fps H.264 MP4, AAC audio when source audio exists. It uses a center crop, so subjects near the edges may be cut off. On some builds the `subtitles` filter requires FFmpeg compiled with `libass`.

This is a reliable **base edit**, not an advanced cinematic motion-graphics package yet. Ask Codex to extend it with beat cuts, speaker tracking, animated ASS captions, overlays, transitions, SFX, and tests after confirming a successful basic render.

## Codex environment

Repo: `demandtab/gpt` (or your chosen repository). Upload these source files using GitHub **Add file → Upload files**. Never upload `input/` or `output/` footage to a public repository.

On Codex Cloud, ask it to verify `ffmpeg` and `ffprobe`. If absent, configure an installation step on a Debian/Ubuntu environment:

```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

Then test `ffmpeg -version && ffprobe -version`, review changes, and publish once. Install scripts must be supported by your environment permissions.

## Working with larger private videos

Use Codex locally with your footage and this repository, or securely stage footage in the cloud task workspace. A GitHub repo alone does not give Codex access to files on your PC. Do not rely on GitHub for storing large footage and exports.

## Sample task to give Codex

> Edit the existing footage in input/source.mp4 as a premium 9:16 Reel. Start by verifying the source duration, audio, and the baseline pipeline. Keep dialogue and speaker identity unchanged. Add a hook-first structure, dynamic animated captions, scene-specific motion graphics, sound effects, tasteful punch-ins and transitions. Create a detailed timeline, implement changes with FFmpeg, render output/reel.mp4, inspect the result, and report any effects you could not complete. Do not replace the original footage with generated visuals without asking.
