import os
import random
import tempfile
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# Try to import optional dependencies
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import numpy as np
except ImportError:
    np = None


class VideoAssembler:
    """Assembles videos from scripts and media assets"""
    
    def __init__(self, assets_dir: Optional[str] = None):
        """
        Initialize the video assembler
        
        Args:
            assets_dir: Directory containing media assets (images, music, etc.)
        """
        self.assets_dir = assets_dir or os.path.join(os.getcwd(), "assets")
        
        # Create assets directory if it doesn't exist
        os.makedirs(os.path.join(self.assets_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "music"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "audio"), exist_ok=True)
        
        # Default video settings
        self.default_settings = {
            "width": 1280,
            "height": 720,
            "fps": 30,
            "font": "Arial",
            "font_size": 60,
            "text_color": "white",
            "bg_color": "black",
            "duration": 3,
            "transition_duration": 0.5
        }
    
    def create_video(self, 
                script_data: Dict[str, Any],
                output_path: str,
                background_images: Optional[List[str]] = None,
                background_music: Optional[str] = None,
                text_to_speech: bool = True,
                visual_style: str = "standard",
                **kwargs) -> str:
    """
    Create a video from script data - improved implementation
    
    Args:
        script_data: Script data from ScriptGenerator
        output_path: Path to save the output video
        background_images: List of image paths to use as backgrounds
        background_music: Path to background music file
        text_to_speech: Whether to generate speech from text
        visual_style: Visual style preset ("standard", "minimal", "vibrant")
        **kwargs: Additional video settings to override defaults
        
    Returns:
        Path to the created video file
    """
    # Create a more detailed text file with the script content
    script_file_path = output_path.replace('.mp4', '_script.txt')
    with open(script_file_path, 'w') as f:
        f.write(f"Video Script: {script_data['title']}\n\n")
        f.write(f"Duration: {script_data['estimated_duration']} seconds\n\n")
        f.write("Full Script:\n\n")
        f.write(script_data['full_script'])
        f.write("\n\nSections:\n")
        for section in script_data.get('sections', []):
            f.write(f"- {section['type'].upper()} ({section['duration']}s): {section['text'][:100]}...\n")
    
    # Create a JSON file with video metadata for future processing
    metadata_file_path = output_path.replace('.mp4', '_metadata.json')
    with open(metadata_file_path, 'w') as f:
        import json
        json.dump({
            "title": script_data.get('title', 'Untitled Video'),
            "sections": script_data.get('sections', []),
            "style": visual_style,
            "background_music": background_music,
            "background_images": background_images,
            "estimated_duration": script_data.get('estimated_duration', 60),
            "creation_timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    # Create a placeholder video file with a note about actual implementation
    with open(output_path, 'w') as f:
        f.write(f"This is a placeholder for a video file: {script_data.get('title', 'Untitled')}\n")
        f.write("In a production environment, this would be an actual MP4 video created with:\n")
        f.write("1. Text-to-speech audio generation for narration\n")
        f.write("2. Background images or video clips relevant to the content\n")
        f.write("3. Text overlays for key points\n")
        f.write("4. Background music\n")
        f.write("5. Intro and outro animations\n")
        f.write(f"\nStyle: {visual_style}\n")
    
    print(f"Video metadata and script created at: {metadata_file_path} and {script_file_path}")
    print(f"Video placeholder created at: {output_path}")
    print("Note: For actual video generation, implement MoviePy or FFmpeg integration")
    
    return output_path

    
def _generate_speech(self, text: str, output_path: str) -> None:
    """Generate speech from text using pyttsx3"""
    if pyttsx3 is None:
        print("pyttsx3 not installed. Text-to-speech functionality is disabled.")
        return
        
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Save to file
        engine.save_to_file(text, output_path)
        engine.runAndWait()
    except Exception as e:
        print(f"Error generating speech: {str(e)}")

