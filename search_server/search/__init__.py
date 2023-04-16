"""Initializes search server package."""
from flask import Flask

app = Flask(__name__) 
app.config.from_object('search.config')

# Load inverted index, stopwords, and pagerank into memory
import search.views  # noqa: E402  pylint: disable=wrong-import-position
import search.model  # noqa: E402  pylint: disable=wrong-import-position