import streamlit as st
import requests
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="YouTube Content Automation",
    page_icon="📺",
    layout="wide"
)
# Add this function to handle OAuth callback
def handle_oauth_callback():
    # Get the authorization code from URL parameters
    code = st.experimental_get_query_params().get("code", [""])[0]
    
    if code:
        # In a real implementation, you would exchange this code for tokens
        st.success("Authentication successful! You can now publish videos to YouTube.")
        
        # Clear the URL parameters
        st.experimental_set_query_params()
    
# Check if this is an OAuth callback
if "code" in st.experimental_get_query_params():
    handle_oauth_callback()

# Initialize session state variables if they don't exist
if 'facts_generated' not in st.session_state:
    st.session_state.facts_generated = 0
if 'scripts_created' not in st.session_state:
    st.session_state.scripts_created = 0
if 'videos_assembled' not in st.session_state:
    st.session_state.videos_assembled = 0
if 'videos_published' not in st.session_state:
    st.session_state.videos_published = 0

# Sidebar navigation
st.sidebar.title("YouTube Automation")
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Dashboard", "Content Generation", "Video Creation", "Publishing", "Analytics", "Settings", "Help"]
)

# Dashboard page
if page == "Dashboard":
    st.title("YouTube Content Automation Dashboard")
    
    # System Status
    st.header("System Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Facts Generated", st.session_state.facts_generated)
    with col2:
        st.metric("Scripts Created", st.session_state.scripts_created)
    with col3:
        st.metric("Videos Assembled", st.session_state.videos_assembled)
    with col4:
        st.metric("Videos Published", st.session_state.videos_published)
    
    # Quick Actions
    st.header("Quick Actions")
    quick_action_cols = st.columns(4)
    
    with quick_action_cols[0]:
        if st.button("Generate Content"):
            st.session_state.facts_generated += 10
            st.success("Generated 10 new facts!")
            st.balloons()
    
    with quick_action_cols[1]:
        if st.button("Create Videos"):
            if st.session_state.facts_generated > st.session_state.scripts_created:
                st.session_state.scripts_created += 5
                st.session_state.videos_assembled += 5
                st.success("Created 5 new videos!")
            else:
                st.warning("Generate more facts first!")
    
    with quick_action_cols[2]:
        if st.button("Publish Videos"):
            if st.session_state.videos_assembled > st.session_state.videos_published:
                st.session_state.videos_published += 3
                st.success("Published 3 videos to YouTube!")
            else:
                st.warning("Create more videos first!")
    
    with quick_action_cols[3]:
        if st.button("Run Analytics"):
            st.info("Analytics updated!")
    
    # Recent Activity
    st.header("Recent Activity")
    
    # Sample activity data
    activities = [
        {"time": "Today, 2:30 PM", "action": "Video published - 5 Amazing Facts About Deep Sea Creatures"},
        {"time": "Today, 10:15 AM", "action": "Content generated - 10 new facts about Ancient History"},
        {"time": "Yesterday, 4:45 PM", "action": "Analytics updated - Performance report for last week"},
        {"time": "2 days ago", "action": "Video created - Fascinating Facts About the Human Brain"}
    ]
    
    for activity in activities:
        st.markdown(f"**{activity['time']}:** {activity['action']}")

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
elif page == "Settings":
    st.title("Settings")
    
    # Tabs for different settings
    tabs = st.tabs(["Workflow", "Components", "Maintenance"])
    
    # Workflow settings
    with tabs[0]:
        st.header("Workflow Settings")
        st.write("Configure automation schedules and notification preferences.")
        
        st.subheader("Automation Schedule")
        
        col1, col2 = st.columns(2)
        
        with col1:
            content_frequency = st.selectbox(
                "Content generation frequency",
                ["Daily", "Every 3 days", "Weekly", "Bi-weekly", "Monthly"]
            )
            
            video_creation = st.selectbox(
                "Video creation timing",
                ["Immediately after content generation", "Daily batch", "Weekly batch"]
            )
        
        with col2:
            publishing_schedule = st.selectbox(
                "Publishing schedule",
                ["Publish immediately", "Daily at specific time", "Custom schedule"]
            )
            
            if publishing_schedule == "Daily at specific time":
                publish_time = st.time_input("Publishing time")
            elif publishing_schedule == "Custom schedule":
                st.write("Configure custom schedule:")
                days = st.multiselect(
                    "Publishing days",
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    ["Monday", "Wednesday", "Friday"]
                )
                publish_time = st.time_input("Publishing time")
        
        st.subheader("Notifications")
        
        email_notifications = st.checkbox("Enable email notifications", value=True)
        
        if email_notifications:
            email = st.text_input("Email address")
            
            notification_events = st.multiselect(
                "Notification events",
                ["Content generation complete", "Video creation complete", "Publishing complete", "Error alerts", "Performance reports"],
                ["Content generation complete", "Publishing complete", "Error alerts"]
            )
        
        if st.button("Save Workflow Settings"):
            st.success("Workflow settings saved successfully!")
    # Add this in the Components tab section of your Settings page
st.header("YouTube API Configuration")
st.write("Configure your YouTube API credentials to enable automatic publishing.")

# Create two columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    # YouTube API credentials
    client_id = st.text_input("Client ID", type="password", help="Enter your Google API Client ID")
    
with col2:
    client_secret = st.text_input("Client Secret", type="password", help="Enter your Google API Client Secret")

# Add authentication button
if st.button("Save and Authenticate"):
    if client_id and client_secret:
        # Save credentials to session state or database
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

    # Component settings
    with tabs[1]:
        st.header("Component Settings")
        st.write("Configure individual components of the automation system.")
        
        components = ["Fact Researcher", "Script Generator", "Media Selector", "Voiceover Generator", "Video Assembler", "YouTube Publisher", "Analytics Optimizer"]
        
        for component in components:
            st.subheader(component)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.checkbox(f"Enable {component}", value=True, key=f"enable_{component}")
                
                if component == "Fact Researcher":
                    st.slider("Fact quality threshold", min_value=1, max_value=10, value=7, key=f"quality_{component}")
                elif component == "Script Generator":
                    st.slider("Creativity level", min_value=1, max_value=10, value=8, key=f"creativity_{component}")
                elif component == "Media Selector":
                    st.slider("Visual quality threshold", min_value=1, max_value=10, value=8, key=f"quality_{component}")
                elif component == "Voiceover Generator":
                    st.slider("Voice naturalness", min_value=1, max_value=10, value=9, key=f"naturalness_{component}")
                elif component == "Video Assembler":
                    st.slider("Production quality", min_value=1, max_value=10, value=8, key=f"quality_{component}")
                elif component == "YouTube Publisher":
                    st.slider("SEO optimization level", min_value=1, max_value=10, value=9, key=f"optimization_{component}")
                elif component == "Analytics Optimizer":
                    st.slider("Optimization aggressiveness", min_value=1, max_value=10, value=7, key=f"aggressiveness_{component}")
            
            with col2:
                st.selectbox(f"{component} mode", ["Automatic", "Semi-automatic", "Manual"], key=f"mode_{component}")
                
                if component == "Fact Researcher":
                    st.number_input("Facts per batch", min_value=5, max_value=100, value=20, key=f"batch_{component}")
                elif component == "Script Generator":
                    st.number_input("Maximum script length (words)", min_value=50, max_value=500, value=200, key=f"length_{component}")
                elif component == "Media Selector":
                    st.number_input("Images per video", min_value=3, max_value=30, value=10, key=f"images_{component}")
                elif component == "Voiceover Generator":
                    st.number_input("Speaking rate (words per minute)", min_value=100, max_value=200, value=150, key=f"rate_{component}")
                elif component == "Video Assembler":
                    st.number_input("Transition duration (seconds)", min_value=0.5, max_value=3.0, value=1.0, step=0.1, key=f"transition_{component}")
                elif component == "YouTube Publisher":
                    st.number_input("Maximum tags per video", min_value=5, max_value=30, value=15, key=f"tags_{component}")
                elif component == "Analytics Optimizer":
                    st.number_input("Analysis frequency (days)", min_value=1, max_value=30, value=7, key=f"frequency_{component}")
        
        if st.button("Save Component Settings"):
            st.success("Component settings saved successfully!")
    
    # Maintenance settings
    with tabs[2]:
        st.header("System Maintenance")
        st.write("Manage system resources and perform maintenance tasks.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Cache"):
                st.success("Cache cleared successfully!")
            
            if st.button("Restart Components"):
                st.success("Components restarted successfully!")
        
        with col2:
            if st.button("Check for Updates"):
                st.info("System is up to date!")
            
            if st.button("View Logs"):
                st.code("2023-04-15 10:23:45 INFO: System started\n2023-04-15 10:24:12 INFO: Content generation initiated\n2023-04-15 10:25:30 INFO: Generated 10 facts\n2023-04-15 10:26:45 INFO: Video assembly complete")
        
        st.subheader("Storage Management")
        
        # Sample storage data
        storage_data = {
            "Facts Database": {"used": 12.5, "total": 100},
            "Media Library": {"used": 256.8, "total": 1000},
            "Generated Videos": {"used": 1458.3, "total": 5000}
        }
        
        for category, data in storage_data.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.progress(data["used"] / data["total"])
            
            with col2:
                st.write(f"{data['used']} MB used")
            
            with col3:
                st.write(f"{data['total']} MB total")
        
        if st.button("Clean Up Storage"):
            st.success("Storage cleaned up successfully!")

# Help page
elif page == "Help":
    st.title("Help & Documentation")
    
    st.write("Welcome to the YouTube Content Automation help page. Here you'll find guides and documentation to help you use the system effectively.")
    
    # Tabs for different help sections
    tabs = st.tabs(["Getting Started", "Tutorials", "FAQ", "Troubleshooting", "Contact Support"])
    
    # Getting Started
    with tabs[0]:
        st.header("Getting Started")
        st.write("Learn the basics of using the YouTube Content Automation system.")
        
        st.subheader("System Overview")
        st.write("""
        The YouTube Content Automation system helps you create, publish, and monetize "Did You Know" style videos with minimal intervention. The system consists of several components:
        
        1. **Content Generation** - Researches interesting facts and generates scripts
        2. **Video Creation** - Creates videos with voiceovers and visuals
        3. **Publishing** - Uploads videos to YouTube with optimized metadata
        4. **Analytics** - Tracks performance and optimizes your strategy
        """)
        
        st.subheader("First Steps")
        st.write("""
        To get started with the system:
        
        1. Configure your YouTube API credentials in the Settings page
        2. Generate your first batch of facts in the Content Generation page
        3. Create videos in the Video Creation page
        4. Publish your videos in the Publishing page
        5. Monitor performance in the Analytics page
        """)
    
    # Tutorials
    with tabs[1]:
        st.header("Tutorials")
        st.write("Step-by-step guides for using the system.")
        
        tutorials = [
            "Setting Up YouTube API Credentials",
            "Generating High-Quality Facts",
            "Creating Engaging Scripts",
            "Selecting the Best Media",
            "Optimizing Video Settings",
            "Publishing Strategies for Maximum Reach",
            "Understanding Analytics and Optimization"
        ]
        
        for tutorial in tutorials:
            st.subheader(tutorial)
            st.write("Click to expand tutorial...")
            st.write("Tutorial content would appear here.")
    
    # FAQ
    with tabs[2]:
        st.header("Frequently Asked Questions")
        
        faqs = [
            {
                "question": "How many videos can I create per month?",
                "answer": "The system can generate as many videos as you need. However, we recommend starting with 2-3 videos per week to build your channel consistently without overwhelming yourself."
            },
            {
                "question": "Do I need to appear on camera?",
                "answer": "No, the system is designed to create faceless videos using stock footage, images, and AI-generated voiceovers."
            },
            {
                "question": "How long does it take to monetize my channel?",
                "answer": "To join the YouTube Partner Program, you need 1,000 subscribers and 4,000 watch hours in the past 12 months. With consistent content, this typically takes 6-12 months."
            },
            {
                "question": "Can I customize the voice used in videos?",
                "answer": "Yes, you can select from various voice options including gender, accent, and speaking style in the Video Creation page."
            },
            {
                "question": "Is the content copyright-free?",
                "answer": "The system uses a combination of public domain information and properly cited facts. All media is sourced from royalty-free libraries to avoid copyright issues."
            }
        ]
        
        for faq in faqs:
            st.subheader(faq["question"])
            st.write(faq["answer"])
    
    # Troubleshooting
    with tabs[3]:
        st.header("Troubleshooting")
        st.write("Solutions for common issues.")
        
        issues = [
            {
                "problem": "Content generation is not working",
                "solution": "Check your internet connection and ensure the Fact Researcher component is enabled in Settings. Try adjusting the fact quality threshold to a lower value."
            },
            {
                "problem": "Videos are not being created",
                "solution": "Ensure you have generated facts first. Check that the Media Selector and Video Assembler components are enabled. Try using different media sources."
            },
            {
                "problem": "Cannot publish to YouTube",
                "solution": "Verify your YouTube API credentials in the Settings page. Ensure your channel is properly set up and that you have granted the necessary permissions."
            },
            {
                "problem": "Analytics data is not showing",
                "solution": "YouTube typically takes 24-48 hours to process analytics data. If the problem persists, check your API permissions and ensure the Analytics Optimizer component is enabled."
            }
        ]
        
        for issue in issues:
            st.subheader(issue["problem"])
            st.write(issue["solution"])
    
    # Contact Support
    with tabs[4]:
        st.header("Contact Support")
        st.write("Need help? Contact our support team.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
        
        with col2:
            issue_type = st.selectbox(
                "Issue Type",
                ["Technical Problem", "Feature Request", "Billing Question", "General Inquiry"]
            )
            
            priority = st.select_slider(
                "Priority",
                options=["Low", "Medium", "High"],
                value="Medium"
            )
        
        message = st.text_area("Message", height=150)
        
        if st.button("Submit"):
            if name and email and message:
                st.success("Support request submitted successfully! We'll get back to you within 24 hours.")
            else:
                st.error("Please fill in all required fields.")
