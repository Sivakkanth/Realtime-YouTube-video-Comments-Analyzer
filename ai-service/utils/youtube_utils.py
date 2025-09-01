import re
from youtube_comment_downloader import YoutubeCommentDownloader
from datetime import datetime

def extract_video_id(url):
    patterns = [
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL format.")


def get_comments(video_url):
    downloader = YoutubeCommentDownloader()
    comments = []

    try:
        comments_generator = downloader.get_comments_from_url(video_url, sort_by=1)

        for item in comments_generator:
            # Convert likes to int
            likes = int(item.get("votes", 0))

            # Convert time_parsed (float) to ISO string
            published_at = None
            if item.get("time_parsed"):
                published_at = datetime.utcfromtimestamp(
                    item["time_parsed"]
                ).isoformat() + "Z"

            comment_data = {
                "author": item.get("author", ""),
                "text": item.get("text", ""),
                "likes": likes,
                "published_at": published_at
            }
            comments.append(comment_data)

    except Exception as e:
        raise RuntimeError(f"Failed to fetch comments: {e}")

    return comments
