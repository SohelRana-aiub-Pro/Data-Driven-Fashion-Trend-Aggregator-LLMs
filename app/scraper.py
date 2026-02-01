# app/scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_trends():
    url = "https://www.vogue.com/fashion/trends"  # example public source
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    articles = []
    for item in soup.select("article h2"):
        articles.append(item.get_text(strip=True))
    return articles
#