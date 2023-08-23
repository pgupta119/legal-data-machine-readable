from bs4 import BeautifulSoup
from typing import List, Dict, Union, Optional
import logging

# Local imports
from src.document.document import Document
from src.document.text_cleaner import TextCleaner

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)


class DocumentParser:
    """
    A parser for extracting information from documents using BeautifulSoup.
    """

    def __init__(self, soup: BeautifulSoup, document: Document):
        """
        Initialize the DocumentParser with a BeautifulSoup object and Document instance.
        """
        self.soup = soup
        self.text = ""
        self.cleaner = TextCleaner()
        self.document = document
        self._populate_meta_data()

    def _populate_meta_data(self):
        """Fetches and populates the document meta-data."""
        try:
            meta_data = {
                'language': self.soup.find('p', class_='hd-lg').text,
                'published_date': self.cleaner.clean_text([self.soup.find('p', class_='hd-date').text])[0],
                'title_document': self.soup.find('p', class_='hd-ti').text,
                'uri': "https://example.com/document"
            }
            self.document.meta_data.update(meta_data)
        except Exception as e:
            logger.error(f"Error populating meta data: {e}")

    # The rest of your methods follow the same pattern...

    # For instance:
    def get_article_ids(self) -> List[str]:
        try:
            article_ids = [tag['id'] for tag in self.soup.select('div[id]') if '.' not in tag['id']]
            return article_ids
        except Exception as e:
            logger.error(f"Error getting article IDs: {e}")
            return []

    def get_articles(self) -> List[Dict[str, Union[str, List[str]]]]:
        try:
            article_ids = self.get_article_ids()
            article_numbers = [item.get_text() for item in self.soup.find_all('p', class_="ti-art")]
            article_definitions = [item.get_text() for item in self.soup.find_all('p', class_="sti-art")]

            articles = []
            for i, article_id in enumerate(article_ids):
                article_info = {
                    "article_number": article_numbers[i],
                    "article_name": self.cleaner.clean_text([article_definitions[i]])[0]
                }
                article_data_soup = self.soup.find_all(id=article_id)[0]
                article_data = [" ".join([p.get_text() for p in article_data_soup.find_all('p', class_='normal')])]
                article_info["data"] = self.cleaner.clean_text(article_data)
                articles.append(article_info)
            return articles
        except Exception as e:
            logger.error(f"Error fetching articles: {e}")
            return []

    def get_annexes(self) -> List[Dict[str, Union[str, List[str]]]]:
        try:
            return self.cleaner.clean_text([item.get_text() for item in self.soup.find_all('div', id='L_2019152EN.01006001')])
        except Exception as e:
            logger.error(f"Error fetching annexes: {e}")
            return []

    def get_titles(self) -> List[str]:
        try:
            titles = [item.get_text() for item in self.soup.find_all(class_='doc-ti')]
            return self.cleaner.clean_text(titles)
        except Exception as e:
            logger.error(f"Error fetching titles: {e}")
            return []

    def get_treaty_regulations(self) -> List[str]:
        try:
            stop_at = self.soup.find("div", id='001')  # finds your stop tag
            treaty_points = stop_at.find_all_previous("p", class_="normal")
            treaty_points.reverse()
            return self.cleaner.clean_text([" ".join([item.get_text() for item in treaty_points])])
        except Exception as e:
            logger.error(f"Error fetching treaty regulations: {e}")
            return []

    def get_notes(self) -> List[str]:
        try:
            notes = [item.get_text() for item in self.soup.find_all('p', class_="note")]
            return self.cleaner.clean_text(notes)
        except Exception as e:
            logger.error(f"Error fetching notes: {e}")
            return []

    def get_signature(self) -> Optional[str]:
        try:
            return self.cleaner.clean_text([item.get_text() for item in self.soup.find_all(class_="final")])[0]
        except Exception as e:
            logger.error(f"Error fetching signature: {e}")
            return None

    def parse_document(self) -> Dict[str, Union[List[str], List[Dict[str, str]]]]:
        try:
            return {
                'article': self.get_articles(),
                'notes': self.get_notes(),
                'titles': self.get_titles(),
                'signature': self.get_signature(),
                'annex': self.get_annexes(),
                'treaty_rules': self.get_treaty_regulations()
            }
        except Exception as e:
            logger.error(f"Error parsing the document: {e}")
            return {}
