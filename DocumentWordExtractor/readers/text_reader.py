"""Plain text and basic document reader."""

from pathlib import Path

from readers.base_reader import BaseReader


class TextReader(BaseReader):
    """Reader for plain text files (.txt) and fallback for other formats."""

    def read(self, file_path: Path) -> str:
        """Read plain text file content."""
        try:
            with open(file_path, encoding="utf-8", errors="replace") as f:
                return f.read()
        except OSError as e:
            raise ValueError(f"Cannot read file: {e}") from e

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        return (".txt",)

