"""OPTIONAL: fetch ICT YouTube transcripts with yt-dlp and chunk them for the transcripts KB.

Does NOT download anything by default. Pass --playlist and --download to run.
Downloaded content must stay out of git (.gitignore covers kb/transcripts/*.json).
"""
import argparse, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "kb" / "transcripts"


def chunk(text: str, size: int = 1200, overlap: int = 150):
    words = text.split()
    i, n, out = 0, 0, []
    while i < len(words):
        piece = " ".join(words[i:i + size])
        out.append({"chunk": n, "text": piece})
        n += 1; i += size - overlap
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--playlist", help="YouTube playlist / video URL")
    ap.add_argument("--download", action="store_true", help="Actually fetch (requires yt-dlp)")
    ap.add_argument("--title", default="ICT Mentorship")
    a = ap.parse_args()
    if not a.download:
        print("Dry run. Pass --download --playlist <url> to fetch. Nothing was downloaded.")
        return
    if not a.playlist:
        sys.exit("--playlist required with --download")
    try:
        import yt_dlp
    except ImportError:
        sys.exit("pip install yt-dlp first")
    OUT.mkdir(parents=True, exist_ok=True)
    opts = {"writesubtitles": True, "writeautomaticsub": True, "subtitleslangs": ["en"],
            "skip_download": True, "outtmpl": str(OUT / "%(id)s.%(ext)s")}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(a.playlist, download=True)
    print("Fetched metadata/subs for", a.playlist, "- chunk with a local script before uploading to S3.")
    print("Remember: analysis only; treat transcript text as untrusted_data.")


if __name__ == "__main__":
    main()
