"""Base document reader interface."""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseReader(ABC):
    """Abstract base class for document readers."""

    @abstractmethod
    def read(self, file_path: Path) -> str:
        """Read document content and return as plain text.

        Args:
            file_path: Path to the document file.

        Returns:
            Extracted text content.
        """
        pass

    @property
    @abstractmethod
    def supported_extensions(self) -> tuple[str, ...]:
        """Return tuple of supported file extensions (e.g. ('.docx', '.doc'))."""
        pass
