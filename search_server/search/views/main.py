"""Search Server views/main.py"""

import heapq
from threading import Thread

import flask
import requests
import search
from flask import render_template, request

def get_index(query, weight, index_url, search_results):
    """Search index and get URL"""
    # Construct search
    search = f"{index_url}?q={query}&w={weight}"
    # Get search results
    response = requests.get(search)
    if response:
        search_results.append(response.json()) #check, do I need to do any sort of []?

@search.app.route('/')
def show_index():
    """Display / route and search results."""

    query = request.args.get('q')
    weight = float(request.args.get('w', default=0.5))

    # If empty query
    if query is None:
        context = {
            "numdocs": 0,
            "search_results": [],
            "query": query,
            "weight": weight
        }
        return flask.render_template("index.html", **context)
    # If query NOT empty, should display results
    else:
        top10_results = []
        index_urls = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
        # Use threads for concurrent requests
        threads = []       
        for url in index_urls:
            thread = Thread(target=get_index, args=(query, weight, url, top10_results))
            threads.append(thread)
            thread.start()
        
        connection = search.model.get_db()
        for search_result in heapq.merge(*top10_results):
            
            # Get all docs
            cur = connection.execute(
                "SELECT * FROM Documents WHERE docid = ?",
                (search_result["docid"],)
            )
            document = cur.fetchone()
            # Get up to 10 search results to the context, no more
            if len(top10_results) < 10:
                top10_results.append({
                    "doc_url": document["url"],
                    "doc_title": document["title"],
                    "doc_summary": document["summary"],
                })

        for thread in threads:
            thread.join()
        
        # Errorcheck weight (idk if this is necessary)
        if weight < 0.0:
            weight = 0
        elif weight > 1.0:
            weight = 1

        context = {
            "numdocs": len(top10_results),
            "search_results": top10_results,
            "query": query,
            "weight": weight
        }

        return render_template("index.html", **context)