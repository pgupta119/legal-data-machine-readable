
import json
import logging

from src.constants import DOC_URL
from src.document.document import Document
from src.document.parser import DocumentParser
from src.document.scraper import DocumentScraper
from src.rdf.rdf_converter import RDFConverter
from src.visualization.rdf_visualise_utility import RDFVisualizer
from pii_masker_example import LegalDocument

# Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)


def initialize_logging(log_level=logging.INFO):
    """Initialize logging settings."""
    logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s]: %(message)s")


def run_rdf_conversion(document):
    """
    Load and convert JSON data to RDF format, then visualize the graph.

    Args:
        document (Document): An instance of the Document class.
    """
    try:
        with open('data/processed/json_after_parsing') as f:
            json_data = json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON data: {e}")
        return

    converter = RDFConverter(json_data, document)
    graph = converter.get_graph()

    # Visualize the graph
    RDFVisualizer.visualize(graph)


def run_pii_masker_example():
    legal_text = """
   Hello, my email is example@email.com and my phone is 1234567890.
    """
    print("before masking: ", legal_text)
    document = LegalDocument(legal_text)
    masked_document = document.mask_pii()
    print("after masking: ", masked_document)


def main():
    """Main function to scrape, parse, save and convert documents."""
    document = Document()
    scraper = DocumentScraper(url=DOC_URL)
    soup = scraper.get_soup()
    logger.info("Successfully fetched and parsed content.")

    try:
        parser = DocumentParser(soup=soup, document=document)
        document_data = parser.parse_document()
    except Exception as e:
        logger.error(f"Error during scraping or parsing: {e}")
        return

    # Save the parsed data as JSON
    try:
        with open('data/processed/json_after_parsing', 'w') as json_file:
            json.dump(document_data, json_file, indent=1)
        logger.info("Document data saved to JSON successfully.")
    except Exception as e:
        logger.error(f"Error saving parsed data to JSON: {e}")
        return

    run_rdf_conversion(document)


if __name__ == "__main__":
    initialize_logging()
    main()

    """
    Run the script to create a `LegalDocument` object and mask the PIIs. The script
    then prints the text before and after mask.
    """
    run_pii_masker_example()

