"""PDF document reader using PyMuPDF."""

from pathlib import Path

from readers.base_reader import BaseReader


class PdfReader(BaseReader):
    """Reader for PDF files using PyMuPDF (fitz)."""

    def read(self, file_path: Path) -> str:
        """Read PDF content and return extracted text."""
        try:
            import fitz  # PyMuPDF
        except ImportError as e:
            raise RuntimeError("PyMuPDF is not installed. Install with: pip install PyMuPDF") from e

        try:
            doc = fitz.open(file_path)
        except fitz.FileDataError as e:
            raise ValueError(f"Corrupted or invalid PDF file: {e}") from e
        except Exception as e:
            raise ValueError(f"Cannot open PDF file: {e}") from e

        try:
            text_parts: list[str] = []
            for page in doc:
                text_parts.append(page.get_text())
            return "\n\n".join(text_parts).strip()
        finally:
            doc.close()

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (".pdf",)
