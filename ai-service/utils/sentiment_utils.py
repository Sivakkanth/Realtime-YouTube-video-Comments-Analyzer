import re
from textblob import TextBlob
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fastapi import HTTPException

MODEL_PATH = "D:\\d\\7\\EE7260_Advanced_Artificial_Intelligence\\final_project\\Realtime-YouTube-video-Comments-Analyzer\\ai-service\\my_model"

# Global variables for model and tokenizer
tokenizer = None
model = None
device = None

# Load the model and tokenizer from the local folder
def load_model():
    """Loads the sentiment analysis model and tokenizer."""
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
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
    
    predicted_class_id = probabilities.argmax(dim=1).item()
    
    label = model.config.id2label[predicted_class_id]
    
    return "p" if label == "LABEL_1" else "n"


def classify_comments(comments_data):
    classified = []

    for comment in comments_data:
        raw_text = comment.get('text', '')
        cleaned = clean_text(raw_text)

        if not cleaned:
            continue  # Skip empty or meaningless comments

        # polarity = TextBlob(cleaned).sentiment.polarity
        # status = 'p' if polarity >= 0 else 'n'
        status = predict_sentiment_text(cleaned)

        classified.append({
            "author": comment.get("author", ""),
            "text": raw_text.strip(),
            "likes": comment.get("likes", 0),
            "time": comment.get("time", ""),
            "status": status
        })

    return classified