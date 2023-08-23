import json
import logging
import urllib
from rdflib import Namespace, URIRef, Literal, Graph, XSD

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RDFConverter:
    """
    Class to convert the given data to RDF format.
    """

    def __init__(self, json_data, document):
        self.json_data = json_data
        self.g = Graph()
        self.document = document
        self._initialize_namespaces()
        self._convert_to_rdf()

    def _initialize_namespaces(self):
        """Initializes namespaces for RDF conversion."""
        logger.info("Initializing RDF namespaces.")
        self.schema = Namespace('http://schema.org/')
        self.dc = Namespace('http://purl.org/dc/terms/URI')
        self.RDF = Namespace('http://www.w3.org/2000/01/rdf-schema#')
        self.eli = Namespace("http://data.europa.eu/eli/ontology#")
        self.doc = URIRef("http://example.org/document/")
        self.cdm = Namespace('http://publications.europa.eu/ontology/cdm#')

    def _convert_to_rdf(self):
        logger.info("Converting JSON data to RDF format.")
        self._convert_to_rdf_for_articles()

        with open('data/output/document_metadata.json', 'w') as json_file_metadata:
            json.dump(self.document.__dict__, json_file_metadata, indent=1)
        logger.info("Saved document metadata to JSON file.")

    def _convert_to_rdf_for_articles(self):
        logger.info("Converting articles to RDF format.")
        self.g.add((self.doc, URIRef(self.cdm + 'language'), Literal(self.document.meta_data['language'])))
        self.g.add((self.doc, URIRef(self.schema), Literal(self.document.meta_data['title_document'])))

        for article in self.json_data['article']:
            text = ' '.join(article['data'])
            uri = URIRef(
                urllib.parse.quote(self.doc) +
                urllib.parse.quote('article/') +
                urllib.parse.quote(article["article_number"].replace(' ', '%'))
            )

            articles_data = {
                'article_number': article['article_number'],
                'article_name': article['article_name'],
                'article_text': text,
                'uri': urllib.parse.unquote(uri)
            }
            self.document.data.append(articles_data)
            self.g.add((uri, self.RDF.type, self.schema.Article))
            self.g.add((uri, URIRef(self.eli + 'SubdivisionType'), Literal("Article", datatype=XSD.string)))
            self.g.add((uri, URIRef(self.dc + 'isPartOf'), self.doc))
        logger.info("Finished adding articles to the RDF graph.")

    def get_graph(self):
        logger.info("Returning the constructed RDF graph.")
        return self.g
