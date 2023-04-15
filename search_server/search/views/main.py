"""Search Server views/main.py"""

import heapq
from threading import Thread

import flask
import requests
import search
from flask import render_template, request

@search.app.route('/')
def show_index():
    """Display / route and search results."""

    query = request.args.get('q', type=str)
    weight = request.args.get('w', default=0.5, type=float)

    # If empty query
    if query is None:
        context = {
            "numdocs": 0,
            "top10docs": [],
            "query": query,
            "weight": weight
        }
        return flask.render_template("index.html", **context)
    else:
        connection = search.model.get_db()

        top10 = []
        num_docs = 0 # for now this is filler
        # Errorcheck weight (idk if this is necessary)
        if weight < 0.0:
            weight = 0
        elif weight > 1.0:
            weight = 1
        context = {
            "numdocs": num_docs,
            "top10docs": top10,
            "query": query,
            "weight": weight
        }
