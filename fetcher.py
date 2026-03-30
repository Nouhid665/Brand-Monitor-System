import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_hackernews(brand):
    url = f"https://hn.algolia.com/api/v1/search?query={brand}&hitsPerPage=30"
    response = requests.get(url)
    data = response.json()

    results = []
    for hit in data["hits"]:
        title = hit.get("title") or hit.get("story_title") or ""
        content = hit.get("comment_text") or hit.get("story_text") or ""
        
        # only include if brand name actually appears in title or content
        combined = (title + " " + content).lower()
        if brand.lower() in combined:
            results.append({
                "source": "hackernews",
                "title": title,
                "content": content,
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            })
    return results


def fetch_newsapi(brand):
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={brand}&language=en&sortBy=relevancy&pageSize=30&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    results = []
    for article in data.get("articles", []):
        title = article.get("title") or ""
        content = article.get("description") or ""
        
        # only include if brand name actually appears
        combined = (title + " " + content).lower()
        if brand.lower() in combined:
            results.append({
                "source": "newsapi",
                "title": title,
                "content": content,
                "url": article.get("url") or ""
            })
    return results


def fetch_all(brand):
    hn_results = fetch_hackernews(brand)
    news_results = fetch_newsapi(brand)
    return hn_results + news_results