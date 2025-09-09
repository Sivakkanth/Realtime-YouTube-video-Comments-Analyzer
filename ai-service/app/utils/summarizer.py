from models.summary_model import summarizer_model
import pandas as pd

def chunk_by_tokens(text, max_tokens=900):
    # Keep the original tokenization if needed for splitting large text
    # or skip if using MLflow model that can handle large text
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

# from models.summary_model import summarizer, tokenizer

# def chunk_by_tokens(text, max_tokens=900):
#     """
#     Split text into chunks within tokenizer's max length.
#     """
#     tokens = tokenizer.encode(text, truncation=False)
#     chunks = []
#     for i in range(0, len(tokens), max_tokens):
#         chunk_tokens = tokens[i:i+max_tokens]
#         chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
#         if chunk_text.strip():
#             chunks.append(chunk_text)
#     return chunks

# def summarize_comments(comments):
#     """
#     Summarize YouTube comments safely without exceeding model's token limit.
#     """
#     texts = [
#         c['text'].strip()
#         for c in comments
#         if isinstance(c.get('text'), str) and c['text'].strip()
#     ]
#     if not texts:
#         return "No valid comment text to summarize."

#     combined = " ".join(texts)

#     # Step 1: Token-safe chunking
#     chunks = chunk_by_tokens(combined, max_tokens=900)

#     # Step 2: Summarize each chunk
#     partial_summaries = []
#     for ch in chunks:
#         try:
#             summary = summarizer(ch, max_length=150, min_length=30, do_sample=False)
#             partial_summaries.append(summary[0]["summary_text"])
#         except Exception as e:
#             print(f"Skipping chunk due to error: {e}")

#     if not partial_summaries:
#         return "Summarization failed for all chunks."

#     combined_summary = " ".join(partial_summaries)

#     # Step 3: Final summary
#     final = summarizer(
#         combined_summary,
#         max_length=150,
#         min_length=30,
#         do_sample=False,
#         batch_size=4
#     )

#     return final[0]["summary_text"]

# def summarize_comments(comments):
#     """
#     Analyzes YouTube comments:
#     1. Summarizes the text of all comments.
#     """
#     # Step 1: Collect all valid comment texts
#     texts = [
#         c['text'].strip()
#         for c in comments
#         if isinstance(c.get('text'), str) and c['text'].strip()
#     ]

#     if not texts:
#         return "No valid comment text to summarize."

#     # Step 2: Combine and truncate to stay within summarization limits
#     combined = " ".join(texts)
#     combined = " ".join(combined.split()[:700])  # Limit to approx. 700 words

#     # Step 3: Generate summary
#     summary_result = summarizer(combined, max_length=100, min_length=30, do_sample=False)

#     return summary_result[0]["summary_text"]