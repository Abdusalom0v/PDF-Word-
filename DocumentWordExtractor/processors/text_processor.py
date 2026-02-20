"""Text processing module for document word extraction."""

import re
import string
from typing import List


class TextProcessor:
    """Process document text: extract words, remove punctuation, remove duplicates."""

    # Word boundary pattern: letters (Latin, Cyrillic), digits
    WORD_PATTERN = re.compile(
        r"\b[a-zA-Zа-яА-ЯёЁәөүҮҗҖңӨӘ0-9]+\b"
    )
    # All punctuation to strip (when used as fallback)
    PUNCTUATION = set(string.punctuation + "«»„"",""—…")

    @classmethod
    def extract_words(cls, text: str) -> List[str]:
        """Extract words from document text.

        Uses word boundaries so punctuation is naturally excluded.
        Supports Latin, Cyrillic (including Uzbek/Kazakh chars), and digits.

        Args:
            text: Raw document text.

        Returns:
            List of all words in the document (punctuation removed).
        """
        if not text or not text.strip():
            return []
        return cls.WORD_PATTERN.findall(text)

    @classmethod
    def remove_punctuation(cls, word: str) -> str:
        """Remove leading and trailing punctuation from a word.

        Args:
            word: Single word or token.

        Returns:
            Word with punctuation stripped.
        """
        return word.strip("".join(cls.PUNCTUATION))

    @classmethod
    def remove_duplicates(cls, words: List[str], preserve_case: bool = False) -> List[str]:
        """Remove duplicate words, preserving order of first occurrence.

        Args:
            words: List of words (may contain duplicates).
            preserve_case: If True, treat "Word" and "word" as different.
                          If False (default), treat them as the same.

        Returns:
            List of unique words in original order.
        """
        seen: set = set()
        result: List[str] = []
        for w in words:
            key = w if preserve_case else w.lower()
            if key not in seen:
                seen.add(key)
                result.append(w)
        return result

    @classmethod
    def get_all_words(cls, text: str) -> List[str]:
        """Get list of all words in the document (punctuation removed, duplicates kept).

        Args:
            text: Document text.

        Returns:
            List of every word occurrence in document order.
        """
        return cls.extract_words(text)

    @classmethod
    def get_unique_words(cls, text: str) -> List[str]:
        """Get list of unique words (no duplicates), preserving first occurrence order.

        Args:
            text: Document text.

        Returns:
            List of unique words.
        """
        words = cls.extract_words(text)
        return cls.remove_duplicates(words, preserve_case=False)
