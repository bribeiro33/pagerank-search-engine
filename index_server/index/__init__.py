"""Initializes index server package and loads necessary files into memory."""

from flask import Flask
import os

app = Flask(__name__) 
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

# Load inverted index, stopwords, and pagerank into memory
import index.api  # noqa: E402  pylint: disable=wrong-import-position
index.api.load_index()