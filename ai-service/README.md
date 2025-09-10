# AI Service (FastAPI + Hugging Face Model)

This service provides:
- YouTube comment extraction
- Sentiment analysis
- Positive score calculation
- Suggestions & summarization

---

## 🚀 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI app
uvicorn main:app --reload --host 0.0.0.0 --port 8000