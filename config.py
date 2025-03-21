import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.pickle")
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")

# Create directories if they don't exist
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(os.path.join(ASSETS_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(ASSETS_DIR, "music"), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Fixed this line

# YouTube API settings
YOUTUBE_API_SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly'
]

# Content generation settings
DEFAULT_FACT_COUNT = 10
DEFAULT_SCRIPT_FORMAT = "Conversational"
DEFAULT_VIDEO_STYLE = "standard"
