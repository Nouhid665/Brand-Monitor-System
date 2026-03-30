import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_mention(title, content):
    text = f"Title: {title}\nContent: {content}"

    prompt = f"""
You are a brand sentiment analyzer.

Analyze the following text and respond in this exact format, nothing else:
SENTIMENT: positive/negative/neutral
SCORE: (a number from 0 to 10, where 0 is very negative and 10 is very positive)
SUMMARY: (one sentence summary of what this is about)

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.choices[0].message.content

    lines = result_text.strip().split("\n")
    sentiment = "neutral"
    score = 5.0
    summary = ""

    for line in lines:
        if line.startswith("SENTIMENT:"):
            sentiment = line.replace("SENTIMENT:", "").strip().lower()
        elif line.startswith("SCORE:"):
            try:
                score = float(line.replace("SCORE:", "").strip())
            except:
                score = 5.0
        elif line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()

    return {
        "sentiment": sentiment,
        "score": score,
        "summary": summary
    }