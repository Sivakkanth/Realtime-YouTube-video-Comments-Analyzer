from transformers import pipeline

# Load the summarization model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

def summarize_comments(comments):
    """
    Analyzes YouTube comments:
    1. Summarizes the text of all comments.
    2. Generates suggestions to improve video quality.
    """
    # Step 1: Collect all valid comment texts
    texts = [
        c['text'].strip()
        for c in comments
        if isinstance(c.get('text'), str) and c['text'].strip()
    ]

    if not texts:
        return {
            "summary": "No valid comment text to summarize.",
            "suggestion": "Cannot generate suggestions due to lack of content."
        }

    # Step 2: Combine and truncate to stay within summarization limits
    combined = " ".join(texts)
    combined = " ".join(combined.split()[:700])  # Limit to approx. 700 words

    # Step 3: Generate summary
    if len(combined.split()) < 30:
        return {
            "summary": combined,
            "suggestion": "Try to gather more meaningful comments to extract actionable insights."
        }

    summary_result = summarizer(combined, max_length=100, min_length=30, do_sample=False)
    summary = summary_result[0]['summary_text']

    # Step 4: Generate suggestion based on the summary
    suggestion_prompt = f"""
You are a professional YouTube content strategist.

Given this summary of YouTube comments:
\"\"\"{summary}\"\"\"

Please generate detailed suggestions to improve the video based on what viewers are expressing.
"""

    suggestion = generate_ai_suggestion(suggestion_prompt)

    return {
        "summary": summary,
        "suggestion": suggestion
    }

# Mock function (replace with GPT/OpenAI API if needed)
def generate_ai_suggestion(prompt):
    return (
        "The comments indicate a need for clearer context or more engaging presentation. "
        "You may consider adding timestamps, improving video titles or descriptions, and responding to viewer questions directly in the content."
    )