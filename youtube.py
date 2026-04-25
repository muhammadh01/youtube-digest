import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

YOUTUBE_PATTERN = r"https?://(www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+"


class YouTubeVideo:
    def __init__(self, url):
        if not re.match(YOUTUBE_PATTERN, url):
            raise ValueError("Invalid YouTube URL. Expected format: https://www.youtube.com/watch?v=...")

        self.url = url
        self.video_id = url.split("v=")[1].split("&")[0]

        response = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No title"

        transcript_data = YouTubeTranscriptApi().fetch(self.video_id)
        self.transcript = " ".join([segment.text for segment in transcript_data])
