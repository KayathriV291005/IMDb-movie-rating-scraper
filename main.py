import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.imdb.com/chart/top/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

movies = soup.select(".ipc-metadata-list-summary-item")

rank_list = []
title_list = []
year_list = []
rating_list = []
url_list = []

print("\n===== IMDb TOP 25 MOVIES =====\n")

for i, movie in enumerate(movies, start=1):

    # Title
    title_raw = movie.select_one(".ipc-title__text").text.strip()
    title = title_raw.split('. ', 1)[-1]   # remove rank prefix

    # Year
    year = movie.select_one(".cli-title-metadata-item").text.strip()

    # Rating
    rating = movie.select_one(".ipc-rating-star--rating").text.strip()

    # URL
    link = movie.select_one("a")["href"]
    full_url = "https://www.imdb.com" + link.split("?")[0]

    # Print in IDLE
    print(f"{i}. {title} ({year}) - Rating: {rating}")

    # Save to list
    rank_list.append(i)
    title_list.append(title)
    year_list.append(year)
    rating_list.append(rating)
    url_list.append(full_url)

# Convert to CSV
df = pd.DataFrame({
    "Rank": rank_list,
    "Title": title_list,
    "Year": year_list,
    "Rating": rating_list,
    "URL": url_list
})

df.to_csv("imdb_top_25_movies.csv", index=False)

print("\nCSV Saved Successfully → imdb_top_25_movies.csv")
