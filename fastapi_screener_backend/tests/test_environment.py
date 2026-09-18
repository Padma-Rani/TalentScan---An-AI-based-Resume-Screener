"""
tests/test_environment.py

PHASE 1 verification script.

Run with:
    python -m tests.test_environment

Purpose:
    Confirms that the virtual environment is correctly set up and that
    every core dependency the AI pipeline will need is importable and
    reports a usable version, BEFORE any AI/OCR code is written.

This does not test AI logic - it only tests that the environment is
ready for Phase 2 (extraction) and Phase 3 (shared AI model manager).
"""

import sys
import shutil
import platform


def _line(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def check_python() -> bool:
    _line("PYTHON")
    print(f"Python executable : {sys.executable}")
    print(f"Python version    : {platform.python_version()}")
    ok = sys.version_info.major == 3 and sys.version_info.minor >= 11
    if not ok:
        print("WARNING: Expected Python 3.11+ (target is 3.13.3).")
    return ok


def check_virtualenv() -> bool:
    _line("VIRTUAL ENVIRONMENT")
    in_venv = sys.prefix != sys.base_prefix
    print(f"Running inside a virtual environment : {in_venv}")
    print(f"sys.prefix       : {sys.prefix}")
    print(f"sys.base_prefix  : {sys.base_prefix}")
    if not in_venv:
        print(
            "WARNING: You do not appear to be running inside .venv.\n"
            "Activate it first:\n"
            "    .\\.venv\\Scripts\\Activate.ps1"
        )
    return in_venv


def check_package(import_name: str, display_name: str | None = None) -> bool:
    display_name = display_name or import_name
    try:
        module = __import__(import_name)
        version = getattr(module, "__version__", "unknown")
        print(f"[OK]   {display_name:<22} version={version}")
        return True
    except ImportError as exc:
        print(f"[FAIL] {display_name:<22} not importable ({exc})")
        return False


def check_torch_device() -> None:
    try:
        import torch

        cuda_available = torch.cuda.is_available()
        print(f"[INFO] torch CUDA available: {cuda_available}")
        if cuda_available:
            print(f"[INFO] CUDA device: {torch.cuda.get_device_name(0)}")
        else:
            print("[INFO] No GPU detected - the system will run on CPU.")
    except Exception as exc:  # pragma: no cover - diagnostic only
        print(f"[WARN] Could not query torch device info: {exc}")


def check_tesseract() -> bool:
    _line("TESSERACT OCR (SYSTEM BINARY)")
    path = shutil.which("tesseract")
    if path:
        print(f"[OK]   tesseract binary found at: {path}")
        return True
    print(
        "[FAIL] tesseract binary was not found on PATH.\n"
        "       Install Tesseract OCR for Windows and either:\n"
        "         1) Add its install folder to your PATH, or\n"
        "         2) Set pytesseract.pytesseract.tesseract_cmd explicitly\n"
        "            in app/extraction/resume_parser.py once that file exists.\n"
        "       See README.md 'Tesseract setup' section for exact steps."
    )
    return False


def main() -> int:
    results = []

    results.append(("Python version", check_python()))
    results.append(("Virtual environment active", check_virtualenv()))

    _line("CORE ML / NLP LIBRARIES")
    results.append(("torch", check_package("torch")))
    results.append(("transformers", check_package("transformers")))
    results.append(("sentence_transformers", check_package("sentence_transformers")))
    results.append(("huggingface_hub", check_package("huggingface_hub")))
    check_torch_device()

    _line("DOCUMENT / IMAGE LIBRARIES")
    results.append(("pymupdf", check_package("pymupdf")))
    results.append(("PIL (Pillow)", check_package("PIL", "Pillow")))
    results.append(("pytesseract", check_package("pytesseract")))

    _line("UTILITIES")
    results.append(("pydantic", check_package("pydantic")))
    results.append(("numpy", check_package("numpy")))

    results.append(("Tesseract OCR binary", check_tesseract()))

    _line("SUMMARY")
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print(f"\n{passed}/{total} checks passed.")

    if passed == total:
        print("\nEnvironment is ready for Phase 2 (Resume extraction/OCR).")
        return 0

    print(
        "\nSome checks failed. Fix the items marked [FAIL] above before "
        "moving on to Phase 2. Re-run:\n"
        "    python -m tests.test_environment"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
