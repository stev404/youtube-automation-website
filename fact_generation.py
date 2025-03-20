"""
Fact Generation Module for YouTube Content Automation
Uses OpenAI API to generate interesting facts for videos
"""

import os
import openai
import random
import json
from typing import List, Dict, Any, Optional

class FactGenerator:
    """Generates interesting facts using OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the fact generator with OpenAI API key"""
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
            
    def set_api_key(self, api_key: str):
        """Set or update the OpenAI API key"""
        self.api_key = api_key
        openai.api_key = api_key
        
    def generate_facts(self, 
                      categories: List[str], 
                      num_facts: int = 10, 
                      fact_length: str = "Medium",
                      reliability: int = 8) -> List[Dict[str, Any]]:
        """
        Generate interesting facts based on specified categories
        
        Args:
            categories: List of categories to generate facts for
            num_facts: Number of facts to generate
            fact_length: Length of facts ("Short", "Medium", "Long")
            reliability: Source reliability score (1-10)
            
        Returns:
            List of dictionaries containing generated facts and metadata
        """
        import openai                 
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Use set_api_key() to set it.")
            
        # Validate inputs
        if not categories:
            raise ValueError("At least one category must be specified")
        if num_facts < 1:
            raise ValueError("Number of facts must be at least 1")
            
        # Map fact length to word count
        length_map = {
            "Short": "20-30 words",
            "Medium": "40-60 words",
            "Long": "80-100 words"
        }
        word_count = length_map.get(fact_length, "40-60 words")
        
        # Prepare system message based on reliability
        system_message = self._get_system_message(reliability)
        
        # Generate facts for each category
        all_facts = []
        facts_per_category = max(1, num_facts // len(categories))
        remaining_facts = num_facts - (facts_per_category * len(categories))
        
        for category in categories:
            # Determine how many facts to generate for this category
            category_facts_count = facts_per_category
            if remaining_facts > 0:
                category_facts_count += 1
                remaining_facts -= 1
                
            # Generate facts for this category
            facts = self._generate_category_facts(
                category, 
                category_facts_count, 
                word_count, 
                system_message
            )
            
            all_facts.extend(facts)
            
            # Check if we have enough facts
            if len(all_facts) >= num_facts:
                break
                
        # Shuffle facts to mix categories
        random.shuffle(all_facts)
        
        return all_facts[:num_facts]
    
    def _get_system_message(self, reliability: int) -> str:
        """Generate system message based on reliability score"""
        if reliability >= 9:
            return ("You are a fact researcher with a strong commitment to accuracy. "
                   "Only provide facts that are well-established and can be verified "
                   "by multiple reputable academic sources. Include specific details "
                   "and context that make the facts more interesting and educational.")
        elif reliability >= 7:
            return ("You are a fact researcher who provides interesting and accurate "
                   "information. Focus on facts that are supported by reputable sources "
                   "while still being engaging and surprising to general audiences.")
        elif reliability >= 5:
            return ("You are a fact researcher who provides interesting information. "
                   "Balance accuracy with entertainment value, focusing on facts that "
                   "are generally accurate but also surprising and engaging.")
        else:
            return ("You are a fact researcher who provides entertaining and surprising "
                   "information. Focus on unusual, counterintuitive, and attention-grabbing "
                   "facts that will interest general audiences, even if they're somewhat "
                   "simplified or not universally accepted.")
    
    def _generate_category_facts(self, 
                               category: str, 
                               num_facts: int, 
                               word_count: str,
                               system_message: str) -> List[Dict[str, Any]]:
        """Generate facts for a specific category"""
        try:
            # Create prompt for the category
            user_message = (
                f"Generate {num_facts} interesting, surprising 'Did You Know' facts about {category}. "
                f"Each fact should be {word_count} in length. "
                f"Make the facts engaging, educational, and conversation-worthy. "
                f"Format the response as a JSON array with each fact having 'text' and 'source' fields. "
                f"For the source, provide a plausible source category like 'Scientific Journal', 'Historical Records', etc."
            )
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse response
            content = response.choices[0].message.content
            facts_data = json.loads(content)
            
            # Process facts
            facts = []
            for fact in facts_data.get("facts", []):
                facts.append({
                    "text": fact.get("text", ""),
                    "source": fact.get("source", "Unknown"),
                    "category": category
                })
                
            return facts
            
        except Exception as e:
            print(f"Error generating facts for {category}: {str(e)}")
            # Return placeholder facts in case of error
            return [{
                "text": f"An interesting fact about {category} would normally appear here.",
                "source": "Error in fact generation",
                "category": category,
                "error": str(e)
            }] * num_facts
            
    def get_sample_facts(self, categories: List[str], num_facts: int = 10) -> List[Dict[str, Any]]:
        """
        Get sample facts when API is not available
        This is a fallback method that doesn't require an API key
        """
        sample_facts = {
            "Science": [
                {
                    "text": "The human body contains enough carbon to fill about 9,000 pencils.",
                    "source": "Scientific American",
                    "category": "Science"
                },
                {
                    "text": "A teaspoonful of neutron star would weigh about 6 billion tons.",
                    "source": "NASA Astrophysics",
                    "category": "Science"
                },
                {
                    "text": "The average person walks the equivalent of three times around the world in a lifetime.",
                    "source": "Health Research Institute",
                    "category": "Science"
                }
            ],
            "History": [
                {
                    "text": "The shortest war in history was between Britain and Zanzibar in 1896, lasting only 38 minutes.",
                    "source": "Historical Archives",
                    "category": "History"
                },
                {
                    "text": "Ancient Egyptians used to use honey as an offering to their gods.",
                    "source": "Archaeological Studies",
                    "category": "History"
                },
                {
                    "text": "The first recorded use of 'OMG' was in a 1917 letter to Winston Churchill.",
                    "source": "British Library Archives",
                    "category": "History"
                }
            ],
            "Nature": [
                {
                    "text": "Octopuses have three hearts, nine brains, and blue blood.",
                    "source": "Marine Biology Journal",
                    "category": "Nature"
                },
                {
                    "text": "Bananas are berries, but strawberries aren't.",
                    "source": "Botanical Classification",
                    "category": "Nature"
                },
                {
                    "text": "A group of flamingos is called a 'flamboyance'.",
                    "source": "Ornithological Society",
                    "category": "Nature"
                }
            ],
            "Space": [
                {
                    "text": "There are more stars in the universe than grains of sand on all the beaches on Earth.",
                    "source": "Astronomical Society",
                    "category": "Space"
                },
                {
                    "text": "A day on Venus is longer than a year on Venus.",
                    "source": "Planetary Science Institute",
                    "category": "Space"
                },
                {
                    "text": "The Great Red Spot on Jupiter is a storm that has been raging for at least 400 years.",
                    "source": "NASA Jupiter Mission",
                    "category": "Space"
                }
            ],
            "Technology": [
                {
                    "text": "The first computer bug was an actual real-life bug - a moth was found in the Harvard Mark II computer in 1947.",
                    "source": "Computer History Museum",
                    "category": "Technology"
                },
                {
                    "text": "The average smartphone user touches their phone 2,617 times a day.",
                    "source": "Digital Behavior Research",
                    "category": "Technology"
                },
                {
                    "text": "The first message sent over the internet was 'LO'. It was supposed to be 'LOGIN' but the system crashed.",
                    "source": "Internet History Archives",
                    "category": "Technology"
                }
            ]
        }
        
        # Collect facts from selected categories
        all_facts = []
        for category in categories:
            if category in sample_facts:
                all_facts.extend(sample_facts[category])
                
        # If we don't have enough facts, add from other categories
        if len(all_facts) < num_facts:
            for category in sample_facts:
                if category not in categories:
                    all_facts.extend(sample_facts[category])
                    if len(all_facts) >= num_facts:
                        break
                        
        # Shuffle and return requested number of facts
        random.shuffle(all_facts)
        return all_facts[:num_facts]
