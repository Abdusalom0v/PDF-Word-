"""Microsoft Word (.docx) document reader."""

from pathlib import Path

from readers.base_reader import BaseReader


class DocxReader(BaseReader):
    """Reader for Microsoft Word .docx files."""

    def read(self, file_path: Path) -> str:
        """Read Word document content using python-docx."""
        try:
            from docx import Document
        except ImportError as e:
            raise RuntimeError(
                "python-docx is not installed. Install with: pip install python-docx"
            ) from e

        try:
            doc = Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)
        except Exception as e:
            raise ValueError(f"Corrupted or invalid DOCX file: {e}") from e

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (".docx",)

