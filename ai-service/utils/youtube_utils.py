import re
from googleapiclient.discovery import build

API_KEY = 'AIzaSyAFeLh0zf4l5WtGh5yqV8-klq3UaCyPPAk'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

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
    video_id = extract_video_id(video_url)
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
    comments = []
    next_page_token = None

    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText",
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comment_snippet = {
                    "authorDisplayName": comment["authorDisplayName"],
                    "textDisplay": comment["textDisplay"],
                    "likeCount": comment.get("likeCount", 0),
                    "publishedAt": comment["publishedAt"]
                }
                comment_data = {
                    "author": comment_snippet["authorDisplayName"],
                    "text": comment_snippet["textDisplay"],
                    "likes": comment_snippet["likeCount"],
                    "published_at": comment_snippet["publishedAt"]
                }
                comments.append(comment_data)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as e:
        raise RuntimeError(f"Failed to fetch comments: {e}")
    
    return comments