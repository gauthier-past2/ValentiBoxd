# pyright: ignore
import csv
import requests
from tmdbv3api import TMDb, Movie
import io

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

TMDB_API_KEY = '57e348eaabf19268d7be8c46b47ec6d4'


def search_tmdb(title):
    response = requests.get(
        "https://api.themoviedb.org/3/search/movie",
        params={"query": title, "api_key": TMDB_API_KEY, "language": "en-US"}
    )
    results = response.json().get("results", [])
    if not results:
        return None
    best = results[0]
    return (
        best["title"],
        best.get("release_date", "")[:4],
        best["id"]
    )


def MakeCSV(titles):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Title", "Year", "TMDbID"])

    for title in titles:
        result = search_tmdb(title)
        if result:
            writer.writerow(result)
        else:
            writer.writerow([title, "", ""])

    return output.getvalue()
