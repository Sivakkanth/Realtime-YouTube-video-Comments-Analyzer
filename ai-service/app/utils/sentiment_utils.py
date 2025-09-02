import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path
from typing import List, Dict
import asyncio

MODEL_PATH = Path(__file__).parent.parent / "my_model"

# Global variables for model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH))
model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_PATH))
device: str | None = None

# Load the model and tokenizer from the local folder
def load_model():
    global tokenizer, model, device
    try:
        print("Loading model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        print("Model loaded successfully!")
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        print(f"Using device: {device}")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise RuntimeError("Model could not be loaded. Check your MODEL_PATH and files.")

# Load model at application startup
load_model()

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@[\w]+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_sentiment_text(text: str) -> str:
    if not model or not tokenizer:
        raise Exception("Model or tokenizer not loaded. Please ensure they are initialized.")

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        predicted_id = torch.argmax(torch.softmax(logits, dim=1), dim=1).item()
        label = model.config.id2label[predicted_id]

    return "p" if label == "LABEL_1" else "n"


async def classify_comments(comments_data: List[Dict]) -> List[Dict]:
    async def classify_single_comment(comment: Dict) -> Dict | None:
        text = comment.get("text", "")
        cleaned = clean_text(text)
        if not cleaned:
            return None  # Skip empty comments

        try:
            # Run CPU-bound prediction in a thread
            status = await asyncio.to_thread(predict_sentiment_text, cleaned)
        except Exception:
            status = "n"  # fallback if prediction fails

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