import re
from typing import List
from src.constants import CLEANING_PATTERNS


class TextCleaner:

    def __init__(self):
        self.text = ''

    def clean_text(self, texts: List[str]) -> List[str]:
        """
        Cleans the provided text entries.
        """
        clean_texts = []
        for text in texts:
            cleaned = self._apply_patterns(text)
            clean_texts.append(cleaned.strip())

        return clean_texts

    def _apply_patterns(self, text: str) -> str:
        """Apply cleaning patterns to the text."""
        for pattern, replacement in CLEANING_PATTERNS:
            text = re.sub(pattern, replacement, text)
        return text
