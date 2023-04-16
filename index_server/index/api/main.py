"""Index Server main code."""
import math
import pathlib
import re
from flask import jsonify, request
import index


# Globals: stopwords (set), pagerank (dict), inverted_index (dict)
stopwords = set()
pagerank = {}
inverted_index = {}
# -----------------     Main functions    ----------------- #
@index.app.route("/api/v1/", methods=["GET"])
def get_services():
    """Return a list of services available."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return jsonify(**context)


@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hits():
    """Return the list of hits given the query."""
    dirty_query = request.args.get("q")
    weight = float(request.args.get("w", default=0.5))
    clean_query = query_cleaning(dirty_query)
    hit_results = get_hit_results(clean_query, weight)
    context = {"hits": hit_results}
    return jsonify(**context)


def load_index():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    load_stopwords(index_dir)
    load_pagerank(index_dir)
    load_inverted_index(index_dir)

# -----------------     load_index helpers    ----------------- #


def load_stopwords(index_dir):
    """Load the stopwords.txt file into stopwords."""
    # Create global var to be accessed in calc funcs later
    global stopwords
    stopwords = set()
    # Get correct path: /index/stopwords.txt
    stopwords_file = index_dir / "stopwords.txt"
    with open(str(stopwords_file), 'r', encoding='utf-8') as infile:
        for line in infile:
            # incase there's extra whitespace, strip
            new_word = line.strip()
            stopwords.add(new_word)


def load_pagerank(index_dir):
    """Load the pagerank.out file into pagerank."""
    # Create global var to be accessed in calc funcs later
    global pagerank
    pagerank = {}
    # Get correct path: /index/pagerank.out
    pagerank_file = index_dir / "pagerank.out"
    with open(str(pagerank_file), 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            # create a data structure that maps doc ID to PageRank score
            # e.g.
            # 3434750,0.0193215
            # 20381,0.0104298
            docid, score = line.split(",")
            pagerank[docid] = float(score)


def load_inverted_index(index_dir):
    """Read the inverted_index.txt file, based on the configured envvar."""
    global inverted_index
    inverted_index = {}

    # which index_path was set is the index file of inverted index to read frm
    # e.g. inverted_index_0.txt
    index_file_config = index.app.config["INDEX_PATH"]
    # /index/inverted_index/inverted_index_0|1|2.txt
    inverted_index_file = index_dir / "inverted_index" / index_file_config
    with open(str(inverted_index_file), 'r', encoding='utf-8') as infile:
        for line in infile:
            # Each item is separated by a space
            index_list = line.strip().split()
            term_name = index_list[0]
            idf = index_list[1]
            # doc specific info starts at [2] and contains 3 items for each doc
            counter = 2
            # keep track of all doc triples for the term
            # docs is a dictionary w/ docid as key and a dict with tf and norm
            docs = {}
            while counter < len(index_list):
                curr_docid = index_list[counter]
                curr_doc_double = {
                    "tf": int(index_list[counter + 1]),
                    "norm_fac": float(index_list[counter + 2])
                }
                docs[curr_docid] = curr_doc_double
                counter += 3

            term_value = {
                "idf": idf,
                "docs": docs
            }
            inverted_index[term_name] = term_value


# -----------------     get_hits helpers   ----------------- #
def query_cleaning(dirty_query):
    """Clean the query (alpha-numeric, case insensitive, no stopwords)."""
    global stopwords
    # Remove non-alphanumeric characters (that also aren’t spaces) like this:
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", dirty_query)
    # Remove extra whitespace
    query = query.strip()
    # Case insensitive.
    # Convert upper case characters to lower case using casefold().
    query = query.casefold()
    # Split the text into whitespace-delimited terms.
    query_list = query.split()
    # Remove stop words.
    clean_query = [word for word in query_list if word not in stopwords]
    return clean_query


def get_hit_results(clean_query, weight):
    """Return the hits corresponding to the query."""
    # Find the freq of each word in the query
    query_tf = count_query_tf(clean_query)
    # If no terms, return empty
    if query_tf is None:
        return []

    # calc query vector
    query_vector = calc_query_vector(query_tf)
    # Not all terms are found in inverted index, return empty
    if query_vector is None:
        return []

    # Find all the docs that contain all of the query words
    all_docs = get_query_docs(query_tf)
    # If no doc w/ all terms is found, return empty
    if all_docs is None:
        return []

    # key is the docid, the value is the doc's vector
    doc_vectors_dict = calc_doc_vector(all_docs, query_tf)
    tf_idf_dict = calc_tf_idf(query_vector, doc_vectors_dict)
    # list of tuples (docid, score)
    sorted_weighted_scores = calc_weighted_score(tf_idf_dict, weight)
    # get the hits in the right format for json
    results_formatted = []
    for results in sorted_weighted_scores:
        results_formatted.append({
            "docid": int(results[0]),
            "score": results[1]
        })

    return results_formatted


# -----------------     get_hit_results helpers    ----------------- #
def count_query_tf(query):
    """Find the freq of each word in the query."""
    term_dict = {}
    for term in query:
        # The frequency will be stored in [0] in the term's value's list
        if term in term_dict:
            term_dict[term] += 1
        else:
            term_dict[term] = 1
    return term_dict


def get_query_docs(query):
    """Get all the docs that contain all of the query terms and idfs."""
    # inverted_index: {"term": "line in doc", "term": "line in doc", etc}
    global inverted_index

    docs_combined = []
    for term in query:
        doc_term_set = set()
        if term in inverted_index:
            docs = inverted_index[term]['docs']
            # loop through all doc ids and add them to the set of all this
            # term's documents
            # docid is the key of the dictonary within doc
            for docid in docs:
                # e.g. {1, 2, 3} or {3, 4, 5}
                doc_term_set.add(docid)
        # e.g. [{1, 2, 3}, {3, 4, 5}]
        docs_combined.append(doc_term_set)
    # creates a new set of only the docids that are featured in all the sets
    # e.g. [{1, 2, 3}, {3, 4, 5}] --> {3}
    # the * is necessary bc you have to unpack all the sets to pass them in
    # as separate arguments
    full_query_docs = set.intersection(*docs_combined)

    return full_query_docs


def calc_query_vector(query):
    """Calculate query vector using query term frequencies and idfs."""
    global inverted_index
    # The query vector has one position for each term.
    # Each position is calculated as tf in query * idf
    query_vector = []

    for term, freq in query.items():
        # If term doesn't exist in inverted index, no hits can be found
        if term not in inverted_index:
            return None
        # Get the idf from the inverted_index
        idf = float(inverted_index[term]["idf"])
        one_position = freq * idf
        query_vector.append(one_position)
    return query_vector


def calc_doc_vector(all_docid_set, query_dict):
    """Calculate all the document vectors for all the docs in the set."""
    global inverted_index
    # The document vector has one position for each term
    # Each position in the vector is calculated as tf in doc i * idf
    all_docs_dict = {}

    for docid in all_docid_set:
        single_doc_vec = []
        first_iter = True
        doc_norm = 0
        # Need all the term's idf and tf in doc i
        for term in query_dict:
            curr_idf = float(inverted_index[term]["idf"])
            # Will this work?
            # idk, if I had time I'd make the dic sys less complicated
            curr_tf = inverted_index[term]["docs"][docid]["tf"]
            curr_pos = curr_idf * curr_tf
            single_doc_vec.append(curr_pos)

            # only needs to be done once
            if first_iter:
                # still need to get doc norm fac for next step
                doc_norm = inverted_index[term]["docs"][docid]["norm_fac"]
                first_iter = False

        # Add the indiv doc vectors to the value of the docid's in the dict
        # and the corresponding doc's norm factor
        all_docs_dict[docid] = [single_doc_vec, doc_norm]

    return all_docs_dict


def calc_tf_idf(query_vec, doc_vec_dict):
    """Calculate the tf-idf score for all the documents."""
    global inverted_index
    tf_idf_dict = {}

    for docid, value in doc_vec_dict.items():
        # value[0] is the doc_vec, value[1] is the doc norm factor
        numerator_dot_prod = float(dot_prod(query_vec, value[0]))
        query_norm = calc_query_norm_fac(query_vec)
        doc_norm = math.sqrt(value[1])
        denominator_mult = float(query_norm * doc_norm)
        tf_idf = numerator_dot_prod / denominator_mult
        tf_idf_dict[docid] = tf_idf

    return tf_idf_dict


def calc_weighted_score(tf_idf_dict, weight):
    """Calc the weighted score for each doc w/ pagerank, tfidf, and weight."""
    global pagerank
    weighted_scores = []
    for docid, tf_idf in tf_idf_dict.items():
        pagerank_score = pagerank[docid]
        weighted_score = weight * pagerank_score + (1 - weight) * tf_idf
        weighted_scores.append((docid, weighted_score))

    # first tuple element is the docid, the second is the weighted score
    # this func sorts first, in descending order, by the value of the score
    # and then, if tied, by ascending docid
    ranked_list = sorted(weighted_scores, key=lambda x: (-x[1], int(x[0])))
    return ranked_list


# -----------------     calc_tf_idf helpers    ----------------- #
def dot_prod(vec_a, vec_b):
    """Calculate the dot product of two vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same length, error earlier")

    dot_product = 0
    for i in range(len(vec_a)):
        dot_product += vec_a[i] * vec_b[i]
    return dot_product


def calc_query_norm_fac(vector):
    """Calculate the sqrt of the sum of squares of a vector."""
    sum_of_squares = 0
    for element in vector:
        sum_of_squares += element ** 2

    return math.sqrt(sum_of_squares)
