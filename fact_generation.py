# Example usage
from fact_generation import FactGenerator

# Initialize with OpenAI API key
fact_generator = FactGenerator(api_key="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")

# Generate facts
facts = fact_generator.generate_facts(
    categories=["Science", "History", "Nature"],
    num_facts=10,
    fact_length="Medium",
    reliability=8
)
