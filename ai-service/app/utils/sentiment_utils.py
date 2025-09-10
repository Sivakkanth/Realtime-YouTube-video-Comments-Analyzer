import re
import pandas as pd
from typing import List, Dict
import asyncio
from models.sentiment_model import sentiment_model

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@[\w]+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def classify_comments(comments_data: List[Dict]) -> List[Dict]:
    async def classify_single_comment(comment: Dict) -> Dict | None:
        text = comment.get("text", "")
        cleaned = clean_text(text)
        if not cleaned:
            return None

        try:
            df = pd.DataFrame({"text": [cleaned]})
            prediction = await asyncio.to_thread(sentiment_model.predict, df)
            label = prediction[0].lower()

            if label == "positive":
                status = "p"
            elif label == "negative":
                status = "n"
            else:
                return None
        except Exception:
            status = "n"

        return {
            "author": comment.get("author", ""),
            "text": cleaned,
            "likes": comment.get("likes", 0),
            "time": comment.get("published_at", ""),
            "status": status
        }
    tasks = [classify_single_comment(c) for c in comments_data]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]