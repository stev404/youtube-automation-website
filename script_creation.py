"""
Script Creation Module for YouTube Automation
Generates video scripts from facts
"""

import random
from typing import Dict, Any, List, Optional
from datetime import datetime

class ScriptGenerator:
    """
    Generates video scripts from facts
    """
    
    def __init__(self):
        """Initialize the ScriptGenerator"""
        # Different intro templates based on format
        self.intro_templates = {
            'Conversational': [
                "Hey there! Did you know that {fact}? That's pretty amazing, right?",
                "Welcome back to our channel! Today we're exploring an incredible fact: {fact}",
                "Here's something that might surprise you... {fact}. Let's dive deeper into this!",
                "I bet you didn't know that {fact}. It's one of those fascinating tidbits that makes life interesting."
            ],
            'Educational': [
                "Today we're exploring an important fact: {fact}. This has significant implications for how we understand our world.",
                "In this educational video, we'll examine the following fact: {fact}. Let's analyze what this means.",
                "Welcome to our learning series! Today's fascinating topic centers around this fact: {fact}",
                "The following information might change your perspective: {fact}. Let's explore the science behind this."
            ],
            'Entertaining': [
                "You won't believe this, but {fact}! Mind-blowing, right?",
                "Prepare to have your mind blown! {fact} - and that's just the beginning of today's amazing facts!",
                "This is going to sound crazy, but {fact}! Let's talk about why this is so incredible!",
                "Wait until you tell your friends this one... {fact}! Their reactions will be priceless!"
            ]
        }
        
        # Different main content templates
        self.main_content_templates = {
            'Conversational': [
                "Let's think about what this means. {fact} is fascinating because it shows us how complex our world really is. Many people don't realize the implications of this information.",
                "When you consider that {fact}, it makes you wonder what other amazing things we still don't know about our world. Scientists continue to study this phenomenon.",
                "I find it incredible that {fact}. It's these kinds of details that make learning about our world so rewarding. There's always something new to discover."
            ],
            'Educational': [
                "To understand why {fact}, we need to examine the underlying principles. This phenomenon occurs because of specific conditions that create this remarkable outcome.",
                "The fact that {fact} has been verified through multiple studies. Researchers have documented this through careful observation and experimentation.",
                "When we analyze {fact} more carefully, we can see how this connects to broader patterns in our world. This is consistent with what we know about related phenomena."
            ],
            'Entertaining': [
                "Can you imagine if {fact} wasn't true? Our world would be completely different! This is the kind of mind-blowing information that makes reality stranger than fiction.",
                "I was shocked when I first learned that {fact}! It's one of those facts that sounds made up but is absolutely true. The universe is full of surprises!",
                "The next time you're at a party, try telling people that {fact}. Watch their jaws drop! It's the perfect conversation starter."
            ]
        }
        
        # Different outro templates
        self.outro_templates = {
            'Conversational': [
                "Thanks for watching! If you enjoyed learning about {fact}, make sure to like and subscribe for more fascinating content.",
                "I hope you found this information about {fact} as interesting as I did. See you in the next video!",
                "Now that you know {fact}, be sure to share this video with someone who would appreciate this knowledge!"
            ],
            'Educational': [
                "Understanding that {fact} helps us build a more complete picture of our world. Join us next time for more educational content.",
                "We hope this explanation of why {fact} has been informative. Don't forget to subscribe for more in-depth explorations.",
                "Continue your learning journey with us as we explore more fascinating facts like {fact} in our upcoming videos."
            ],
            'Entertaining': [
                "Wasn't that amazing? Now you can amaze your friends by telling them that {fact}! Don't forget to like and subscribe!",
                "Mind = blown! {fact} is just one of the incredible facts we share on this channel. Stay tuned for more!",
                "If you enjoyed learning that {fact}, smash that like button and subscribe for more mind-blowing content!"
            ]
        }
    
    def generate_script(self, 
                       fact_data: Dict[str, Any],
                       format_type: str = "Conversational",
                       target_length: str = "60 seconds",
                       **kwargs) -> Dict[str, Any]:
        """
        Generate a script from a fact
        
        Args:
            fact_data: Fact data dictionary
            format_type: Script format (Conversational, Educational, Entertaining)
            target_length: Target video length
            **kwargs: Additional script parameters
            
        Returns:
            Script data dictionary
        """
        # Get fact content
        fact_content = fact_data.get('content', '')
        if not fact_content:
            raise ValueError("Fact content is required")
        
        # Validate format type
        if format_type not in self.intro_templates:
            format_type = "Conversational"  # Default to conversational
        
        # Select templates
        intro = random.choice(self.intro_templates[format_type]).format(fact=fact_content)
        main = random.choice(self.main_content_templates[format_type]).format(fact=fact_content)
        outro = random.choice(self.outro_templates[format_type]).format(fact=fact_content)
        
        # Add a random transition
        transition = random.choice([
            "This is particularly interesting when you consider the broader context.",
            "When you think about it, this reveals something profound about our world.",
            "It's these kinds of discoveries that make learning so rewarding.",
            "This fact has fascinated people for generations.",
            "Scientists continue to study this phenomenon to understand it better."
        ])
        
        # Generate full script
        full_script = f"""
[INTRO]
{intro}

[MAIN CONTENT]
{main}

{transition}

[OUTRO]
{outro}
        """
        
        # Parse target length to seconds
        if isinstance(target_length, str) and "seconds" in target_length:
            try:
                estimated_duration = int(target_length.split()[0])
            except (ValueError, IndexError):
                estimated_duration = 60  # Default to 60 seconds
        else:
            estimated_duration = 60
        
        # Create script sections for video assembly
        sections = [
            {"type": "intro", "text": intro, "duration": int(estimated_duration * 0.2)},
            {"type": "main", "text": main, "duration": int(estimated_duration * 0.5)},
            {"type": "transition", "text": transition, "duration": int(estimated_duration * 0.1)},
            {"type": "outro", "text": outro, "duration": int(estimated_duration * 0.2)}
        ]
        
        # Create script data
        script_data = {
            "id": kwargs.get('id', random.randint(1000, 9999)),
            "fact_id": fact_data.get('id', 0),
            "title": f"Did You Know: {fact_content[:50]}{'...' if len(fact_content) > 50 else ''}",
            "content": full_script,
            "full_script": full_script,
            "format": format_type,
            "length": target_length,
            "estimated_duration": estimated_duration,
            "sections": sections,
            "created_at": datetime.now().isoformat()
        }
        
        return script_data
    
    def get_available_formats(self) -> List[Dict[str, Any]]:
        """
        Get available script formats
        
        Returns:
            List of format dictionaries with name and description
        """
        return [
            {
                "name": "Conversational",
                "description": "Friendly, casual tone like talking to a friend"
            },
            {
                "name": "Educational",
                "description": "More formal, focused on learning and understanding"
            },
            {
                "name": "Entertaining",
                "description": "Energetic, exciting tone focused on amazement"
            }
        ]
