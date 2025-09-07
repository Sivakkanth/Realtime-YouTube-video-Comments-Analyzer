import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.youtube_utils import get_all_comments, get_video_metadata
from utils.sentiment_utils import classify_comments
from utils.calculate_positive_score_percentage import calculate_positive_score_percentage
from utils.summarizer import summarize_comments
from utils.suggester import generate_suggestions;

app = FastAPI(title='YouTube Analyzer', version='1.0')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS for your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://realtime-you-tube-video-comments-an.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text: str

class AnalyzeRequest(BaseModel):
    youtube_url: str

@app.post("/analyze")
async def analyze_video(data: AnalyzeRequest):
    try:
        metadata_task = get_video_metadata(data.youtube_url) 
        comments_task = get_all_comments(data.youtube_url, sort_by=1)

        metadata, comments = await asyncio.gather(metadata_task, comments_task)

        if not comments:
            raise HTTPException(status_code=400, detail="No comments found.")

        classified_comments = await classify_comments(comments)
        score = calculate_positive_score_percentage(classified_comments)
        summary = summarize_comments(classified_comments)
        suggestions = generate_suggestions(classified_comments)

        return {
            "video_metadata": metadata,
            "total_comments": len(comments),
            # "comments": classified_comments,
            "positive_score": score,
            "summary": summary,
            "suggestions": suggestions
        }

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.exception("Error analyzing video")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/test")
def t():
    return "started project"