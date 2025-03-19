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


# Content Generation page
elif page == "Content Generation":
    st.title("Content Generation")
    
    st.write("Generate interesting 'Did You Know' facts for your videos.")
    
    # Fact generation settings
    st.subheader("Fact Generation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_facts = st.number_input("Number of facts to generate", min_value=1, max_value=100, value=10)
        fact_length = st.select_slider("Fact length", options=["Short", "Medium", "Long"], value="Medium")
    
    with col2:
        categories = st.multiselect(
            "Fact categories",
            ["Science", "History", "Nature", "Space", "Technology", "Psychology", "Art", "Food", "Geography"],
            ["Science", "History", "Nature"]
        )
        
        reliability = st.slider("Source reliability", min_value=1, max_value=10, value=8)
    
    if st.button("Generate Facts"):
        with st.spinner("Generating interesting facts..."):
            # Simulate API call delay
            import time
            time.sleep(2)
            
            # Sample facts based on selected categories
            sample_facts = {
                "Science": [
                    "The human body contains enough carbon to fill about 9,000 pencils.",
                    "A teaspoonful of neutron star would weigh about 6 billion tons.",
                    "The average person walks the equivalent of three times around the world in a lifetime."
                ],
                "History": [
                    "The shortest war in history was between Britain and Zanzibar in 1896, lasting only 38 minutes.",
                    "Ancient Egyptians used to use honey as an offering to their gods.",
                    "The first recorded use of 'OMG' was in a 1917 letter to Winston Churchill."
                ],
                "Nature": [
                    "Octopuses have three hearts, nine brains, and blue blood.",
                    "Bananas are berries, but strawberries aren't.",
                    "A group of flamingos is called a 'flamboyance'."
                ],
                "Space": [
                    "There are more stars in the universe than grains of sand on all the beaches on Earth.",
                    "A day on Venus is longer than a year on Venus.",
                    "The Great Red Spot on Jupiter is a storm that has been raging for at least 400 years."
                ],
                "Technology": [
                    "The first computer bug was an actual real-life bug - a moth was found in the Harvard Mark II computer in 1947.",
                    "The average smartphone user touches their phone 2,617 times a day.",
                    "The first message sent over the internet was 'LO'. It was supposed to be 'LOGIN' but the system crashed."
                ]
            }
            
            # Display generated facts
            st.subheader("Generated Facts")
            displayed_facts = []
            
            for category in categories:
                if category in sample_facts:
                    for fact in sample_facts[category]:
                        displayed_facts.append(fact)
                        if len(displayed_facts) >= num_facts:
                            break
                if len(displayed_facts) >= num_facts:
                    break
            
            for i, fact in enumerate(displayed_facts[:num_facts]):
                st.write(f"{i+1}. {fact}")
            
            st.session_state.facts_generated += num_facts
            st.success(f"Successfully generated {num_facts} facts!")
    
    # Fact sources
    st.subheader("Fact Sources")
    st.write("Configure your fact sources and reliability settings.")
    
    sources = [
        {"name": "Wikipedia", "reliability": 7, "enabled": True},
        {"name": "Scientific Journals", "reliability": 9, "enabled": True},
        {"name": "News Websites", "reliability": 6, "enabled": True},
        {"name": "Educational Websites", "reliability": 8, "enabled": True}
    ]
    
    for i, source in enumerate(sources):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(source["name"])
        with col2:
            st.write(f"Reliability: {source['reliability']}/10")
        with col3:
            sources[i]["enabled"] = st.checkbox("Enable", value=source["enabled"], key=f"source_{i}")

# Video Creation page
elif page == "Video Creation":
    st.title("Video Creation")
    
    # Tabs for different stages of video creation
    tabs = st.tabs(["Script Generation", "Media Selection", "Video Assembly"])
    
    # Script Generation tab
    with tabs[0]:
        st.header("Script Generation")
        st.write("Convert facts into engaging video scripts.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            script_format = st.selectbox(
                "Script format",
                ["Conversational", "Educational", "Humorous", "Dramatic", "Inspirational"]
            )
            
            script_length = st.select_slider(
                "Script length",
                options=["15 seconds", "30 seconds", "60 seconds", "2 minutes", "5 minutes"],
                value="60 seconds"
            )
        
        with col2:
            language_style = st.selectbox(
                "Language style",
                ["Formal", "Casual", "Enthusiastic", "Mysterious", "Technical"]
            )
            
            include_questions = st.checkbox("Include rhetorical questions", value=True)
        
        if st.button("Generate Scripts"):
            with st.spinner("Generating scripts..."):
                # Simulate API call delay
                import time
                time.sleep(2)
                
                st.subheader("Generated Scripts")
                
                # Sample script
                sample_script = """
                [INTRO]
                Did you know that octopuses have three hearts, nine brains, and blue blood?
                
                [MAIN CONTENT]
                That's right! These incredible creatures have two hearts that pump blood through their gills, and a third heart that circulates blood through the rest of their body.
                
                Their nine brains include a central brain and eight additional mini-brains - one for each arm. This allows each arm to think and act independently!
                
                And unlike our red blood, which gets its color from iron, octopus blood contains copper, giving it a blue appearance.
                
                [OUTRO]
                Next time you see an octopus, remember you're looking at one of the most alien-like creatures on our own planet!
                """
                
                st.text_area("Script 1", sample_script, height=300)
                
                st.session_state.scripts_created += 1
                st.success("Script generated successfully!")
    
    # Media Selection tab
    with tabs[1]:
        st.header("Media Selection")
        st.write("Select images, videos, and audio for your content.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            image_source = st.multiselect(
                "Image sources",
                ["Pixabay", "Pexels", "Unsplash", "iStock", "Adobe Stock"],
                ["Pixabay", "Pexels", "Unsplash"]
            )
            
            video_source = st.multiselect(
                "Video sources",
                ["Pixabay", "Pexels", "Coverr", "Videvo", "Adobe Stock"],
                ["Pixabay", "Pexels"]
            )
        
        with col2:
            audio_source = st.multiselect(
                "Audio sources",
                ["Epidemic Sound", "Artlist", "YouTube Audio Library", "SoundCloud", "Free Music Archive"],
                ["YouTube Audio Library", "Free Music Archive"]
            )
            
            visual_style = st.selectbox(
                "Visual style",
                ["Minimalist", "Colorful", "Professional", "Vintage", "Modern", "Abstract"]
            )
        
        if st.button("Select Media"):
            with st.spinner("Selecting media..."):
                # Simulate API call delay
                import time
                time.sleep(2)
                
                st.subheader("Selected Media")
                
                # Sample media selection
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.image("https://images.pexels.com/photos/1069927/pexels-photo-1069927.jpeg?auto=compress&cs=tinysrgb&w=600", caption="Octopus - Main Image") 
                
                with col2:
                    st.image("https://images.pexels.com/photos/3377405/pexels-photo-3377405.jpeg?auto=compress&cs=tinysrgb&w=600", caption="Ocean - Background") 
                
                with col3:
                    st.image("https://images.pexels.com/photos/3094799/pexels-photo-3094799.jpeg?auto=compress&cs=tinysrgb&w=600", caption="Marine Life - Supporting Image") 
                
                st.write("**Selected Audio:** Underwater Ambience - YouTube Audio Library")
                
                st.success("Media selected successfully!")
    
    # Video Assembly tab
    with tabs[2]:
        st.header("Video Assembly")
        st.write("Combine scripts, images, and audio into complete videos.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            resolution = st.selectbox(
                "Resolution",
                ["720p", "1080p", "1440p", "4K"]
            )
            
            frame_rate = st.selectbox(
                "Frame rate",
                ["24 fps", "30 fps", "60 fps"]
            )
        
        with col2:
            format = st.selectbox(
                "Format",
                ["MP4", "MOV", "AVI", "WMV"]
            )
            
            quality = st.select_slider(
                "Quality",
                options=["Low", "Medium", "High", "Ultra"],
                value="High"
            )
        
        st.subheader("Voice Settings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            voice_provider = st.selectbox(
                "Voice provider",
                ["ElevenLabs", "Murf.ai", "Google TTS", "Amazon Polly", "Microsoft Azure"]
            )
        
        with col2:
            voice_gender = st.selectbox(
                "Voice type",
                ["Male", "Female", "Neutral"]
            )
        
        with col3:
            voice_accent = st.selectbox(
                "Voice accent",
                ["American", "British", "Australian", "Indian", "German", "French"]
            )
        
        if st.button("Assemble Video"):
            with st.spinner("Assembling video..."):
                # Simulate API call delay
                import time
                time.sleep(3)
                
                st.subheader("Assembled Video")
                
                # Sample video player (using a placeholder image)
                st.image("https://images.pexels.com/photos/1069927/pexels-photo-1069927.jpeg?auto=compress&cs=tinysrgb&w=600", caption="Video Preview") 
                
                st.write("**Title:** Amazing Facts About Octopuses")
                st.write("**Duration:** 60 seconds")
                st.write("**Size:** 24.7 MB")
                
                st.session_state.videos_assembled += 1
                st.success("Video assembled successfully!")
                st.balloons()

# Publishing page
elif page == "Publishing":
    st.title("Publishing")
    
    # Tabs for different aspects of publishing
    tabs = st.tabs(["YouTube Settings", "Publish Videos", "SEO Settings"])
    
    # YouTube Settings tab
    with tabs[0]:
        st.header("YouTube Settings")
        st.write("Configure your YouTube API credentials and channel settings.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input("Client ID", type="password")
            client_secret = st.text_input("Client Secret", type="password")
        
        with col2:
            redirect_uri = st.text_input("Redirect URI", "http://localhost:8501/oauth2callback") 
            channel_id = st.text_input("Channel ID (optional)")
        
        if st.button("Authenticate"):
            if client_id and client_secret:
                st.success("Authentication successful! Connected to YouTube channel.")
            else:
                st.error("Please enter your Client ID and Client Secret.")
    
    # Publish Videos tab
    with tabs[1]:
        st.header("Publish Videos")
        st.write("Upload and schedule your videos for publishing on YouTube.")
        
        # Sample videos ready for publishing
        videos = [
            {"title": "Amazing Facts About Octopuses", "duration": "60 seconds", "status": "Ready"},
            {"title": "The Shortest War in History", "duration": "45 seconds", "status": "Ready"},
            {"title": "Fascinating Facts About Bananas", "duration": "50 seconds", "status": "Ready"}
        ]
        
        st.subheader("Videos Ready for Publishing")
        
        for i, video in enumerate(videos):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.write(video["title"])
            
            with col2:
                st.write(video["duration"])
            
            with col3:
                st.write(video["status"])
            
            with col4:
                videos[i]["selected"] = st.checkbox("Select", key=f"publish_{i}")
        
        st.subheader("Publishing Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            privacy = st.selectbox(
                "Privacy status",
                ["Public", "Unlisted", "Private"]
            )
            
            monetization = st.checkbox("Enable monetization", value=True)
        
        with col2:
            publish_time = st.radio(
                "Publishing time",
                ["Publish immediately", "Schedule for later"]
            )
            
            if publish_time == "Schedule for later":
                schedule_date = st.date_input("Schedule date")
                schedule_time = st.time_input("Schedule time")
        
        if st.button("Publish Selected"):
            selected_count = sum(1 for video in videos if video.get("selected", False))
            
            if selected_count > 0:
                with st.spinner(f"Publishing {selected_count} videos..."):
                    # Simulate API call delay
                    import time
                    time.sleep(2)
                    
                    st.session_state.videos_published += selected_count
                    st.success(f"Successfully published {selected_count} videos to YouTube!")
            else:
                st.warning("Please select at least one video to publish.")
    
    # SEO Settings tab
    with tabs[2]:
        st.header("SEO Settings")
        st.write("Optimize your videos for maximum visibility and engagement.")
        
        st.subheader("Title Templates")
        title_template = st.text_area(
            "Title template",
            "Did You Know: {fact_summary} | Amazing Facts",
            help="Use {fact_summary} as a placeholder for the main fact."
        )
        
        st.subheader("Description Templates")
        description_template = st.text_area(
            "Description template",
            """🔍 Did You Know: {fact_summary}

Learn more amazing facts in this short video!

⏱️ TIMESTAMPS:
0:00 - Introduction
0:10 - Main Fact
0:40 - Additional Information

👍 If you enjoyed this video, please like and subscribe for more amazing facts!

🔗 LINKS:
Website: https://www.amazingfacts.com
Instagram: https://www.instagram.com/amazingfacts

#DidYouKnow #{tag1} #{tag2} #Facts #Amazing

*Some links may be affiliate links where I earn a small commission at no extra cost to you."""
        ) 
        
        st.subheader("Tag Generation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_tags = st.number_input("Maximum number of tags", min_value=5, max_value=30, value=15)
            include_trending = st.checkbox("Include trending tags", value=True)
        
        with col2:
            tag_style = st.selectbox(
                "Tag style",
                ["Specific", "Broad", "Mixed"]
            )
            
            auto_translate = st.checkbox("Auto-translate tags to local languages", value=False)
        
        st.subheader("Thumbnail Settings")
        
        thumbnail_style = st.selectbox(
            "Thumbnail style",
            ["Text Overlay", "Shocked Face", "Question Mark", "Before & After", "Minimalist"]
        )
        
        ab_testing = st.checkbox("Enable A/B testing for thumbnails", value=True)
        
        if st.button("Save SEO Settings"):
            st.success("SEO settings saved successfully!")

# Analytics page
elif page == "Analytics":
    st.title("Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        date_range = st.selectbox(
            "Date range",
            ["Last 7 days", "Last 28 days", "Last 90 days", "Last 12 months", "Lifetime"]
        )
    
    with col2:
        comparison = st.checkbox("Compare with previous period", value=False)
    
    # Performance metrics
    st.header("Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Views", "1,248", "+42%")
    
    with col2:
        st.metric("Watch Time (hours)", "78.3", "+28%")
    
    with col3:
        st.metric("Subscribers", "156", "+15")
    
    with col4:
        st.metric("Estimated Revenue", "$12.47", "+$3.21")
    
    # Performance charts
    st.header("Performance Charts")
    
    chart_tabs = st.tabs(["Views", "Watch Time", "Subscribers", "Revenue"])
    
    # Sample chart data
    import numpy as np
    import pandas as pd
    
    # Views chart
    with chart_tabs[0]:
        dates = pd.date_range(start="2023-01-01", periods=30, freq="D")
        views = np.random.randint(20, 100, size=30).cumsum()
        
        chart_data = pd.DataFrame({
            "Date": dates,
            "Views": views
        })
        
        st.line_chart(chart_data.set_index("Date"))
    
    # Watch Time chart
    with chart_tabs[1]:
        watch_time = np.random.randint(1, 10, size=30).cumsum()
        
        chart_data = pd.DataFrame({
            "Date": dates,
            "Watch Time (hours)": watch_time
        })
        
        st.line_chart(chart_data.set_index("Date"))
    
    # Subscribers chart
    with chart_tabs[2]:
        subscribers = np.random.randint(0, 5, size=30).cumsum()
        
        chart_data = pd.DataFrame({
            "Date": dates,
            "Subscribers": subscribers
        })
        
        st.line_chart(chart_data.set_index("Date"))
    
    # Revenue chart
    with chart_tabs[3]:
        revenue = np.random.uniform(0.1, 1.0, size=30).cumsum()
        
        chart_data = pd.DataFrame({
            "Date": dates,
            "Revenue ($)": revenue
        })
        
        st.line_chart(chart_data.set_index("Date"))
    
    # Top performing videos
    st.header("Top Performing Videos")
    
    top_videos = [
        {"title": "Amazing Facts About Octopuses", "views": 487, "watch_time": 32.4, "ctr": "8.2%"},
        {"title": "The Shortest War in History", "views": 342, "watch_time": 25.1, "ctr": "7.5%"},
        {"title": "Fascinating Facts About Bananas", "views": 289, "watch_time": 18.7, "ctr": "6.9%"}
    ]
    
    for video in top_videos:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(video["title"])
        
        with col2:
            st.write(f"Views: {video['views']}")
        
        with col3:
            st.write(f"Watch time: {video['watch_time']}h")
        
        with col4:
            st.write(f"CTR: {video['ctr']}")
    
    # Optimization recommendations
    st.header("Optimization Recommendations")
    
    recommendations = [
        "Increase video frequency to 3 per week for better channel growth",
        "Focus more on Science and History topics which have higher engagement",
        "Optimize thumbnails with more vibrant colors and text",
        "Increase video length to 90 seconds for better monetization"
    ]
    
    for recommendation in recommendations:
        st.info(recommendation)
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
