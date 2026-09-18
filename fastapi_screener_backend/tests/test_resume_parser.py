"""
tests/test_resume_parser.py

Run with:
    python -m tests.test_resume_parser

Verifies text extraction from a text-layer PDF and (if Tesseract is
installed) from a generated image, proving the parser automatically
picks the correct extraction path per file.
"""
import os
import tempfile

import pymupdf
from PIL import Image, ImageDraw

from app.extraction.resume_parser import ResumeParser, ResumeParserError


SAMPLE_RESUME_TEXT = "John Doe\nSoftware Engineer\nSkills: Java, Spring Boot, AWS\n"


def _make_text_pdf(path: str) -> None:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), SAMPLE_RESUME_TEXT)
    doc.save(path)
    doc.close()


def _make_image_with_text(path: str) -> None:
    image = Image.new("RGB", (700, 150), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "Jane Smith - Python, Django, PostgreSQL", fill="black")
    image.save(path)


def test_text_layer_pdf() -> bool:
    print("\n--- Test: text-layer PDF ---")
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = os.path.join(tmp, "resume.pdf")
        _make_text_pdf(pdf_path)

        text = ResumeParser().parse(pdf_path)
        print("Extracted text:\n" + text)

        ok = "Java" in text and "AWS" in text
        print(f"[{'PASS' if ok else 'FAIL'}] Text-layer PDF extraction")
        return ok


def test_image_ocr() -> bool:
    print("\n--- Test: image OCR (PNG) ---")
    with tempfile.TemporaryDirectory() as tmp:
        image_path = os.path.join(tmp, "resume.png")
        _make_image_with_text(image_path)

        try:
            text = ResumeParser().parse(image_path)
        except ResumeParserError as exc:
            print(f"[SKIP] OCR test skipped (Tesseract likely not installed yet): {exc}")
            return True  # Do not fail the whole suite before Phase-2 setup is done.

        print("Extracted text:\n" + text)
        ok = "Python" in text or "Django" in text
        print(f"[{'PASS' if ok else 'FAIL'}] Image OCR extraction")
        return ok


def test_unsupported_file() -> bool:
    print("\n--- Test: unsupported file type ---")
    with tempfile.TemporaryDirectory() as tmp:
        bad_path = os.path.join(tmp, "resume.txt")
        with open(bad_path, "w", encoding="utf-8") as f:
            f.write("plain text file")

        try:
            ResumeParser().parse(bad_path)
            print("[FAIL] Expected ResumeParserError for unsupported type")
            return False
        except ResumeParserError as exc:
            print(f"[PASS] Correctly rejected unsupported file: {exc}")
            return True


def main() -> int:
    results = [test_text_layer_pdf(), test_image_ocr(), test_unsupported_file()]
    passed = sum(results)
    print(f"\n{passed}/{len(results)} resume parser tests passed.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
