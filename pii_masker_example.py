"""
PII Masker Example:

This script demonstrates the process of detecting and masking personally identifiable
information (PII) from a given legal document text. The script provides basic
implementations for masking email addresses and phone numbers.

Classes:
- PII_Masker: Handles the task of masking PIIs in provided text.
- LegalDocument: Represents a legal document with methods to access metadata,
                 mask PII, convert to JSON, and share with collaborators.

Usage:
Run the script to create a `LegalDocument` object and mask the PIIs. The script
then prints the masked text, metadata, text, and a JSON representation of the document.
"""

import re
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class PII_Masker:
    def __init__(self, text):
        self.text = text

    def mask_pii(self, text):
        """Masks email addresses and phone numbers in the provided text."""
        text = re.sub(r'[\w\.-]+@[\w\.-]+', '***MASKED EMAIL***', text)

        # Updated phone number regex to account for spaces, dashes, and other separators
        text = re.sub(r'(\d{1,3}[-.\s]?){2}\d{4}', '***MASKED PHONE***', text)

        return text


class LegalDocument:
    def __init__(self, text):
        self.text = text
        self.metadata = {
            "title": "Legal Document",
            "author": "Your Name",
            "date_created": "2023-08-22",
        }
        logging.info("Legal document created.")

    def get_metadata(self):
        """Returns the metadata of the document."""
        return self.metadata

    def mask_pii(self):
        """Masks PIIs in the document using the PII_Masker class."""
        logging.info("Masking PII data in the document.")
        pii_masker = PII_Masker(self.text)
        return pii_masker.mask_pii(self.text)