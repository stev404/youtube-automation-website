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

# Initialize with sample data
for fact in SAMPLE_FACTS:
    FACTS_DB.append({
        "id": len(FACTS_DB) + 1,
        "content": fact,
        "created_at": datetime.now().isoformat(),
        "category": random.choice(["Science", "History", "Nature", "Technology"])
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

@app.route('/api/facts/generate', methods=['POST'])
def generate_facts():
    data = request.json
    
    # Validate request
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    num_facts = data.get('num_facts', 5)
    categories = data.get('categories', ["Science", "History", "Nature", "Technology"])
    
    # Sample facts based on categories (in a real app, this would use AI)
    sample_facts_by_category = {
        "Science": [
            "The human body contains enough carbon to fill about 9,000 pencils.",
            "A teaspoonful of neutron star would weigh about 6 billion tons.",
            "The average person walks the equivalent of three times around the world in a lifetime.",
            "A day on Venus is longer than a year on Venus.",
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat."
        ],
        "History": [
            "The shortest war in history was between Britain and Zanzibar in 1896, lasting only 38 minutes.",
            "Ancient Egyptians used to use honey as an offering to their gods.",
            "The first recorded use of 'OMG' was in a 1917 letter to Winston Churchill.",
            "The Great Wall of China is not visible from space with the naked eye, contrary to popular belief.",
            "Vikings used the bones of slain animals to make their weapons stronger."
        ],
        "Nature": [
            "Octopuses have three hearts, nine brains, and blue blood.",
            "Bananas are berries, but strawberries aren't.",
            "A group of flamingos is called a 'flamboyance'.",
            "Polar bears' fur is not white—it's actually transparent and reflects visible light.",
            "Koalas sleep up to 22 hours a day."
        ],
        "Technology": [
            "The first computer bug was an actual real-life bug - a moth was found in the Harvard Mark II computer in 1947.",
            "The average smartphone user touches their phone 2,617 times a day.",
            "The first message sent over the internet was 'LO'. It was supposed to be 'LOGIN' but the system crashed.",
            "The first website is still online: http://info.cern.ch/",
            "The QWERTY keyboard layout was designed to slow typists down to prevent jamming on mechanical typewriters."
        ]
    }
    
    generated_facts = []
    for _ in range(min(num_facts, 20) ):  # Limit to 20 facts per request
        category = random.choice(categories)
        if category in sample_facts_by_category and sample_facts_by_category[category]:
            fact_content = random.choice(sample_facts_by_category[category])
            
            # Create new fact
            new_fact = {
                "id": len(FACTS_DB) + 1,
                "content": fact_content,
                "created_at": datetime.now().isoformat(),
                "category": category
            }
            
            FACTS_DB.append(new_fact)
            generated_facts.append(new_fact)
    
    return jsonify(generated_facts), 201

@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    return jsonify(SCRIPTS_DB)

@app.route('/api/scripts/generate', methods=['POST'])
def generate_scripts():
    data = request.json
    
    # Validate request
    if not data or 'fact_ids' not in data:
        return jsonify({"error": "Invalid request. 'fact_ids' field is required"}), 400
    
    fact_ids = data['fact_ids']
    script_format = data.get('format', 'Conversational')
    script_length = data.get('length', '60 seconds')
    
    generated_scripts = []
    for fact_id in fact_ids:
        # Find the fact
        fact = next((f for f in FACTS_DB if f['id'] == fact_id), None)
        if not fact:
            continue
        
        # Generate script (in a real app, this would use AI)
        script_content = f"""
[INTRO]
Did you know that {fact['content']}

[MAIN CONTENT]
That's right! This fascinating fact is just one example of the amazing world we live in.

Let's explore this a bit more...

{random.choice([
    "Scientists have been studying this phenomenon for decades.",
    "This discovery changed our understanding of the subject.",
    "Many people are surprised when they learn this fact.",
    "It's one of those things that makes you appreciate the complexity of our world.",
    "This is just one of many incredible facts about this topic."
])}

[OUTRO]
Next time you're in a conversation, share this interesting fact and watch people's reactions!
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
