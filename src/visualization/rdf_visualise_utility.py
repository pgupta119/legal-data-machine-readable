import logging
from rdflib import Graph
import io
import pydotplus
from rdflib.tools.rdf2dot import rdf2dot

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RDFVisualizer:
    """
    Utility class for visualizing RDF graphs.
    """

    OUTPUT_TTL_PATH = 'data/output/document.ttl'
    OUTPUT_PNG_PATH = 'data/output/document_kg.png'
    MAX_TRIPLES = 15

    @classmethod
    def visualize(cls, graph: Graph):
        """Visualizes the given RDF graph."""
        logger.info("Visualizing RDF graph...")

        filtered_g = cls._filter_triples(graph)
        cls._create_visualization(filtered_g)
        graph.serialize(destination=cls.OUTPUT_TTL_PATH, format='ttl')

        logger.info(f"Visualization saved to {cls.OUTPUT_PNG_PATH}")

    @classmethod
    def _filter_triples(cls, graph: Graph) -> Graph:
        """Returns a new graph containing a subset of triples from the input graph."""
        all_triples = list(graph)
        filtered_triples = all_triples[:cls.MAX_TRIPLES]

        filtered_g = Graph()
        for s, p, o in filtered_triples:
            filtered_g.add((s, p, o))

        return filtered_g

    @staticmethod
    def _create_visualization(graph: Graph):
        """Creates and saves a visualization of the given RDF graph."""
        stream = io.StringIO()
        rdf2dot(graph, stream)
        dg = pydotplus.graph_from_dot_data(stream.getvalue())
        dg.write_png(RDFVisualizer.OUTPUT_PNG_PATH)
