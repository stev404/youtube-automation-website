# Example usage
from fact_generation import FactGenerator

# Initialize with OpenAI API key
fact_generator = FactGenerator(api_key="your_openai_api_key")

# Generate facts
facts = fact_generator.generate_facts(
    categories=["Science", "History", "Nature"],
    num_facts=10,
    fact_length="Medium",
    reliability=8
)
