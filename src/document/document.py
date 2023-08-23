class Document:
    """
    A singleton class that represents a document with meta-data and data.

    The singleton pattern ensures that there's only one instance of the Document
    class at any given time, providing a single point of access to this instance.
    """

    _instance = None  # Singleton instance holder

    def __new__(cls):
        # If no instance exists, create a new one and store it in _instance
        if not cls._instance:
            cls._instance = super(Document, cls).__new__(cls)
        return cls._instance  # Return the stored instance

    def __init__(self):
        if not hasattr(self, 'meta_data'):  # Check to prevent reinitialization
            self.meta_data = {}
            self.data = []
