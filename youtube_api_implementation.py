"""
YouTube API Integration with Refresh Token Authentication
This module provides a more robust implementation for YouTube API integration
that doesn't require browser interaction after initial setup.
"""

import os
import pickle
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes required for YouTube API - using minimal scopes to reduce risk of account shutdown
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',  # For uploading videos
    'https://www.googleapis.com/auth/youtube.readonly'  # For reading channel info
]

class YouTubeAPIRefreshToken:
    """YouTube API wrapper using refresh token authentication"""
    
    def __init__(self, client_secrets_file=None, token_file='youtube_token.pickle'):
        """Initialize the YouTube API client"""
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self.credentials = None
        self.youtube = None
        
    def authenticate_with_browser(self):
        """
        Perform one-time authentication with browser to get refresh token
        This only needs to be done once, then the refresh token can be used
        for future authentication without browser interaction
        """
        if not self.client_secrets_file:
            raise ValueError("Client secrets file is required for initial authentication")
            
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, SCOPES)
        
        # Run the OAuth flow to get refresh token
        credentials = flow.run_local_server(port=8501)
        
        # Save credentials to file
        with open(self.token_file, 'wb') as token:
            pickle.dump(credentials, token)
            
        self.credentials = credentials
        return credentials
        
    def authenticate(self):
        """
        Authenticate with YouTube API using saved refresh token
        This can be done without browser interaction
        """
        credentials = None
        
        # Check if token file exists
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                credentials = pickle.load(token)
                
        # If no valid credentials available, need initial browser auth
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                # If we have a refresh token, use it to get a new access token
                credentials.refresh(Request())
                
                # Save refreshed credentials
                with open(self.token_file, 'wb') as token:
                    pickle.dump(credentials, token)
            else:
                # If no refresh token, need browser auth
                if not self.client_secrets_file:
                    raise ValueError(
                        "No valid credentials found. Run authenticate_with_browser() first "
                        "with a client_secrets_file to get a refresh token."
                    )
                credentials = self.authenticate_with_browser()
                
        self.credentials = credentials
        
        # Build the YouTube API client
        self.youtube = build('youtube', 'v3', credentials=credentials)
        return self.youtube
        
    def get_channel_info(self):
        """Get information about the authenticated user's channel"""
        if not self.youtube:
            self.authenticate()
            
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        
        if response.get('items'):
            return response['items'][0]
        return None
        
    def upload_video(self, file_path, title, description, tags=None, category_id="22", 
                    privacy_status="private", notify_subscribers=True):
        """Upload a video to YouTube"""
        if not self.youtube:
            self.authenticate()
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")
            
        tags = tags or []
        
        # Define video metadata
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            },
            "notifySubscribers": notify_subscribers
        }
        
        # Create the media upload object
        media = MediaFileUpload(file_path, resumable=True)
        
        # Execute the upload request
        request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )
        
        # Upload the video
        response = request.execute()
        return response
        
    def get_video_analytics(self, video_id):
        """Get analytics for a specific video"""
        if not self.youtube:
            self.authenticate()
            
        # Get basic video statistics
        request = self.youtube.videos().list(
            part="statistics",
            id=video_id
        )
        response = request.execute()
        
        if response.get('items'):
            return response['items'][0]['statistics']
        return None
        
    def get_channel_analytics(self):
        """Get analytics for the authenticated user's channel"""
        if not self.youtube:
            self.authenticate()
            
        # Get channel statistics
        request = self.youtube.channels().list(
            part="statistics",
            mine=True
        )
        response = request.execute()
        
        if response.get('items'):
            return response['items'][0]['statistics']
        return None
        
    def update_video_metadata(self, video_id, title=None, description=None, tags=None, 
                             category_id=None, privacy_status=None):
        """Update metadata for an existing video"""
        if not self.youtube:
            self.authenticate()
            
        # Get current video details
        request = self.youtube.videos().list(
            part="snippet,status",
            id=video_id
        )
        response = request.execute()
        
        if not response.get('items'):
            raise ValueError(f"Video not found with ID: {video_id}")
            
        video = response['items'][0]
        snippet = video['snippet']
        status = video['status']
        
        # Update fields if provided
        if title:
            snippet['title'] = title
        if description:
            snippet['description'] = description
        if tags:
            snippet['tags'] = tags
        if category_id:
            snippet['categoryId'] = category_id
        if privacy_status:
            status['privacyStatus'] = privacy_status
            
        # Update the video
        request = self.youtube.videos().update(
            part="snippet,status",
            body={
                "id": video_id,
                "snippet": snippet,
                "status": status
            }
        )
        
        response = request.execute()
        return response

# Example usage
def setup_youtube_api(client_secrets_file=None, token_file='youtube_token.pickle'):
    """
    Set up YouTube API with refresh token authentication
    
    Args:
        client_secrets_file: Path to client secrets JSON file (only needed for initial setup)
        token_file: Path to save/load the token pickle file
        
    Returns:
        YouTubeAPIRefreshToken instance
    """
    api = YouTubeAPIRefreshToken(client_secrets_file, token_file)
    
    try:
        # Try to authenticate with existing token
        api.authenticate()
        print("Successfully authenticated with existing token")
    except Exception as e:
        if client_secrets_file:
            print(f"Error authenticating with existing token: {str(e)}")
            print("Attempting to authenticate with browser...")
            api.authenticate_with_browser()
            print("Successfully authenticated with browser and saved refresh token")
        else:
            raise ValueError(
                "No valid token found and no client_secrets_file provided. "
                "Please provide a client_secrets_file for initial setup."
            )
    
    return api

# Instructions for one-time setup
def generate_setup_instructions():
    """Generate instructions for one-time setup of YouTube API with refresh token"""
    instructions = """
# YouTube API Setup Instructions

## One-Time Setup (Required for Initial Authentication)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable the YouTube Data API v3
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" and select "OAuth client ID"
   - Select "Desktop app" as the application type
   - Name your OAuth client
   - Download the client secrets JSON file
5. Run the following code once to authenticate and generate a refresh token:

```python
from youtube_api_implementation import setup_youtube_api

# Replace with the path to your downloaded client secrets file
client_secrets_file = "client_secret.json"

# This will open a browser window for authentication
api = setup_youtube_api(client_secrets_file)

# Test the connection
channel_info = api.get_channel_info()
print(f"Connected to channel: {channel_info['snippet']['title']}")
```

6. After completing this setup, a token file will be saved that contains your refresh token.
7. For future use, you can authenticate without browser interaction:

```python
from youtube_api_implementation import setup_youtube_api

# No client secrets file needed for subsequent runs
api = setup_youtube_api()

# Use the API
api.upload_video("my_video.mp4", "My Video Title", "Video description")
```

## Important Notes

- Keep your client secrets file and token file secure
- The refresh token is long-lived but not permanent
- If you get authentication errors after a long period, you may need to repeat the one-time setup
- Use minimal scopes to reduce the risk of account shutdown
"""
    return instructions

if __name__ == "__main__":
    # Generate setup instructions
    instructions = generate_setup_instructions()
    print(instructions)
