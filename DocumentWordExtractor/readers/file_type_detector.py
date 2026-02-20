"""Automatic file type detection by extension and magic bytes."""

from pathlib import Path

# Magic byte signatures: (bytes to check, extension)
# PDF: %PDF
# DOCX: PK (ZIP format - Office Open XML)
MAGIC_SIGNATURES: list[tuple[bytes, str]] = [
    (b"%PDF", ".pdf"),
    (b"PK", ".docx"),  # DOCX is ZIP-based
]


def detect_file_type(file_path: Path) -> str | None:
    """Detect file type from extension first, then from magic bytes.

    Returns the detected extension (e.g. '.pdf', '.docx') or None if unknown.
    """
    suffix = file_path.suffix.lower()
    if suffix in (".pdf", ".docx", ".txt"):
        return suffix

    try:
        with open(file_path, "rb") as f:
            header = f.read(8)
    except OSError:
        return None

    for magic, ext in MAGIC_SIGNATURES:
        if header.startswith(magic):
            return ext
    return None
