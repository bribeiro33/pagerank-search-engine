# Scalable Search Engine
## Key Features
- MapReduce pipeline to build a segmented inverted index
- Implementation of a REST API for the index server
- Integration of tf-idf and PageRank algorithms
- Parallel data processing for efficient information retrieval
- Deployment of multiple Index servers for scalability
- User interface for search functionality
- Client-side dynamic page updates
- Pytest as testing framework
- Passes pylint, pycodestyle, pydocstyle
- Bash scripts to simplify running index server, search server, and search database

![image](https://github.com/bribeiro33/pagerank-search-engine/assets/53235549/575760e0-8c40-49ae-9bd5-0e29fca07e47)


## Key files
1. **inverted_index**
- map[0-5].py
- reduce[0-5].py
- pipeline.sh
2. **index_server**
- index/api/main.py
3. **search_server**
- templates/index.html
- views/main.py

## How to run

### Run Bash Scripts
1. **Install dependencies:** ```./bin/install ```
2. **Run the Pipeline** ```./pipeline.sh input```
3. **Manage Index Servers** 
- Start: ```./bin/index start```
- Stop: ```./bin/index stop```
- Restart: ```./bin/index restart```
- Status: ```./bin/index status```
4. **Database Management for Search Server**
- Create: ```./bin/searchdb create```
- Destroy: ```./bin/searchdb destroy```
- Reset: ```./bin/searchdb reset```
5. **Manage Search Server**
- Start: ```./bin/search start```
- Stop: ```./bin/search stop```
- Restart: ```./bin/search restart```
- Status: ```./bin/search status```

### Run Individual Commands
1. **Run Index Server (can run multiple, use different ports):**
    ```
   INDEX_PATH="inverted_index_0.txt" flask --app index --debug run --host 0.0.0.0 --port 9000
    ```
3. **Create Database:**
    ```
    mkdir -p var/
    sqlite3 var/search.sqlite3 < search_server/search/sql/search.sql
    ```
4. **Query Index Server for "web" with a PageRank weight of 0.3:**
    ```
   http "localhost:9000/api/v1/hits/?w=0.3&q=web"
    ```
5. **Run Search Server:**
    ```
   flask --app search --debug run --host 0.0.0.0 --port 8000
    ```

