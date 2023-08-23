from typing import List, Pattern

DOC_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R0947&from=en#d1e40-45-1"


# Patterns for cleaning texts, described in a tuple: (pattern, replacement)
CLEANING_PATTERNS: List[Pattern[str]] = [
    (r'[\n\xa0]+', ' '),  # Replace newlines and non-breaking spaces with space
    (r'[\‘\’\'"]', ''),  # Remove quotation marks
    (r'\(\d+\)', ''),  # Remove numbers inside parentheses
    (r'\([a-z]\)', ''),  # Remove lowercase letters inside parentheses followed by a dot
    (r';', ''),  # Remove semicolons
    (r'\d+\.\s', ''),  # Remove numbers followed by a dot and space
    (r'[a-z]\.\s', ''),  # Remove lowercase letters followed by a dot and space
    (r'[A-Z]\.\s', ''),  # Remove uppercase letters followed by a dot and space
    (r'[^\x00-\x7F]+', ''),  # Remove non-ASCII characters
    (r',', ''),  # Remove commas
    (r' +', ' ')  # Replace multiple spaces with a single space
]