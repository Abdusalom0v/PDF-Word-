"""Word extraction processor."""

import re
from typing import List


class WordExtractor:
    """Extracts and processes words from text."""

    WORD_PATTERN = re.compile(r"\b[a-zA-Zа-яА-ЯёЁәөүҮҗҖңӨӘ0-9]+\b")

    @classmethod
    def extract_words(cls, text: str) -> List[str]:
        """Extract all words from text.

        Args:
            text: Source text to extract words from.

        Returns:
            List of extracted words.
        """
        if not text or not text.strip():
            return []
        return cls.WORD_PATTERN.findall(text)

    @classmethod
    def extract_unique_words(cls, text: str) -> List[str]:
        """Extract unique words preserving order of first occurrence."""
        seen = set()
        result = []
        for word in cls.extract_words(text):
            lower = word.lower()
            if lower not in seen:
                seen.add(lower)
                result.append(word)
        return result
