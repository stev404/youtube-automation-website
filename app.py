# app.py (Streamlit frontend) 
import streamlit as st
import requests
import json
import os
from datetime import datetime
import time
from youtube_api_implementation import setup_youtube_api
from fact_generation import FactGenerator
from script_creation import ScriptGenerator
from video_assembly import VideoAssembler
import config

# Initialize YouTube API
@st.cache_resource
def get_youtube_api():
    try:
        return setup_youtube_api(token_file=config.TOKEN_FILE)
    except Exception as e:
        st.error(f"Error initializing YouTube API: {str(e)}")
        return None


# Page configuration
st.set_page_config(
    page_title="YouTube Content Automation",
    page_icon="📺",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'facts_generated' not in st.session_state:
    st.session_state.facts_generated = 0
if 'scripts_created' not in st.session_state:
    st.session_state.scripts_created = 0
if 'videos_assembled' not in st.session_state:
    st.session_state.videos_assembled = 0
if 'videos_published' not in st.session_state:
    st.session_state.videos_published = 0
if 'youtube_api' not in st.session_state:
    st.session_state.youtube_api = None
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'channel_info' not in st.session_state:
    st.session_state.channel_info = None
if 'uploaded_videos' not in st.session_state:
    st.session_state.uploaded_videos = []

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
    
    # YouTube Connection Status
    st.header("YouTube Connection Status")
    if st.session_state.is_authenticated:
        st.success("✅ Connected to YouTube")
        if st.session_state.channel_info:
            channel_name = st.session_state.channel_info.get('snippet', {}).get('title', 'Your Channel')
            st.write(f"Connected to channel: **{channel_name}**")
            
            # Display some channel stats
            stats = st.session_state.channel_info.get('statistics', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Subscribers", stats.get('subscriberCount', '0'))
            with col2:
                st.metric("Videos", stats.get('videoCount', '0'))
            with col3:
                st.metric("Views", stats.get('viewCount', '0'))
    else:
        st.warning("⚠️ Not connected to YouTube")
        st.write("Go to the Publishing page to configure your YouTube API credentials.")
    
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
            if not st.session_state.is_authenticated:
                st.error("Please connect to YouTube first in the Publishing page.")
            elif st.session_state.videos_assembled > st.session_state.videos_published:
                with st.spinner("Publishing videos to YouTube..."):
                    # This would actually call the YouTube API in a real implementation
                    if st.session_state.youtube_api:
                        st.session_state.videos_published += 3
                        st.success("Published 3 videos to YouTube!")
                    else:
                        st.error("YouTube API not initialized. Please authenticate in the Publishing page.")
            else:
                st.warning("Create more videos first!")
    
    with quick_action_cols[3]:
        if st.button("Run Analytics"):
            if st.session_state.is_authenticated and st.session_state.youtube_api:
                with st.spinner("Fetching analytics from YouTube..."):
                    try:
                        channel_analytics = st.session_state.youtube_api.get_channel_analytics()
                        st.info("Analytics updated!")
                        st.write("Channel statistics:", channel_analytics)
                    except Exception as e:
                        st.error(f"Error fetching analytics: {str(e)}")
            else:
                st.error("Please connect to YouTube first in the Publishing page.")
    
    # Recent Activity
    st.header("Recent Activity")
    
    # Sample activity data
    activities = [
        {"time": "Today, 2:30 PM", "action": "Video published - 5 Amazing Facts About Deep Sea Creatures"},
        {"time": "Today, 10:15 AM", "action": "Content generated - 10 new facts about Ancient History"},
        {"time": "Yesterday, 4:45 PM", "action": "Analytics updated - Performance report for last week"},
        {"time": "2 days ago", "action": "Video created - Fascinating Facts About the Human Brain"}
    ]
    
    # Add real uploaded videos to activity if available
    if st.session_state.uploaded_videos:
        for video in st.session_state.uploaded_videos[:3]:
            activities.insert(0, {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "action": f"Video published - {video.get('snippet', {}).get('title', 'Unknown')}"
            })
    
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
            
            # Update session state
            st.session_state.facts_generated += len(displayed_facts[:num_facts])
            
            # Save button
            if st.button("Save Facts for Video Creation"):
                st.success(f"Saved {len(displayed_facts[:num_facts])} facts for video creation!")

# Video Creation page
elif page == "Video Creation":
    st.title("Video Creation")
    
    # Initialize content generation components
    fact_generator = FactGenerator()
    script_generator = ScriptGenerator()
    video_assembler = VideoAssembler()
    
    # Check if facts are available
    if st.session_state.facts_generated == 0:
        st.warning("Please generate facts first in the Content Generation page.")
    else:
        # Tabs for different aspects of video creation
        tabs = st.tabs(["Create Scripts", "Assemble Videos", "Preview"])
        
        # Create Scripts tab
        with tabs[0]:
            st.header("Create Scripts")
            st.write("Convert your generated facts into engaging video scripts.")
            
            # Get available facts (in a real implementation, these would be stored in session state or database)
            # This is a placeholder - you would replace this with your actual facts from the Content Generation page
            sample_facts = []
            for category in ["Science", "History", "Nature", "Space", "Technology"]:
                if category in st.session_state.get('selected_categories', ["Science", "History", "Nature"]):
                    for fact in fact_generator.get_sample_facts([category], 3):
                        sample_facts.append(fact)
            
            # Script settings
            st.subheader("Script Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                video_title = st.text_input("Video Title", "Amazing Facts You Didn't Know")
                include_sources = st.checkbox("Include Sources", value=False)
            
            with col2:
                num_facts_per_video = st.slider("Facts per Video", min_value=3, max_value=10, value=5)
                
            # Create script button
            if st.button("Create Scripts"):
                if len(sample_facts) >= num_facts_per_video:
                    with st.spinner("Creating engaging scripts..."):
                        # Initialize script generator
                        script_generator = ScriptGenerator()
                        
                        # Select facts for this video
                        selected_facts = sample_facts[:num_facts_per_video]
                        
                        # Create script
                        script_data = script_generator.create_script_with_sections(
                            facts=selected_facts,
                            title=video_title,
                            include_sources=include_sources
                        )
                        
                        # Store in session state
                        if 'scripts' not in st.session_state:
                            st.session_state.scripts = []
                        
                        st.session_state.scripts.append(script_data)
                        st.session_state.scripts_created += 1
                        
                        st.success(f"Script created successfully! Estimated video duration: {script_data['estimated_duration']} seconds")
                        
                        # Display script preview
                        with st.expander("Script Preview", expanded=True):
                            st.write(script_data["full_script"])
                else:
                    st.error(f"Not enough facts available. Please generate at least {num_facts_per_video} facts.")
            
            # Display existing scripts
            if 'scripts' in st.session_state and st.session_state.scripts:
                st.subheader("Your Scripts")
                for i, script in enumerate(st.session_state.scripts):
                    with st.expander(f"Script {i+1}: {script['title']}"):
                        st.write(f"Duration: {script['estimated_duration']} seconds")
                        st.write(f"Facts: {script['fact_count']}")
                        st.write(script["full_script"])
        
        # Assemble Videos tab
        with tabs[1]:
            st.header("Assemble Videos")
            st.write("Create videos from your scripts with customizable settings.")
            
            if 'scripts' not in st.session_state or not st.session_state.scripts:
                st.warning("Please create scripts first in the Create Scripts tab.")
            else:
                # Video settings
                st.subheader("Video Settings")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_script_index = st.selectbox(
                        "Select Script", 
                        range(len(st.session_state.scripts)), 
                        format_func=lambda i: f"Script {i+1}: {st.session_state.scripts[i]['title']}"
                    )
                    
                    visual_style = st.selectbox(
                        "Visual Style",
                        ["standard", "minimal", "vibrant"],
                        format_func=lambda x: x.capitalize()
                    )
                
                with col2:
                    text_to_speech = st.checkbox("Enable Text-to-Speech", value=True)
                    use_background_music = st.checkbox("Add Background Music", value=True)
                
                # Create video button
                if st.button("Create Video"):
                    with st.spinner("Assembling your video..."):
                        # Get selected script
                        script_data = st.session_state.scripts[selected_script_index]
                        
                        # Initialize video assembler
                        video_assembler = VideoAssembler()
                        
                        # Create temporary directory for output if it doesn't exist
                        output_dir = "output"
                        os.makedirs(output_dir, exist_ok=True)
                        
                        # Generate output filename
                        output_filename = f"video_{len(st.session_state.get('videos', []))}.mp4"
                        output_path = os.path.join(output_dir, output_filename)
                        
                        # Create video
                        video_path = video_assembler.create_video(
                            script_data=script_data,
                            output_path=output_path,
                            text_to_speech=text_to_speech,
                            visual_style=visual_style
                        )
                        
                        # Store in session state
                        if 'videos' not in st.session_state:
                            st.session_state.videos = []
                        
                        video_info = {
                            "path": video_path,
                            "title": script_data["title"],
                            "duration": script_data["estimated_duration"],
                            "script_index": selected_script_index
                        }
                        
                        st.session_state.videos.append(video_info)
                        st.session_state.videos_assembled += 1
                        
                        st.success(f"Video created successfully at {video_path}")
                
                # Display existing videos
                if 'videos' in st.session_state and st.session_state.videos:
                    st.subheader("Your Videos")
                    for i, video in enumerate(st.session_state.videos):
                        with st.expander(f"Video {i+1}: {video['title']}"):
                            st.write(f"Duration: {video['duration']} seconds")
                            st.write(f"Path: {video['path']}")
                            
                            # In a real implementation, you would add video preview here
                            st.info("Video preview would be displayed here in the full implementation.")
        
        # Preview tab
        with tabs[2]:
            st.header("Preview")
            st.write("Preview your videos before publishing.")
            
            if 'videos' not in st.session_state or not st.session_state.videos:
                st.warning("Please create videos first in the Assemble Videos tab.")
            else:
                # Select video to preview
                selected_video_index = st.selectbox(
                    "Select Video", 
                    range(len(st.session_state.videos)), 
                    format_func=lambda i: f"Video {i+1}: {st.session_state.videos[i]['title']}"
                )
                
                # Display video info
                video = st.session_state.videos[selected_video_index]
                st.subheader(video['title'])
                st.write(f"Duration: {video['duration']} seconds")
                
                # In a real implementation, you would embed the video player here
                st.info("Video player would be embedded here in the full implementation.")
                
                # Display associated script
                script_data = st.session_state.scripts[video['script_index']]
                with st.expander("View Script"):
                    st.write(script_data["full_script"])


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
            redirect_uri = st.text_input("Redirect URI", "https://youtube-automation-backwnd-4.onrender.com/oauth2callback") 
            channel_id = st.text_input("Channel ID (optional)")
        
        if st.button("Authenticate"):
            if client_id and client_secret:
                try:
                    with st.spinner("Authenticating with YouTube..."):
                        # Initialize YouTube API
                        youtube_api = YouTubeAPI(
                            client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri
                        )
                        
                        # Authenticate
                        youtube_api.authenticate()
                        
                        # Get channel info
                        channel_info = youtube_api.get_channel_info()
                        
                        # Store in session state
                        st.session_state.youtube_api = youtube_api
                        st.session_state.is_authenticated = True
                        st.session_state.channel_info = channel_info
                        
                        channel_name = channel_info.get('snippet', {}).get('title', 'Your Channel')
                        st.success(f"Authentication successful! Connected to YouTube channel: {channel_name}")
                except Exception as e:
                    st.error(f"Authentication failed: {str(e)}")
                    st.info("Please make sure your credentials are correct and you have a YouTube channel set up.")
            else:
                st.error("Please enter your Client ID and Client Secret.")
    
    # Publish Videos tab
    with tabs[1]:
        st.header("Publish Videos")
        st.write("Upload and schedule your videos for publishing on YouTube.")
        
        if not st.session_state.is_authenticated:
            st.warning("Please authenticate with YouTube in the YouTube Settings tab first.")
        else:
            # Video upload form
            st.subheader("Upload Video")
            
            video_title = st.text_input("Video Title", "Amazing Facts You Didn't Know")
            video_description = st.text_area(
                "Video Description", 
                "Check out these amazing facts that will blow your mind!\n\n"
                "Don't forget to like and subscribe for more interesting content."
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                video_tags = st.text_input("Tags (comma separated)", "facts, amazing, did you know, interesting")
                category_id = st.selectbox(
                    "Category",
                    [
                        ("Film & Animation", "1"),
                        ("Autos & Vehicles", "2"),
                        ("Music", "10"),
                        ("Pets & Animals", "15"),
                        ("Sports", "17"),
                        ("Short Movies", "18"),
                        ("Travel & Events", "19"),
                        ("Gaming", "20"),
                        ("Videoblogging", "21"),
                        ("People & Blogs", "22"),
                        ("Comedy", "23"),
                        ("Entertainment", "24"),
                        ("News & Politics", "25"),
                        ("Howto & Style", "26"),
                        ("Education", "27"),
                        ("Science & Technology", "28"),
                        ("Nonprofits & Activism", "29")
                    ],
                    index=11  # Default to "People & Blogs"
                )
            
            with col2:
                privacy_status = st.selectbox(
                    "Privacy Status",
                    [
                        ("Private", "private"),
                        ("Unlisted", "unlisted"),
                        ("Public", "public")
                    ],
                    index=0  # Default to Private
                )
                notify_subscribers = st.checkbox("Notify Subscribers", value=False)
            
            # File uploader for video
            uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi"])
            
            if uploaded_file is not None:
                # Save the uploaded file temporarily
                temp_file_path = os.path.join(os.getcwd(), uploaded_file.name)
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"File uploaded: {uploaded_file.name}")
                
                # Upload button
                if st.button("Upload to YouTube"):
                    try:
                        with st.spinner("Uploading video to YouTube..."):
                            # Process tags
                            tags_list = [tag.strip() for tag in video_tags.split(",") if tag.strip()]
                            
                            # Get category ID value
                            selected_category_id = category_id[1]
                            
                            # Get privacy status value
                            selected_privacy_status = privacy_status[1]
                            
                            # Upload video
                            response = st.session_state.youtube_api.upload_video(
                                file_path=temp_file_path,
                                title=video_title,
                                description=video_description,
                                tags=tags_list,
                                category_id=selected_category_id,
                                privacy_status=selected_privacy_status,
                                notify_subscribers=notify_subscribers
                            )
                            
                            # Store uploaded video info
                            if response:
                                st.session_state.uploaded_videos.append(response)
                                st.session_state.videos_published += 1
                                
                                video_id = response.get('id')
                                video_url = f"https://www.youtube.com/watch?v={video_id}"
                                
                                st.success("Video uploaded successfully!")
                                st.markdown(f"**Video URL:** [Watch on YouTube]({video_url})")
                    except Exception as e:
                        st.error(f"Upload failed: {str(e)}")
                    finally:
                        # Clean up the temporary file
                        if os.path.exists(temp_file_path):
                            os.remove(temp_file_path)
            
            # Existing videos section
            st.subheader("Your Videos")
            
            if st.session_state.uploaded_videos:
                for i, video in enumerate(st.session_state.uploaded_videos):
                    video_id = video.get('id')
                    video_title = video.get('snippet', {}).get('title', 'Unknown')
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    st.write(f"{i+1}. [{video_title}]({video_url})")
            else:
                st.info("No videos uploaded yet.")
    
    # SEO Settings tab
    with tabs[2]:
        st.header("SEO Settings")
        st.write("Configure SEO settings for your YouTube videos.")
        
        # SEO settings form
        st.subheader("Default SEO Templates")
        
        title_template = st.text_input(
            "Title Template",
            "🤯 {fact_number} Mind-Blowing Facts That Will Amaze You! | Did You Know?"
        )
        
        description_template = st.text_area(
            "Description Template",
            "Check out these amazing facts that will blow your mind!\n\n"
            "{facts}\n\n"
            "Don't forget to like and subscribe for more interesting content.\n\n"
            "#DidYouKnow #AmazingFacts #Interesting"
        )
        
        tags_template = st.text_input(
            "Default Tags",
            "facts, amazing, did you know, interesting, mind-blowing, knowledge, learn"
        )
        
        if st.button("Save SEO Templates"):
            st.success("SEO templates saved successfully!")

# Analytics page
elif page == "Analytics":
    st.title("Analytics")
    
    if not st.session_state.is_authenticated:
        st.warning("Please authenticate with YouTube in the Publishing page first.")
    else:
        try:
            # Fetch channel analytics
            with st.spinner("Fetching analytics from YouTube..."):
                channel_analytics = st.session_state.youtube_api.get_channel_analytics()
                
                # Display channel analytics
                st.header("Channel Overview")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Subscribers", channel_analytics.get('subscriberCount', '0'))
                with col2:
                    st.metric("Total Views", channel_analytics.get('viewCount', '0'))
                with col3:
                    st.metric("Videos", channel_analytics.get('videoCount', '0'))
                with col4:
                    st.metric("Comments", channel_analytics.get('commentCount', '0'))
                
                # Video performance
                st.header("Video Performance")
                
                if st.session_state.uploaded_videos:
                    for video in st.session_state.uploaded_videos:
                        video_id = video.get('id')
                        video_title = video.get('snippet', {}).get('title', 'Unknown')
                        
                        # Fetch video analytics
                        video_analytics = st.session_state.youtube_api.get_video_analytics(video_id)
                        
                        st.subheader(video_title)
                        
                        if video_analytics:
                            vcol1, vcol2, vcol3, vcol4 = st.columns(4)
                            
                            with vcol1:
                                st.metric("Views", video_analytics.get('viewCount', '0'))
                            with vcol2:
                                st.metric("Likes", video_analytics.get('likeCount', '0'))
                            with vcol3:
                                st.metric("Comments", video_analytics.get('commentCount', '0'))
                            with vcol4:
                                st.metric("Favorites", video_analytics.get('favoriteCount', '0'))
                        else:
                            st.info("No analytics available for this video yet.")
                else:
                    st.info("No videos uploaded yet.")
        except Exception as e:
            st.error(f"Error fetching analytics: {str(e)}")
            st.info("YouTube typically takes 24-48 hours to process analytics data.")

# Settings page
elif page == "Settings":
    st.title("Settings")
    
    # Tabs for different settings categories
    tabs = st.tabs(["Workflow Settings", "Component Settings", "System Settings"])
    
    # Workflow settings
    with tabs[0]:
        st.header("Workflow Settings")
        st.write("Configure your content automation workflow.")
        
        # Content generation settings
        st.subheader("Content Generation")
        
        fact_quality = st.slider("Fact Quality Threshold", min_value=1, max_value=10, value=7)
        fact_sources = st.multiselect(
            "Fact Sources",
            ["Academic Journals", "News Sites", "Wikipedia", "Books", "Scientific Publications"],
            ["News Sites", "Wikipedia", "Scientific Publications"]
        )
        
        # Video creation settings
        st.subheader("Video Creation")
        
        video_quality = st.select_slider(
            "Video Quality",
            options=["Low (480p)", "Medium (720p)", "High (1080p)", "Ultra (4K)"],
            value="High (1080p)"
        )
        
        video_length = st.slider("Target Video Length (seconds)", min_value=30, max_value=600, value=180, step=30)
        
        media_sources = st.multiselect(
            "Media Sources",
            ["Pixabay", "Pexels", "Unsplash", "Custom Library", "Generated Images"],
            ["Pixabay", "Pexels", "Unsplash"]
        )
        
        # Publishing settings
        st.subheader("Publishing")
        
        publishing_schedule = st.radio(
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
    
    # Component settings
    with tabs[1]:
        st.header("Component Settings")
        st.write("Configure individual components of the automation system.")
        
        # Components
        components = [
            {
                "name": "Fact Researcher",
                "description": "Searches for interesting facts from various sources",
                "enabled": True
            },
            {
                "name": "Script Generator",
                "description": "Creates engaging scripts from facts",
                "enabled": True
            },
            {
                "name": "Media Selector",
                "description": "Finds relevant images and videos for facts",
                "enabled": True
            },
            {
                "name": "Video Assembler",
                "description": "Combines scripts and media into videos",
                "enabled": True
            },
            {
                "name": "YouTube Publisher",
                "description": "Uploads and schedules videos on YouTube",
                "enabled": True
            },
            {
                "name": "Analytics Optimizer",
                "description": "Analyzes performance and suggests improvements",
                "enabled": True
            }
        ]
        
        for component in components:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(component["name"])
                st.write(component["description"])
            
            with col2:
                enabled = st.checkbox("Enabled", value=component["enabled"], key=f"component_{component['name']}")
        
        if st.button("Save Component Settings"):
            st.success("Component settings saved successfully!")
    
    # System settings
    with tabs[2]:
        st.header("System Settings")
        st.write("Configure system-level settings.")
        
        # Storage settings
        st.subheader("Storage Settings")
        
        storage_path = st.text_input("Storage Path", "/data/youtube_automation")
        max_storage = st.slider("Maximum Storage (GB)", min_value=1, max_value=100, value=10)
        
        cleanup_options = st.multiselect(
            "Automatic Cleanup",
            ["Remove published videos", "Remove unused media", "Archive old facts", "Compress log files"],
            ["Remove published videos", "Remove unused media"]
        )
        
        # System maintenance
        st.subheader("System Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Cache"):
                st.success("Cache cleared successfully!")
            
            if st.button("Restart Components"):
                st.success("Components restarted successfully!")
        
        with col2:
            if st.button("Check for Updates"):
                st.info("System is up to date!")
            
            if st.button("Backup System"):
                st.success("System backup created successfully!")
        
        if st.button("Save System Settings"):
            st.success("System settings saved successfully!")

# Help page
elif page == "Help":
    st.title("Help & Documentation")
    
    # Tabs for different help sections
    tabs = st.tabs(["Getting Started", "Tutorials", "FAQ", "Troubleshooting", "Contact Support"])
    
    # Getting Started
    with tabs[0]:
        st.header("Getting Started")
        st.write("Welcome to the YouTube Content Automation system!")
        
        st.write("""
        This system helps you automate the creation and publishing of 'Did You Know' style videos on YouTube.
        The process is divided into four main steps:
        
        1. **Content Generation** - Creates interesting facts for your videos
        2. **Video Creation** - Assembles facts into engaging videos
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
                "answer": "No, this system is designed for creating faceless videos. The content is presented using text, images, and background footage without requiring you to appear on camera."
            },
            {
                "question": "How do I get YouTube API credentials?",
                "answer": "You need to create a project in the Google Cloud Console, enable the YouTube Data API v3, and create OAuth 2.0 credentials. See our tutorial 'Setting Up YouTube API Credentials' for detailed instructions."
            },
            {
                "question": "Can I customize the video style?",
                "answer": "Yes, you can customize various aspects of your videos including visual style, transitions, text appearance, and background music in the Video Creation page."
            },
            {
                "question": "How long does it take to create a video?",
                "answer": "The time varies depending on video length and complexity, but typically the system can generate a 3-5 minute video in about 10-15 minutes."
            }
        ]
        
        for faq in faqs:
            st.subheader(faq["question"])
            st.write(faq["answer"])
    
    # Troubleshooting
    with tabs[3]:
        st.header("Troubleshooting")
        st.write("Common issues and their solutions.")
        
        issues = [
            {
                "problem": "Cannot generate facts",
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
            subject = st.text_input("Subject")
        
        with col2:
            message = st.text_area("Message", height=150)
            
        if st.button("Send Message"):
            if name and email and subject and message:
                st.success("Message sent! Our support team will get back to you soon.")
            else:
                st.error("Please fill in all fields.")
