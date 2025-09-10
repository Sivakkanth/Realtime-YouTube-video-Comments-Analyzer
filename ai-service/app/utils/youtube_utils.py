import re
import json
import httpx
import logging
import asyncio
from datetime import datetime
from typing import List, Dict
from urllib.parse import urlparse, parse_qs
from youtube_comment_downloader import YoutubeCommentDownloader
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
executor = ThreadPoolExecutor()

# def extract_video_id(url: str) -> str:
#     patterns = [
#         r"youtu\.be/([a-zA-Z0-9_-]{11})",
#         r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
#         r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, url)
#         if match:
#             return match.group(1)
#     logger.error(f"Invalid YouTube URL provided: {url}")
#     raise ValueError("Invalid YouTube URL format.")


def convert_youtube_url(short_url):
    """
    Converts a youtu.be URL to a standard YouTube watch URL.
    """
    # Regex to find the video ID after youtu.be/
    video_id_match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', short_url)
    if video_id_match:
        video_id = video_id_match.group(1)
        return f'https://www.youtube.com/watch?v={video_id}'
    return None

def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    # Case 1: youtu.be short links
    if "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")

    # Case 2: youtube.com/watch?v=...
    if "youtube.com" in parsed.netloc:
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]
        # Case 3: shorts URL
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
        # Case 4: embed URL
        match = re.match(r"^/embed/([a-zA-Z0-9_-]{11})", parsed.path)
        if match:
            return match.group(1)

    logger.error(f"Invalid YouTube URL provided: {url}")
    raise ValueError("Invalid YouTube URL format.")

async def get_video_metadata(url: str) -> dict:
    video_id = extract_video_id(url)
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(video_url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch video page: {resp.status_code}")

    html = resp.text

    match = re.search(r'var ytInitialPlayerResponse = ({.*?});', html)
    if not match:
        raise ValueError("Could not find video details in page.")

    data = json.loads(match.group(1))
    video_details = data.get("videoDetails", {})

    return {
        "video_id": video_details.get("videoId"),
        "title": video_details.get("title"),
        "author": video_details.get("author"),
        "short_description": video_details.get("shortDescription"),
        "view_count": video_details.get("viewCount"),
        "length_seconds": video_details.get("lengthSeconds"),
        "keywords": video_details.get("keywords"),
        "channel_id": video_details.get("channelId"),
    }

def parse_likes(like_str: str) -> int:
    try:
        s = str(like_str).strip().upper().replace(',', '')
        if s.endswith('K'):
            return int(float(s[:-1]) * 1_000)
        elif s.endswith('M'):
            return int(float(s[:-1]) * 1_000_000)
        elif s.isdigit():
            return int(s)
        else:
            # fallback for unexpected chars
            cleaned = ''.join(c for c in s if c.isdigit())
            return int(cleaned) if cleaned else 0
    except Exception:
        return 0

def _blocking_get_all_comments(video_url: str, sort_by: int = 1) -> List[Dict]:
    downloader = YoutubeCommentDownloader()
    comments: List[Dict] = []

    for item in downloader.get_comments_from_url(video_url, sort_by=sort_by):
        likes = parse_likes(item.get("votes", 0))
        published_at = None
        if item.get("time_parsed"):
            published_at = datetime.utcfromtimestamp(item["time_parsed"]).isoformat() + "Z"
        comments.append({
            "author": item.get("author", ""),
            "text": item.get("text", "").strip(),
            "likes": likes,
            "published_at": published_at
        })

    logger.info(f"Fetched {len(comments)} comments from {video_url}")
    return comments

async def get_all_comments(video_url: str, sort_by: int = 1) -> List[Dict]:
    return await asyncio.to_thread(_blocking_get_all_comments, video_url, sort_by)