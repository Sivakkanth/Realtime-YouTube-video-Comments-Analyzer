import re
from textblob import TextBlob

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@[\w]+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def classify_comments(comments_data):
    classified = []

    for comment in comments_data:
        raw_text = comment.get('text', '')
        cleaned = clean_text(raw_text)

        if not cleaned:
            continue  # Skip empty or meaningless comments

        polarity = TextBlob(cleaned).sentiment.polarity
        status = 'p' if polarity >= 0 else 'n'

        classified.append({
            "author": comment.get("author", ""),
            "text": raw_text.strip(),
            "likes": comment.get("likes", 0),
            "time": comment.get("time", ""),
            "status": status
        })

    return classified