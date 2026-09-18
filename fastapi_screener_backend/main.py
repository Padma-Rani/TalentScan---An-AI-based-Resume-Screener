"""
main.py

CLI entry point demonstrating the complete AI Resume Screening
pipeline end-to-end.

Usage:
    python main.py --resume "path/to/resume.pdf" --job "path/to/job.txt"
    python main.py --resume "path/to/resume.pdf" --job-text "Job description text..."

If no arguments are given, you will be prompted interactively.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from app.screening.screening_engine import ScreeningEngine


def _read_job_text(job_path: str | None, job_text: str | None) -> str:
    if job_text:
        return job_text
    if job_path:
        path = Path(job_path)
        if not path.exists():
            print(f"[ERROR] Job description file not found: {job_path}")
            sys.exit(1)
        return path.read_text(encoding="utf-8", errors="ignore")
    print("[ERROR] Provide either --job (file path) or --job-text (raw text).")
    sys.exit(1)


def _interactive() -> tuple[str, str]:
    resume_path = input("Path to resume file (PDF/JPG/JPEG/PNG): ").strip()
    print(
        "Paste the job description, then press Enter followed by Ctrl+Z "
        "then Enter (Windows) to finish:"
    )
    job_text = sys.stdin.read()
    return resume_path, job_text


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Resume Screening System")
    parser.add_argument("--resume", help="Path to resume file (PDF/JPG/JPEG/PNG)")
    parser.add_argument("--job", help="Path to a job description text file")
    parser.add_argument("--job-text", help="Job description text, inline")
    args = parser.parse_args()

    if args.resume:
        resume_path = args.resume
        job_text = _read_job_text(args.job, args.job_text)
    else:
        resume_path, job_text = _interactive()

    print("\nInitializing AI Resume Screening System...")
    engine = ScreeningEngine()

    result = engine.screen_resume_file(resume_path, job_text)

    print("\n" + "=" * 60)
    print("SCREENING RESULT")
    print("=" * 60)
    print(json.dumps(result, indent=2, default=str))

    if result.get("error"):
        return 1

    print("\n" + "-" * 60)
    print(f"Final Score: {result['final_score']}")
    print(f"Recommendation: {result['recommendation']}")
    print("-" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
