from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Sample data storage (in a real app, this would be a database)
FACTS_DB = []
SCRIPTS_DB = []
VIDEOS_DB = []
PUBLISHED_VIDEOS_DB = []

# Sample facts for initial data
SAMPLE_FACTS = [
    "The human body contains enough carbon to fill about 9,000 pencils.",
    "A teaspoonful of neutron star would weigh about 6 billion tons.",
    "The shortest war in history was between Britain and Zanzibar in 1896, lasting only 38 minutes.",
    "Octopuses have three hearts, nine brains, and blue blood.",
    "Bananas are berries, but strawberries aren't.",
    "A group of flamingos is called a 'flamboyance'.",
    "There are more stars in the universe than grains of sand on all the beaches on Earth.",
    "The first computer bug was an actual real-life bug - a moth was found in the Harvard Mark II computer in 1947.",
    "The average smartphone user touches their phone 2,617 times a day."
]
# Add this function to your API integration code
def publish_to_youtube(video_id, youtube_credentials):
    """
    Publish a video to YouTube using the provided credentials
    """
    client_id = youtube_credentials.get("client_id")
    client_secret = youtube_credentials.get("client_secret")
    
    if not client_id or not client_secret:
        return {"error": "YouTube API credentials not configured"}
    
    # In a real implementation, you would use these credentials to authenticate with YouTube API
    # and upload the video
    
    # For now, just call your existing publish endpoint
    response = requests.post(
        f"{BACKEND_URL}/api/publish",
        json={"video_ids": [video_id]}
    )
    
    return response.json()

# Initialize with sample data
for fact in SAMPLE_FACTS:
    FACTS_DB.append({
        "id": len(FACTS_DB) + 1,
        "content": fact,
        "created_at": datetime.now().isoformat(),
        "category": random.choice(["Science", "History", "Nature", "Technology"])
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "YouTube Content Automation API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "facts": "/api/facts",
            "scripts": "/api/scripts",
            "videos": "/api/videos",
            "publish": "/api/publish",
            "analytics": "/api/analytics"
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/facts', methods=['GET'])
def get_facts():
    return jsonify(FACTS_DB)

@app.route('/api/facts', methods=['POST'])
def create_facts():
    data = request.json
    
    # Validate request
    if not data or 'content' not in data:
        return jsonify({"error": "Invalid request. 'content' field is required"}), 400
    
    # Create new fact
    new_fact = {
        "id": len(FACTS_DB) + 1,
        "content": data['content'],
        "created_at": datetime.now().isoformat(),
        "category": data.get('category', 'General')
    }
    
    FACTS_DB.append(new_fact)
    return jsonify(new_fact), 201

@app.route('/api/scripts/generate', methods=['POST'])
def generate_scripts():
    data = request.json
    
    # Validate request
    if not data or 'fact_ids' not in data:
        return jsonify({"error": "Invalid request. 'fact_ids' field is required"}), 400
    
    fact_ids = data['fact_ids']
    script_format = data.get('format', 'Conversational')
    script_length = data.get('length', '60 seconds')
    
    # Different intro templates based on format
    intro_templates = {
        'Conversational': [
            # Add at least 4 templates here
        ],
        'Educational': [
            # Add at least 4 templates here
        ],
        'Entertaining': [
            # Add at least 4 templates here
        ]
    }
    
    # Different main content templates
    main_content_templates = {
        'Conversational': [
            # Add at least 3 templates here
        ],
        'Educational': [
            # Add at least 3 templates here
        ],
        'Entertaining': [
            # Add at least 3 templates here
        ]
    }
    
    # Different outro templates
    outro_templates = {
        'Conversational': [
            # Add at least 3 templates here
        ],
        'Educational': [
            # Add at least 3 templates here
        ],
        'Entertaining': [
            # Add at least 3 templates here
        ]
    }
    
    generated_scripts = []
    for fact_id in fact_ids:
        # Find the fact
        fact = next((f for f in FACTS_DB if f['id'] == fact_id), None)
        if not fact:
            continue
        
        # Select appropriate templates based on format
        format_key = script_format if script_format in intro_templates else 'Conversational'
        
        intro = random.choice(intro_templates[format_key]).format(fact=fact['content'])
        main = random.choice(main_content_templates[format_key]).format(fact=fact['content'])
        outro = random.choice(outro_templates[format_key]).format(fact=fact['content'])
        
        # Generate script with more variety
        script_content = f"""
[INTRO]
{intro}

[MAIN CONTENT]
{main}

{random.choice([
    "This is particularly interesting when you consider the broader context.",
    "When you think about it, this reveals something profound about our world.",
    "It's these kinds of discoveries that make learning so rewarding.",
    "This fact has fascinated people for generations.",
    "Scientists continue to study this phenomenon to understand it better."
])}

[OUTRO]
{outro}
        """
        
        # Create new script
        new_script = {
            "id": len(SCRIPTS_DB) + 1,
            "fact_id": fact_id,
            "content": script_content,
            "format": script_format,
            "length": script_length,
            "created_at": datetime.now().isoformat()
        }
        
        SCRIPTS_DB.append(new_script)
        generated_scripts.append(new_script)
    
    return jsonify(generated_scripts), 201


@app.route('/api/videos', methods=['GET'])
def get_videos():
    return jsonify(VIDEOS_DB)

@app.route('/api/videos/assemble', methods=['POST'])
def assemble_videos():
    data = request.json
    
    # Validate request
    if not data or 'script_ids' not in data:
        return jsonify({"error": "Invalid request. 'script_ids' field is required"}), 400
    
    script_ids = data['script_ids']
    resolution = data.get('resolution', '1080p')
    voice_type = data.get('voice_type', 'Male')
    
    assembled_videos = []
    for script_id in script_ids:
        # Find the script
        script = next((s for s in SCRIPTS_DB if s['id'] == script_id), None)
        if not script:
            continue
        
        # Find the fact
        fact = next((f for f in FACTS_DB if f['id'] == script['fact_id']), None)
        if not fact:
            continue
        
        # Generate video metadata (in a real app, this would create an actual video)
        title = f"Did You Know: {fact['content'][:50]}..." if len(fact['content']) > 50 else f"Did You Know: {fact['content']}"
        
        # Create new video
        new_video = {
            "id": len(VIDEOS_DB) + 1,
            "script_id": script_id,
            "title": title,
            "duration": script['length'],
            "resolution": resolution,
            "voice_type": voice_type,
            "status": "Ready",
            "created_at": datetime.now().isoformat()
        }
        
        VIDEOS_DB.append(new_video)
        assembled_videos.append(new_video)
    
    return jsonify(assembled_videos), 201

@app.route('/api/publish', methods=['POST'])
def publish_videos():
    data = request.json
    
    # Validate request
    if not data or 'video_ids' not in data:
        return jsonify({"error": "Invalid request. 'video_ids' field is required"}), 400
    
    video_ids = data['video_ids']
    privacy = data.get('privacy', 'Public')
    
    published_videos = []
    for video_id in video_ids:
        # Find the video
        video = next((v for v in VIDEOS_DB if v['id'] == video_id), None)
        if not video:
            continue
        
        # Create published video (in a real app, this would upload to YouTube)
        new_published_video = {
            "id": len(PUBLISHED_VIDEOS_DB) + 1,
            "video_id": video_id,
            "title": video['title'],
            "privacy": privacy,
            "youtube_url": f"https://youtube.com/watch?v=example{video_id}",
            "published_at": datetime.now() .isoformat()
        }
        
        PUBLISHED_VIDEOS_DB.append(new_published_video)
        published_videos.append(new_published_video)
    
    return jsonify(published_videos), 201

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    # In a real app, this would fetch data from YouTube Analytics API
    return jsonify({
        "views": 1248,
        "watch_time": 78.3,
        "subscribers": 156,
        "revenue": 12.47,
        "top_videos": [
            {"title": "Amazing Facts About Octopuses", "views": 487, "watch_time": 32.4, "ctr": 8.2},
            {"title": "The Shortest War in History", "views": 342, "watch_time": 25.1, "ctr": 7.5},
            {"title": "Fascinating Facts About Bananas", "views": 289, "watch_time": 18.7, "ctr": 6.9}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
