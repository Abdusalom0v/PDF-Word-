"""Factory for selecting appropriate document reader."""

from pathlib import Path

from readers.base_reader import BaseReader
from readers.text_reader import TextReader
from readers.docx_reader import DocxReader
from readers.pdf_reader import PdfReader
from readers.file_type_detector import detect_file_type


class DocumentFactory:
    """Creates the appropriate reader for a given file."""

    _readers: list[BaseReader] = [
        PdfReader(),
        DocxReader(),
        TextReader(),
    ]

    _ext_to_reader: dict[str, BaseReader] = {
        ext: r
        for r in _readers
        for ext in r.supported_extensions
    }

    @classmethod
    def get_reader(cls, file_path: Path) -> BaseReader | None:
        """Get reader for the given file path. Detects type by extension or magic bytes."""
        detected = detect_file_type(file_path)
        if detected:
            return cls._ext_to_reader.get(detected)
        return None
