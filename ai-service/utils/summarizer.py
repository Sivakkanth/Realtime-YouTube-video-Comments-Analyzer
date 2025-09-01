from transformers import pipeline

# Load the summarization model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

def summarize_comments(comments):
    """
    Analyzes YouTube comments:
    1. Summarizes the text of all comments.
    """
    # Step 1: Collect all valid comment texts
    texts = [
        c['text'].strip()
        for c in comments
        if isinstance(c.get('text'), str) and c['text'].strip()
    ]

    if not texts:
        return "No valid comment text to summarize."

    # Step 2: Combine and truncate to stay within summarization limits
    combined = " ".join(texts)
    combined = " ".join(combined.split()[:700])  # Limit to approx. 700 words

    # Step 3: Generate summary
    summary_result = summarizer(combined, max_length=100, min_length=30, do_sample=False)

    return summary_result[0]["summary_text"]
