import logging
import requests
from bs4 import BeautifulSoup

# Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)


class DocumentScraper:
    """
    A class used to scrape web content and represent it using BeautifulSoup.
    """

    def __init__(self, url: str):
        self.url = url
        self.soup = self._initialize_soup()

    def _initialize_soup(self) -> BeautifulSoup:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch content from URL: {self.url}. Error: {e}")
            raise

    def get_soup(self) -> BeautifulSoup:
        return self.soup