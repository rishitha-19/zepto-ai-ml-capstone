import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
books = []

for page in range(1, 6):  # scrape first 5 pages
    res = requests.get(BASE_URL.format(page))
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".product_pod")
    for item in items:
        title = item.h3.a["title"]
        price = item.select_one(".price_color").text.strip("£")
        rating = item.p["class"][1]  # e.g. "Three"
        availability = item.select_one(".availability").text.strip()
        books.append([title, price, rating, availability, "All"])

df = pd.DataFrame(books, columns=["title","price_gbp","star_rating","availability","category"])
df["price_gbp"] = df["price_gbp"].astype(float)
rating_map = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}
df["rating"] = df["star_rating"].map(rating_map)
df["in_stock"] = df["availability"].str.contains("In stock")
df["price_inr"] = df["price_gbp"] * 105.50

# SQLite schema
conn = sqlite3.connect("books.db")
df.to_sql("books", conn, if_exists="replace", index=False)
conn.commit()
