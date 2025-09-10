from models.suggester_model import suggester_model
import pandas as pd

def generate_suggestions(comments):
    texts = [
        c['text'].strip()
        for c in comments
        if isinstance(c.get('text'), str) and c['text'].strip() and c.get('status') == 'n'
    ]
    
    if not texts:
        return ["No valid comment text to suggest."]

    combined_text = " ".join(texts)
    print("Combined Negative Comments:", combined_text)

    df = pd.DataFrame({"text": [combined_text]})
    print("DataFrame passed to model:", df)

    try:
        suggestions = suggester_model.predict(df)
        if isinstance(suggestions, (list, tuple)):
            return suggestions
        return [str(suggestions)]
    except Exception as e:
        return [f"Error generating suggestions: {str(e)}"]