# AI Resume Screener

A modular, AI-driven resume screening system that dynamically extracts
structured information from resumes and job descriptions using local,
open-source language models, compares a candidate against a job, and
produces an explainable match score — with no hardcoded skill
database.

## Features

- **Automatic file handling** — accepts PDF, JPG, JPEG, and PNG resumes.
  Text-layer PDFs are parsed directly; scanned PDFs and images are OCR'd
  automatically. You never have to say which type a file is.
- **Genuinely dynamic technology extraction** — an LLM reads each resume
  and job description and reports the technologies it actually finds.
  New job stacks (e.g. Go/gRPC, Rust/Actix) are handled with zero code
  changes.
- **Layered, false-positive-resistant skill matching** — exact match →
  alias match → conservative semantic match. "Spring Boot" will not be
  treated as a match for "Java".
- **Intelligent qualification matching** — experience is compared in
  months; education uses semantic similarity, so "BS Computer Science,
  University of Georgia" satisfies "Bachelor's degree in Computer
  Science or a related field" without an exact string match.
- **Explainable results** — every score comes with matched/missing
  skills, experience and education evidence, and a plain-language
  recommendation, all traceable back to extracted resume content.
- **Shared model loading** — the LLM and embedding model are loaded
  once per process via a singleton `ModelManager` and reused everywhere.

## Architecture

```
AI_RESUME_SCREENER_FINAL/
├── app/
│   ├── ai/
│   │   ├── model_manager.py       # Loads & shares the LLM + embedding model
│   │   ├── resume_analyzer.py     # Resume text -> structured JSON (AI)
│   │   └── job_analyzer.py        # Job text -> structured requirements (AI)
│   ├── extraction/
│   │   └── resume_parser.py       # PDF/image -> plain text (auto OCR)
│   ├── matching/
│   │   └── matcher.py             # DynamicAIMatcher: skill matching
│   ├── qualification/
│   │   ├── qualification_matcher.py   # Experience + education matching
│   │   └── experience_calculator.py   # Deterministic date math -> months
│   ├── screening/
│   │   └── screening_engine.py    # Orchestrates the full pipeline
│   └── core/
│       ├── config.py              # All model names / weights / thresholds
│       ├── json_utils.py          # Robust LLM JSON extraction
│       └── similarity.py          # Shared cosine-similarity function
├── data/
│   ├── resumes/
│   └── job_descriptions/
├── tests/                         # One test module per pipeline stage
├── main.py                        # CLI entry point
├── requirements.txt
└── .gitignore
```

**Pipeline:**

```
Resume File → ResumeParser → Resume Text
Resume Text → ResumeAnalyzer (LLM) → Structured Resume
Job Description → JobDescriptionAnalyzer (LLM) → Structured Requirements
Structured Resume + Requirements → DynamicAIMatcher → Skill Matches
Structured Resume + Requirements → QualificationMatcher → Qualification Result
All of the above → ScreeningEngine → Final Explainable Result
```

## AI models used

| Purpose | Model | Why |
|---|---|---|
| Resume & job description analysis | `Qwen/Qwen2.5-1.5B-Instruct` | Small enough to run on CPU, strong instruction-following, current `transformers` chat-template support. |
| Skill / education semantic matching | `sentence-transformers/all-MiniLM-L6-v2` | Fast, accurate for short technology-name embeddings. |

Both are loaded exactly once per process through `app/ai/model_manager.py`.
If Phase-4/5 testing shows extraction quality needs improvement on messy
or OCR'd text, `Qwen2.5-3B-Instruct` is a drop-in upgrade (same tokenizer
family) — swap the name in `app/core/config.py` only.

## Technologies used

Python 3.13, PyTorch, Hugging Face Transformers, Sentence-Transformers,
PyMuPDF, Pillow, pytesseract + Tesseract OCR, python-dateutil, pydantic.

## Supported resume formats

PDF (text-layer or scanned), JPG, JPEG, PNG.

## Installation

### 1. Virtual environment (PowerShell)

```powershell
cd AI_RESUME_SCREENER_FINAL
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
where.exe python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

In VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → choose
`.venv\Scripts\python.exe`.

### 2. Tesseract OCR setup (Windows)

1. Download the installer from
   https://github.com/UB-Mannheim/tesseract/wiki
2. Install it (default path: `C:\Program Files\Tesseract-OCR`).
3. Add that folder to your Windows PATH, **or** set the path explicitly
   near the top of `app/extraction/resume_parser.py`:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```
4. Verify: open a new PowerShell window and run `tesseract --version`.

If Tesseract is missing, the app raises a clear `ResumeParserError`
instead of crashing with a raw traceback.

### 3. Hugging Face model caching

The first run of any AI test/command downloads `Qwen2.5-1.5B-Instruct`
(~3 GB) and `all-MiniLM-L6-v2` (~90 MB) into the Hugging Face cache
(`~/.cache/huggingface` — on Windows, `%USERPROFILE%\.cache\huggingface`).
Every subsequent run reuses the cached files; nothing is re-downloaded.

## Running the application

```powershell
python main.py --resume data\resumes\sample_resume.pdf --job data\job_descriptions\sample_job.txt
```

or run it interactively with no arguments:

```powershell
python main.py
```

## Running every test (in order)

```powershell
python -m tests.test_environment
python -m tests.test_resume_parser
python -m tests.test_resume_analyzer
python -m tests.test_job_analyzer
python -m tests.test_matcher
python -m tests.test_qualification_matcher
python -m tests.test_full_screening
```

## AI model verification

`test_resume_analyzer.py`, `test_job_analyzer.py`, and `test_matcher.py`
each print the exact **model → input → AI output → parsed result**
chain, so you can see the model genuinely reasoning over the text
rather than just confirming it downloaded. `test_job_analyzer.py`
additionally runs two completely different technology stacks (Java vs.
Python) through the *same, unmodified* code to prove the extraction is
dynamic, not a hardcoded skill list.

## Example workflow

1. Drop a resume into `data/resumes/`.
2. Drop or type a job description.
3. `python main.py --resume data/resumes/your_resume.pdf --job-text "..."`
4. Review the JSON result: matched/missing skills, experience and
   education match, final score, and recommendation.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError` | Confirm `.venv` is activated and `pip install -r requirements.txt` completed. |
| `ResumeParserError: Tesseract OCR binary was not found` | Complete the Tesseract setup step above. |
| Model download seems stuck | First download is large (~3 GB); check your network connection and disk space. |
| `[WARN] ... model output was not valid JSON` | The LLM occasionally returns malformed JSON; a safe empty structure is used automatically. Re-running the same input often succeeds. |
| Slow generation on CPU | Expected — Qwen2.5-1.5B runs on CPU but is not fast. A GPU (if available) is used automatically. |

## Future improvements

- REST API layer (FastAPI) wrapping `ScreeningEngine` for a web frontend.
- Batch screening of many resumes against one job description.
- Persisted screening history / database backend.
- Configurable scoring weights via a settings UI instead of `config.py`.
