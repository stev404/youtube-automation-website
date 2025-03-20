"""
Script Creation Module for YouTube Content Automation
Converts facts into engaging video scripts
"""

import random
from typing import List, Dict, Any, Optional

class ScriptGenerator:
    """Generates video scripts from facts"""
    
    def __init__(self):
        """Initialize the script generator"""
        # Templates for script components
        self.intro_templates = [
            "Welcome to another episode of Amazing Facts! Today, we're going to explore some mind-blowing information that will leave you saying 'Wow!'",
            "Did you know? In today's video, we'll share some fascinating facts that will make you the most interesting person in any conversation.",
            "Get ready to be amazed! These incredible facts will change the way you see the world around you.",
            "Hello curious minds! Today we're diving into some extraordinary facts that most people don't know about.",
            "Prepare to have your mind blown! These amazing facts will make you question everything you thought you knew."
        ]
        
        self.transition_templates = [
            "But that's not all! Here's another fascinating fact...",
            "Moving on to our next amazing discovery...",
            "Wait until you hear this next one...",
            "If you thought that was interesting, check this out...",
            "Here's something else that will surprise you...",
            "Now for another mind-blowing fact...",
            "Let's continue with another incredible piece of information...",
            "The next fact is equally amazing...",
            "You won't believe this next one..."
        ]
        
        self.conclusion_templates = [
            "Thanks for watching! If you enjoyed these facts, don't forget to like and subscribe for more amazing content.",
            "Which fact surprised you the most? Let us know in the comments below, and don't forget to subscribe for more fascinating videos!",
            "We hope you learned something new today! Hit that subscribe button for more incredible facts every week.",
            "If you enjoyed this video, give it a thumbs up and share it with a friend who loves learning new things!",
            "That's all for today's amazing facts! Subscribe for more mind-blowing information in our next video."
        ]
        
    def create_script(self, 
                     facts: List[Dict[str, Any]], 
                     title: Optional[str] = None,
                     include_sources: bool = False,
                     custom_intro: Optional[str] = None,
                     custom_conclusion: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a complete video script from a list of facts
        
        Args:
            facts: List of fact dictionaries with 'text' and optionally 'source' and 'category'
            title: Optional custom title for the video
            include_sources: Whether to include sources in the script
            custom_intro: Optional custom introduction
            custom_conclusion: Optional custom conclusion
            
        Returns:
            Dictionary containing the complete script and metadata
        """
        if not facts:
            raise ValueError("At least one fact is required to create a script")
            
        # Generate title if not provided
        if not title:
            categories = set(fact.get('category', '') for fact in facts if 'category' in fact)
            if categories:
                category_str = " and ".join(list(categories)[:2])
                title = f"Amazing Facts About {category_str} You Probably Didn't Know"
            else:
                title = "Mind-Blowing Facts That Will Amaze You"
                
        # Create script sections
        intro = custom_intro if custom_intro else random.choice(self.intro_templates)
        conclusion = custom_conclusion if custom_conclusion else random.choice(self.conclusion_templates)
        
        # Build the main content with facts and transitions
        main_content = []
        for i, fact in enumerate(facts):
            fact_text = fact['text']
            
            # Add source if requested
            if include_sources and 'source' in fact:
                fact_text += f" (Source: {fact['source']})"
                
            main_content.append(fact_text)
            
            # Add transition between facts (except after the last fact)
            if i < len(facts) - 1:
                main_content.append(random.choice(self.transition_templates))
                
        # Combine all script components
        full_script = [intro] + main_content + [conclusion]
        
        # Create script metadata
        script_data = {
            "title": title,
            "intro": intro,
            "facts": facts,
            "transitions": [main_content[i] for i in range(1, len(main_content), 2)] if len(main_content) > 1 else [],
            "conclusion": conclusion,
            "full_script": "\n\n".join(full_script),
            "word_count": len("\n\n".join(full_script).split()),
            "fact_count": len(facts)
        }
        
        return script_data
        
    def create_script_with_sections(self,
                                  facts: List[Dict[str, Any]],
                                  title: Optional[str] = None,
                                  include_sources: bool = False) -> Dict[str, Any]:
        """
        Create a script with clearly defined sections for video creation
        
        Args:
            facts: List of fact dictionaries
            title: Optional custom title
            include_sources: Whether to include sources
            
        Returns:
            Dictionary with script sections and metadata
        """
        # Get basic script
        script_data = self.create_script(
            facts, 
            title=title,
            include_sources=include_sources
        )
        
        # Create structured sections for video creation
        sections = []
        
        # Add intro section
        sections.append({
            "type": "intro",
            "text": script_data["intro"],
            "duration": 8  # Approximate seconds
        })
        
        # Add fact sections with transitions
        for i, fact in enumerate(facts):
            # Add fact
            sections.append({
                "type": "fact",
                "text": fact["text"],
                "source": fact.get("source", ""),
                "category": fact.get("category", ""),
                "fact_number": i + 1,
                "duration": 10  # Approximate seconds per fact
            })
            
            # Add transition (except after last fact)
            if i < len(facts) - 1:
                transition_text = script_data["transitions"][i] if i < len(script_data["transitions"]) else random.choice(self.transition_templates)
                sections.append({
                    "type": "transition",
                    "text": transition_text,
                    "duration": 3  # Approximate seconds
                })
                
        # Add conclusion section
        sections.append({
            "type": "conclusion",
            "text": script_data["conclusion"],
            "duration": 8  # Approximate seconds
        })
        
        # Calculate total duration
        total_duration = sum(section["duration"] for section in sections)
        
        # Add sections to script data
        script_data["sections"] = sections
        script_data["estimated_duration"] = total_duration
        
        return script_data
        
    def format_script_for_tts(self, script_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format script for text-to-speech processing
        
        Args:
            script_data: Script data from create_script_with_sections
            
        Returns:
            List of dictionaries with text and metadata for TTS
        """
        tts_segments = []
        
        for section in script_data.get("sections", []):
            tts_segments.append({
                "text": section["text"],
                "type": section["type"],
                "duration": section["duration"],
                "fact_number": section.get("fact_number", None)
            })
            
        return tts_segments
