from abc import ABC, abstractmethod

# ===============================
# PARSER STRATEGY AND IMPLEMENTATIONS
# ===============================

class ParserStrategy(ABC):
    """Abstract Base Class defining the strategy interface for parsers."""
    REGISTRY = {} 

    @abstractmethod
    def parse(self, data):
        pass

    @classmethod
    def register_parser(cls, file_type):
        def decorator(subclass):
            cls.REGISTRY[file_type] = subclass
            return subclass 
        return decorator

@ParserStrategy.register_parser('JSON')
class JSONParserStrategy(ParserStrategy):
    """Concrete parser strategy for parsing JSON data."""
    def __init__(self):
        import json
        self.json = json

    def parse(self, data):
        return self.json.loads(data)

@ParserStrategy.register_parser('CSV')
class CSVParserStrategy(ParserStrategy):
    """Concrete parser strategy for parsing CSV data."""
    def __init__(self):
        import csv
        from io import StringIO
        self.csv = csv
        self.StringIO = StringIO

    def parse(self, data):
        reader = self.csv.DictReader(self.StringIO(data))
        return [dict(row) for row in reader]

# ===============================
# PARSER FACTORY
# ===============================

class ParserFactory:
    """Factory class to provide the appropriate parser based on the file type."""
    @staticmethod
    def get_parser(file_type):
        parser_class = ParserStrategy.REGISTRY.get(file_type)
        if not parser_class:
            raise ValueError(f"Invalid file type: {file_type}")
        return parser_class()