"""
YouTube API Integration for Streamlit Application
"""

import os
import sys
import pickle
from pathlib import Path
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# Scopes required for YouTube API
# If modifying these scopes, delete the file token.pickle
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

class YouTubeAPI:
    """YouTube API wrapper for content automation"""
    
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        """Initialize the YouTube API client"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.credentials = None
        self.youtube = None
        
    def create_client_config(self):
        """Create client configuration from provided credentials"""
        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and Client Secret are required")
            
        client_config = {
            "installed": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uris": [self.redirect_uri or "https://youtube-automation-backwnd-4.onrender.com/oauth2callback"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        return client_config
        
    def authenticate(self, token_path='token.pickle') :
    """Authenticate with YouTube API using OAuth2"""
    credentials = None
    
    # Check if token file exists
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            credentials = pickle.load(token)
            
    # If credentials are invalid or don't exist, get new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            client_config = self.create_client_config()
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
                client_config, SCOPES)
                
            # Instead of run_local_server, use a different approach for web apps
            # This will require implementing a route in your app to handle the OAuth callback
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            # In a web app, you would redirect to auth_url and handle the callback
            # For now, we'll just print the URL and ask the user to manually authorize
            print(f"Please go to this URL and authorize the app: {auth_url}")
            auth_code = input("Enter the authorization code: ")
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
                
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(credentials, token)
                
    self.credentials = credentials
    
    # Build the YouTube API client
    self.youtube = googleapiclient.discovery.build(
        'youtube', 'v3', credentials=credentials)
        
    return self.youtube
        
    def get_channel_info(self):
        """Get information about the authenticated user's channel"""
        if not self.youtube:
            raise ValueError("YouTube API client not authenticated. Call authenticate() first.")
            
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
            raise ValueError("YouTube API client not authenticated. Call authenticate() first.")
            
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
            raise ValueError("YouTube API client not authenticated. Call authenticate() first.")
            
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
            raise ValueError("YouTube API client not authenticated. Call authenticate() first.")
            
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
            raise ValueError("YouTube API client not authenticated. Call authenticate() first.")
            
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
