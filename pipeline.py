import time
from database import create_db, insert_mention, get_mentions
from fetcher import fetch_all
from analyzer import analyze_mention

def run_pipeline(brand):
    print(f"Fetching mentions for: {brand}")
    
    mentions = fetch_all(brand)
    print(f"Total fetched: {len(mentions)}")

    for i, mention in enumerate(mentions):
        print(f"Analyzing {i+1}/{len(mentions)}: {mention['title'][:50]}")
        
        try:
            analysis = analyze_mention(mention["title"], mention["content"])
            insert_mention(
                brand=brand,
                source=mention["source"],
                title=mention["title"],
                content=mention["content"],
                url=mention["url"],
                sentiment=analysis["sentiment"],
                score=analysis["score"]
            )
        except Exception as e:
            print(f"Skipping mention due to error: {e}")
            continue
        
        time.sleep(1)  # give Ollama breathing room

    print("Done!")
    return get_mentions(brand)