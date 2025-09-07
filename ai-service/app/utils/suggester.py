from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from pathlib import Path

# Load the fine-tuned model and tokenizer from the saved directory
model_path = Path(__file__).parent.parent / "suggesion_model"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

def generate_suggestions(comments):
    texts = [
        c['text'].strip()
        for c in comments
        if isinstance(c.get('text'), str) and c['text'].strip()
    ]
    if not texts:
        return ["No valid comment text to suggest."]

    combined = " ".join(texts)
    # Tokenize the input text
    inputs = tokenizer(
        combined,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )

    # Generate the summary with adjusted parameters
    summary_ids = model.generate(
        inputs['input_ids'],
        max_length=50, # A shorter max length
        min_length=10, # A more reasonable minimum length
        num_beams=4,
        no_repeat_ngram_size=3, # Prevent repeating n-grams
        early_stopping=True
    )

    # Decode the generated tokens back to text
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return [summary]