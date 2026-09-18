"""
app/extraction/resume_parser.py

Extracts raw text from a resume file (PDF, JPG, JPEG, PNG).

- PDFs with a real text layer: extracted directly via PyMuPDF.
- PDFs that are scanned/image-only (no extractable text on a page):
  that page is rasterized and OCR'd automatically.
- JPG/JPEG/PNG: OCR'd directly.

The caller never has to say whether a file is "text-based" or
"image-based" - this module determines that per-page automatically.
"""
from __future__ import annotations

import io
import shutil
from pathlib import Path

import pymupdf
from PIL import Image

try:
    import pytesseract
    _PYTESSERACT_IMPORTABLE = True
except ImportError:  # pragma: no cover
    _PYTESSERACT_IMPORTABLE = False


class ResumeParserError(Exception):
    """Raised for any resume extraction failure, with a clear, actionable message."""


SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

# A PDF page with fewer than this many extracted characters is treated
# as scanned/image-only and routed through OCR instead.
MIN_TEXT_LAYER_CHARS = 20


class ResumeParser:
    """Single entry point for turning a resume file into plain text."""

    def parse(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise ResumeParserError(f"Resume file not found: {file_path}")

        extension = path.suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            raise ResumeParserError(
                f"Unsupported file type '{extension}'. "
                f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )

        text = self._parse_pdf(path) if extension == ".pdf" else self._parse_image(path)
        text = text.strip()

        if not text:
            raise ResumeParserError(
                f"No text could be extracted from '{path.name}'. "
                "The file may be empty, corrupted, or an unreadable scan."
            )
        return text

    # ---- PDF handling ----

    def _parse_pdf(self, path: Path) -> str:
        try:
            doc = pymupdf.open(str(path))
        except Exception as exc:
            raise ResumeParserError(f"Could not open PDF '{path.name}': {exc}") from exc

        if doc.page_count == 0:
            doc.close()
            raise ResumeParserError(f"PDF '{path.name}' has no pages.")

        parts: list[str] = []
        used_ocr = False

        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)
            page_text = page.get_text().strip()

            if len(page_text) >= MIN_TEXT_LAYER_CHARS:
                parts.append(page_text)
            else:
                used_ocr = True
                parts.append(self._ocr_pdf_page(page))

        doc.close()

        if used_ocr:
            print(f"[INFO] '{path.name}' contained scanned/image page(s) - OCR was used automatically.")

        return "\n".join(part for part in parts if part)

    def _ocr_pdf_page(self, page) -> str:
        self._require_tesseract()
        pixmap = page.get_pixmap(dpi=300)
        image = Image.open(io.BytesIO(pixmap.tobytes("png")))
        return self._run_ocr(image)

    # ---- Image handling ----

    def _parse_image(self, path: Path) -> str:
        self._require_tesseract()
        try:
            image = Image.open(path)
        except Exception as exc:
            raise ResumeParserError(f"Could not open image '{path.name}': {exc}") from exc
        return self._run_ocr(image)

    def _run_ocr(self, image: Image.Image) -> str:
        try:
            return pytesseract.image_to_string(image)
        except Exception as exc:
            raise ResumeParserError(
                f"OCR failed: {exc}\n"
                "If this mentions Tesseract not being found, see the README "
                "'Tesseract setup' section."
            ) from exc

    def _require_tesseract(self) -> None:
        if not _PYTESSERACT_IMPORTABLE:
            raise ResumeParserError(
                "pytesseract is not installed. Run: "
                "python -m pip install pytesseract"
            )

        if shutil.which("tesseract") is not None:
            return

        try:
            pytesseract.get_tesseract_version()
            return
        except Exception:
            raise ResumeParserError(
                "Tesseract OCR binary was not found on PATH.\n"
                "1. Install it from https://github.com/UB-Mannheim/tesseract/wiki\n"
                "2. Either add the install folder to your PATH, or set:\n"
                "     import pytesseract\n"
                "     pytesseract.pytesseract.tesseract_cmd = "
                "r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'\n"
                "   near the top of app/extraction/resume_parser.py.\n"
                "See README.md 'Tesseract setup' for full details."
            )
