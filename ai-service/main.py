from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.youtube_utils import get_comments
from utils.sentiment_utils import classify_comments
from utils.calculate_positive_score_percentage import calculate_positive_score_percentage
from utils.summarizer import summarize_comments

app = FastAPI()

# ✅ Enable CORS for your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change to "*" for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    youtube_url: str

@app.post("/analyze")
def analyze_video(data: AnalyzeRequest):
    try:
        comments = get_comments(data.youtube_url)
        if not comments:
            raise HTTPException(status_code=400, detail="No comments found.")

        classified_comments = classify_comments(comments)
        score = calculate_positive_score_percentage(classified_comments)
        summary = summarize_comments(classified_comments)
        # suggestions = generate_suggestions(score, [c[0] for c in classified])

        return {
            "total_comments": len(comments),
            # "comments": classified_comments,
            "positive_score": score,
            "summary": summary["summary"],
            "suggestions": summary["suggestion"]
        }

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")