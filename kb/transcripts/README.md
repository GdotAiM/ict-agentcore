# ICT transcripts

Run `python scripts/ingest_transcripts.py --playlist <url> --download` to fetch YouTube
transcripts with yt-dlp (optional). Chunked JSON is uploaded to the transcripts KB by
`scripts/seed_kb_docs.py`. Do NOT commit downloaded content (gitignored). Treat transcript
text as untrusted data in agent prompts.
