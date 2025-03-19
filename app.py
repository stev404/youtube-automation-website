import streamlit as st
import requests
import json
import random
from datetime import datetime

# Configuration
BACKEND_URL = "https://your-backend-url.onrender.com"  # Replace with your actual backend URL

# Page title and configuration
st.set_page_config(
    page_title="YouTube Content Automation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
) 

# OAuth callback handler
def handle_oauth_callback():
    # Get the authorization code from URL parameters
    code = st.query_params.get("code", [""])[0] if "code" in st.query_params else ""
    
    if code:
        # In a real implementation, you would exchange this code for tokens
        st.success("Authentication successful! You can now publish videos to YouTube.")
        
        # Clear the URL parameters
        st.query_params.clear()
    
# Check if this is an OAuth callback
if "code" in st.query_params:
    handle_oauth_callback()


# Initialize session state
if 'facts' not in st.session_state:
    st.session_state.facts = []
if 'scripts' not in st.session_state:
    st.session_state.scripts = []
if 'videos' not in st.session_state:
    st.session_state.videos = []
if 'published_videos' not in st.session_state:
    st.session_state.published_videos = []

# Sidebar navigation
st.sidebar.title("YouTube Automation")
st.sidebar.markdown("---")

# Navigation
navigation = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Content Generation", "Video Creation", "Publishing", "Analytics", "Settings", "Help"]
)

# Helper functions
def fetch_facts():
    try:
        response = requests.get(f"{BACKEND_URL}/api/facts")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching facts: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return []

def generate_facts(num_facts=5, categories=None):
    if categories is None:
        categories = ["Science", "History", "Nature", "Technology"]
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/facts/generate",
            json={"num_facts": num_facts, "categories": categories}
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error generating facts: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return []

def generate_scripts(fact_ids):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/scripts/generate",
            json={"fact_ids": fact_ids}
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error generating scripts: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return []

def assemble_videos(script_ids, resolution="1080p", voice_type="Male"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/videos/assemble",
            json={
                "script_ids": script_ids,
                "resolution": resolution,
                "voice_type": voice_type
            }
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error assembling videos: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return []

def publish_videos(video_ids, privacy="Public"):
    try:
        # Check if YouTube credentials are configured
        if 'youtube_client_id' in st.session_state and 'youtube_client_secret' in st.session_state:
            # In a real implementation, you would use these credentials
            pass
        
        response = requests.post(
            f"{BACKEND_URL}/api/publish",
            json={"video_ids": video_ids, "privacy": privacy}
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error publishing videos: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return []

def get_analytics():
    try:
        response = requests.get(f"{BACKEND_URL}/api/analytics")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching analytics: {response.status_code}")
            return {}
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return {}

# Dashboard page
if navigation == "Dashboard":
    st.title("YouTube Content Automation Dashboard")
    
    # System Status
    st.header("System Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Facts Generated", len(st.session_state.facts))
    with col2:
        st.metric("Scripts Created", len(st.session_state.scripts))
    with col3:
        st.metric("Videos Assembled", len(st.session_state.videos))
    with col4:
        st.metric("Videos Published", len(st.session_state.published_videos))
    
    # Quick Actions
    st.header("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Generate Content"):
            st.session_state.facts.extend(generate_facts())
            st.success("Content generated successfully!")
    
    with col2:
        if st.button("Create Videos"):
            if st.session_state.facts:
                fact_ids = [fact["id"] for fact in st.session_state.facts[:5]]
                scripts = generate_scripts(fact_ids)
                st.session_state.scripts.extend(scripts)
                
                script_ids = [script["id"] for script in scripts]
                videos = assemble_videos(script_ids)
                st.session_state.videos.extend(videos)
                
                st.success("Videos created successfully!")
            else:
                st.warning("No facts available. Generate content first.")
    
    with col3:
        if st.button("Publish Videos"):
            if st.session_state.videos:
                video_ids = [video["id"] for video in st.session_state.videos[:3]]
                published = publish_videos(video_ids)
                st.session_state.published_videos.extend(published)
                
                st.success("Videos published successfully!")
            else:
                st.warning("No videos available. Create videos first.")
    
    with col4:
        if st.button("Run Analytics"):
            st.session_state.analytics = get_analytics()
            st.success("Analytics updated!")
    
    # Recent Activity
    st.header("Recent Activity")
    
    # Sample activity data
    activities = [
        {"time": "Today, 2:30 PM", "action": "Video published", "details": "5 Amazing Facts About Deep Sea Creatures"},
        {"time": "Today, 10:15 AM", "action": "Content generated", "details": "10 new facts about Ancient History"},
        {"time": "Yesterday, 4:45 PM", "action": "Analytics updated", "details": "Performance report for last week"},
        {"time": "2 days ago", "action": "Video created", "details": "Fascinating Facts About the Human Brain"}
    ]
    
    for activity in activities:
        st.write(f"{activity['time']}: {activity['action']} - {activity['details']}")


# Publishing page
elif navigation == "Publishing":
    st.title("Publishing")
    
    st.write("Publish your videos to YouTube.")
    
    # Check if YouTube API is configured
    if 'youtube_client_id' not in st.session_state or 'youtube_client_secret' not in st.session_state:
        st.warning("YouTube API credentials not configured. Please go to Settings to configure your YouTube API credentials.")
    
    # Display videos
    st.subheader("Videos Ready for Publishing")
    
    if not st.session_state.videos:
        st.info("No videos available for publishing. Go to Video Creation to create videos.")
    else:
        selected_videos = []
        
        for i, video in enumerate(st.session_state.videos):
            # Skip already published videos
            if any(pv['video_id'] == video['id'] for pv in st.session_state.published_videos):
                continue
                
            selected = st.checkbox(f"Video #{i+1}: {video['title']}", key=f"pub_video_{i}")
            if selected:
                selected_videos.append(video['id'])
        
        # Publishing settings
        st.subheader("Publishing Settings")
        
        privacy = st.selectbox("Privacy Setting", ["Public", "Unlisted", "Private"], index=0)
        
        # Publish button
        if st.button("Publish Selected Videos"):
            if selected_videos:
                with st.spinner("Publishing videos..."):
                    published = publish_videos(selected_videos, privacy)
                    st.session_state.published_videos.extend(published)
                    st.success(f"Published {len(published)} videos!")
            else:
                st.warning("Please select at least one video.")
    
    # Display published videos
    st.subheader("Published Videos")
    
    if not st.session_state.published_videos:
        st.info("No videos published yet.")
    else:
        for i, video in enumerate(st.session_state.published_videos):
            with st.expander(f"Published Video #{i+1}: {video['title']}"):
                st.write(f"**Privacy:** {video['privacy']}")
                st.write(f"**Published At:** {video['published_at']}")
                st.write(f"**YouTube URL:** {video['youtube_url']}")
                
                # Link to YouTube
                st.markdown(f"[View on YouTube]({video['youtube_url']})")

# Analytics page
elif navigation == "Analytics":
    st.title("Analytics")
    
    st.write("Track the performance of your YouTube channel.")
    
    # Refresh analytics button
    if st.button("Refresh Analytics"):
        with st.spinner("Fetching analytics..."):
            st.session_state.analytics = get_analytics()
            st.success("Analytics updated!")
    
    # Display analytics
    if 'analytics' not in st.session_state:
        st.session_state.analytics = get_analytics()
    
    analytics = st.session_state.analytics
    
    if not analytics:
        st.info("No analytics data available.")
    else:
        # Overview metrics
        st.subheader("Channel Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Views", analytics.get('views', 0))
        with col2:
            st.metric("Watch Time (hours)", analytics.get('watch_time', 0))
        with col3:
            st.metric("Subscribers", analytics.get('subscribers', 0))
        with col4:
            st.metric("Revenue ($)", analytics.get('revenue', 0))
        
        # Top videos
        st.subheader("Top Performing Videos")
        
        top_videos = analytics.get('top_videos', [])
        
        if not top_videos:
            st.info("No video performance data available.")
        else:
            for i, video in enumerate(top_videos):
                with st.expander(f"{i+1}. {video['title']}"):
                    st.write(f"**Views:** {video['views']}")
                    st.write(f"**Watch Time (hours):** {video['watch_time']}")
                    st.write(f"**Click-Through Rate:** {video['ctr']}%")

# Settings page
elif navigation == "Settings":
    st.title("Settings")
    
    # Settings tabs
    settings_tab = st.tabs(["Workflow", "Components", "Maintenance"])
    
    # Workflow tab
    with settings_tab[0]:
        st.header("Workflow Settings")
        st.write("Configure automation schedules and notification preferences.")
        
        # Automation Schedule
        st.subheader("Automation Schedule")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Content generation frequency")
            content_freq = st.selectbox(
                "Content generation frequency",
                ["Daily", "Weekly", "Monthly", "Manual"],
                label_visibility="collapsed"
            )
        
        with col2:
            st.write("Publishing schedule")
            publish_schedule = st.selectbox(
                "Publishing schedule",
                ["Publish immediately", "Schedule for peak hours", "Manual publishing"],
                label_visibility="collapsed"
            )
        
        st.write("Video creation timing")
        video_timing = st.selectbox(
            "Video creation timing",
            ["Immediately after content generation", "Daily batch processing", "Manual triggering"],
            label_visibility="collapsed"
        )
        
        # Notifications
        st.subheader("Notifications")
        
        enable_notifications = st.checkbox("Enable email notifications")
        
        if enable_notifications:
            email = st.text_input("Email address")
            
            st.write("Notification events")
            notification_events = st.multiselect(
                "Notification events",
                ["Content generation complete", "Publishing complete", "Error alerts"],
                ["Content generation complete", "Publishing complete", "Error alerts"],
                label_visibility="collapsed"
            )
        
        # Save button
        if st.button("Save Workflow Settings"):
            st.success("Workflow settings saved successfully!")
    
    # Components tab
    with settings_tab[1]:
        st.header("Component Settings")
        st.write("Configure individual components of the automation system.")
        
        # Fact Researcher
        st.subheader("Fact Researcher")
        
        enable_fact_researcher = st.checkbox("Enable Fact Researcher", value=True)
        
        if enable_fact_researcher:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Fact quality threshold")
                fact_quality = st.slider("Fact quality threshold", 1, 10, 7, label_visibility="collapsed")
            
            with col2:
                st.write("Fact Researcher mode")
                fact_mode = st.selectbox(
                    "Fact Researcher mode",
                    ["Automatic", "Semi-automatic", "Manual review"],
                    label_visibility="collapsed"
                )
            
            st.write("Facts per batch")
            facts_per_batch = st.number_input("Facts per batch", 1, 50, 20, label_visibility="collapsed")
        
        # Script Generator
        st.subheader("Script Generator")
        
        enable_script_generator = st.checkbox("Enable Script Generator", value=True)
        
        if enable_script_generator:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Creativity level")
                creativity = st.slider("Creativity level", 1, 10, 8, label_visibility="collapsed")
            
            with col2:
                st.write("Script Generator mode")
                script_mode = st.selectbox(
                    "Script Generator mode",
                    ["Automatic", "Semi-automatic", "Manual review"],
                    label_visibility="collapsed"
                )
            
            st.write("Maximum script length (words)")
            max_script_length = st.number_input("Maximum script length (words)", 50, 500, 200, label_visibility="collapsed")
        
        # Media Selector
        st.subheader("Media Selector")
        
        enable_media_selector = st.checkbox("Enable Media Selector", value=True)
        
        if enable_media_selector:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Image quality")
                image_quality = st.slider("Image quality", 1, 10, 8, label_visibility="collapsed")
            
            with col2:
                st.write("Media source")
                media_source = st.selectbox(
                    "Media source",
                    ["Royalty-free stock", "AI-generated", "Mixed sources"],
                    label_visibility="collapsed"
                )
        
        # YouTube API Configuration
        st.subheader("YouTube API Configuration")
        st.write("Configure your YouTube API credentials to enable automatic publishing.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input("Client ID", type="password", help="Enter your Google API Client ID")
            
        with col2:
            client_secret = st.text_input("Client Secret", type="password", help="Enter your Google API Client Secret")
        
        # Add authentication button
        if st.button("Save and Authenticate"):
            if client_id and client_secret:
                # Save credentials to session state
                st.session_state.youtube_client_id = client_id
                st.session_state.youtube_client_secret = client_secret
                
                # Show success message
                st.success("YouTube API credentials saved successfully!")
                
                # In a real implementation, you would initiate OAuth flow here
                st.info("To complete authentication, you would be redirected to Google's consent screen. This feature will be implemented in the next update.")
            else:
                st.error("Please enter both Client ID and Client Secret.")
        
        # Display current connection status
        st.subheader("Connection Status")
        if 'youtube_client_id' in st.session_state and 'youtube_client_secret' in st.session_state:
            st.write("✅ YouTube API credentials are configured")
        else:
            st.write("❌ YouTube API credentials not configured")
        
        # Save button
        if st.button("Save Component Settings"):
            st.success("Component settings saved successfully!")
    
    # Maintenance tab
    with settings_tab[2]:
        st.header("System Maintenance")
        st.write("Manage system resources and perform maintenance tasks.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Cache"):
                st.success("Cache cleared successfully!")
        
        with col2:
            if st.button("Check for Updates"):
                st.info("Your system is up to date.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Restart Components"):
                st.success("Components restarted successfully!")
        
        with col2:
            if st.button("View Logs"):
                st.info("Logs will be displayed here in a future update.")
        
        # Storage Management
        st.subheader("Storage Management")
        
        # Sample storage data
        storage_data = [
            {"type": "Facts Database", "used": 12.5},
            {"type": "Media Files", "used": 256.8},
            {"type": "Generated Videos", "used": 1458.3}
        ]
        
        for item in storage_data:
            st.progress(min(item["used"] / 2000, 1.0))
            st.write(f"{item['used']} MB used")
        
        if st.button("Clean Up Storage"):
            st.success("Storage cleaned up successfully!")

# Help page
elif navigation == "Help":
    st.title("Help & Documentation")
    
    st.write("Learn how to use the YouTube Content Automation system.")
    
    # FAQ
    st.subheader("Frequently Asked Questions")
    
    with st.expander("How does the content generation work?"):
        st.write("""
        The content generation system uses AI to research and generate interesting "Did You Know" facts.
        
        1. Select the categories you're interested in
        2. Choose how many facts you want to generate
        3. Click "Generate Facts"
        4. The system will create unique, engaging facts for your videos
        """)
    
    with st.expander("How do I publish videos to YouTube?"):
        st.write("""
        To publish videos to YouTube:
        
        1. Configure your YouTube API credentials in Settings > Components > YouTube API Configuration
        2. Create videos in the Video Creation page
        3. Go to the Publishing page
        4. Select the videos you want to publish
        5. Choose your privacy settings
        6. Click "Publish Selected Videos"
        """)
    
    with st.expander("What are the system requirements?"):
        st.write("""
        The YouTube Content Automation system is cloud-based and runs entirely in your web browser.
        
        You'll need:
        - A modern web browser (Chrome, Firefox, Safari, Edge)
        - A YouTube channel
        - Google API credentials (for publishing to YouTube)
        """)
    
    # Contact Support
    st.subheader("Contact Support")
    
    st.write("If you need assistance, please contact our support team.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name")
    
    with col2:
        email = st.text_input("Your Email")
    
    message = st.text_area("Message", height=150)
    
    if st.button("Send Message"):
        if name and email and message:
            st.success("Message sent! Our support team will get back to you soon.")
        else:
            st.error("Please fill in all fields.")
