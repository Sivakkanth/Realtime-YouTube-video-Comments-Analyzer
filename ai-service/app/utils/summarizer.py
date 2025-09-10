from models.summary_model import summarizer_model
import pandas as pd

def chunk_by_tokens(text, max_tokens=900):
    return [text]

def summarize_comments(comments):
    texts = [
        c['text'].strip()
        for c in comments
        if isinstance(c.get('text'), str) and c['text'].strip()
    ]
    if not texts:
        return "No valid comment text to summarize."

    # Optional: combine all comments
    combined_text = " ".join(texts)

    # Use MLflow model
    df = pd.DataFrame({"text": [combined_text]})
    try:
        summary_list = summarizer_model.predict(df)
        return summary_list[0]
    except Exception as e:
        return f"Error generating summary: {str(e)}"