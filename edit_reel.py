#!/usr/bin/env python3
"""Simple, reusable FFmpeg vertical-reel editor.
Requires FFmpeg/ffprobe on PATH; no Python dependencies.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

def run(cmd):
    print("+", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)

def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(path)], capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)

def main():
    parser = argparse.ArgumentParser(description="Make a 9:16 vertical Reel from existing footage.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/reel.mp4"))
    parser.add_argument("--start", type=float, default=0)
    parser.add_argument("--duration", type=float, default=30)
    parser.add_argument("--captions", type=Path, help="Optional subtitle file (.srt)")
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("Install FFmpeg and ffprobe first.")
    if not args.source.is_file():
        parser.error(f"Input video not found: {args.source}")
    if args.start < 0 or args.duration <= 0:
        parser.error("Start must be nonnegative and duration must be positive.")
    info = probe(args.source)
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    # Crop to portrait, center horizontally; improve contrast subtly.
    vf = [
        "scale=1080:1920:force_original_aspect_ratio=increase",
        "crop=1080:1920",
        "eq=contrast=1.06:saturation=1.08",
        f"fps={args.fps}",
        "format=yuv420p"
    ]
    if args.captions:
        if not args.captions.is_file():
            parser.error(f"Captions not found: {args.captions}")
        # FFmpeg subtitles filter uses libass. Resolve path and escape common special characters.
        sub = str(args.captions.resolve()).replace("\\", "/")
        sub = sub.replace(":", r"\:").replace("'", r"\'").replace("[", r"\[").replace("]", r"\]")
        vf.insert(-1, f"subtitles=filename='{sub}'")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-ss", str(args.start), "-i", str(args.source),
        "-t", str(args.duration), "-vf", ",".join(vf),
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-movflags", "+faststart"
    ]
    if has_audio:
        cmd.extend(["-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-c:a", "aac", "-b:a", "192k"])
    else:
        cmd.extend(["-an"])
    cmd.append(str(args.output))
    run(cmd)
    print("Finished:", args.output.resolve())

if __name__ == "__main__":
    main()
