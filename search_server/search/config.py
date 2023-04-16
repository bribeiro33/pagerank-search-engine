import pathlib
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

DATABASE_FILENAME = ROOT_DIR / "var" / "search.sqlite3"
