"""Search Server views/main.py."""

import heapq
from threading import Thread, Event

import flask
import requests
import search
from flask import render_template, request


def get_index(query, weight, index_url, search_results, event):
    """Search index and get URL."""
    # Construct search
    get_search = f"{index_url}?q={query}&w={weight}"
    # Get search results
    response = requests.get(get_search, timeout=10)
    if response:
        # response is a list not dict bc dict doesn't work w/ heapq.merge
        search_results.append(response.json()["hits"])
    event.set()


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
            "weight": weight,
            "empty": True
        }
        return flask.render_template("index.html", **context)
    # If query NOT empty, should display results
    top10_results = []
    index_urls = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
    # Use threads for concurrent requests
    threads = []

    # Create a list of Event objects
    events = [Event() for _ in range(3)]

    for i, url in enumerate(index_urls):
        thread = Thread(target=get_index, args=(query, weight, url,
                                                top10_results, events[i]))
        threads.append(thread)
        thread.start()

    # Wait for all events to be set
    events[0].wait()
    events[1].wait()
    events[2].wait()
    # Need all results from 3 api requests before merging the results
    for thread in threads:
        thread.join()

    connection = search.model.get_db()
    final_results = []
    i = False  # i is the same as completed_results, just did this for styling
    # loops through each docid in the merged doc response
    # need to sort by the score values of each docid in desc order
    for pair in heapq.merge(*top10_results,
                            key=lambda x: x["score"],
                            reverse=True):
        if i:
            break
        # Get all the doc's info with curr_docid
        cur = connection.execute(
            "SELECT * FROM Documents WHERE docid = ?",
            (pair['docid'],)
        )
        document = cur.fetchone()
        # Get up to 10 search results to the context, no more
        if len(final_results) < 10:
            final_results.append({
                "doc_url": document["url"],
                "doc_title": document["title"],
                "doc_summary": document["summary"],
            })
        else:
            i = True

    # Errorcheck weight (idk if this is necessary)
    if weight < 0.0:
        weight = 0
    elif weight > 1.0:
        weight = 1

    context = {
        "numdocs": len(final_results),
        "search_results": final_results,
        "query": query,
        "weight": weight,
        "empty": False
    }

    return render_template("index.html", **context)
