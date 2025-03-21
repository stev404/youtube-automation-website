"""
Video Assembly Module for YouTube Automation
Creates videos from scripts and assets
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import random

class VideoAssembler:
    """
    Assembles videos from scripts and assets
    """
    
    def __init__(self, output_dir: str = "output", assets_dir: str = "assets"):
        """
        Initialize the VideoAssembler
        
        Args:
            output_dir: Directory to save output videos
            assets_dir: Directory containing assets (images, music)
        """
        self.output_dir = output_dir
        self.assets_dir = assets_dir
        
        # Create directories if they don't exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(os.path.join(assets_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(assets_dir, "music"), exist_ok=True)
    
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
            f.write(f"Video Script: {script_data.get('title', 'Untitled Video')}\n\n")
            f.write(f"Duration: {script_data.get('estimated_duration', 60)} seconds\n\n")
            f.write("Full Script:\n\n")
            f.write(script_data.get('full_script', script_data.get('content', 'No script content')))
            f.write("\n\nSections:\n")
            for section in script_data.get('sections', []):
                f.write(f"- {section.get('type', 'SECTION').upper()} ({section.get('duration', 10)}s): {section.get('text', '')[:100]}...\n")
        
        # Create a JSON file with video metadata for future processing
        metadata_file_path = output_path.replace('.mp4', '_metadata.json')
        with open(metadata_file_path, 'w') as f:
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
    
    def get_available_styles(self) -> List[Dict[str, Any]]:
        """
        Get available visual styles for videos
        
        Returns:
            List of style dictionaries with name and description
        """
        return [
            {
                "name": "standard",
                "description": "Clean, professional look with subtle animations"
            },
            {
                "name": "minimal",
                "description": "Simple, text-focused design with minimal distractions"
            },
            {
                "name": "vibrant",
                "description": "Colorful, energetic style with bold text and animations"
            },
            {
                "name": "educational",
                "description": "Focused on clarity with diagrams and explanatory elements"
            }
        ]
    
    def get_available_background_music(self) -> List[Dict[str, Any]]:
        """
        Get available background music tracks
        
        Returns:
            List of music dictionaries with name and path
        """
        music_dir = os.path.join(self.assets_dir, "music")
        music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))] if os.path.exists(music_dir) else []
        
        # If no music files found, return placeholder data
        if not music_files:
            return [
                {
                    "name": "Upbeat",
                    "path": "placeholder_upbeat.mp3",
                    "description": "Energetic and positive background music"
                },
                {
                    "name": "Calm",
                    "path": "placeholder_calm.mp3",
                    "description": "Relaxing and peaceful background music"
                },
                {
                    "name": "Mysterious",
                    "path": "placeholder_mysterious.mp3",
                    "description": "Intriguing and curious background music"
                }
            ]
        
        # Return actual music files
        return [
            {
                "name": os.path.splitext(f)[0],
                "path": os.path.join(music_dir, f),
                "description": f"Background music: {os.path.splitext(f)[0]}"
            } for f in music_files
        ]
