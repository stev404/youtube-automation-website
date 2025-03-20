# Example usage
from script_creation import ScriptGenerator

# Initialize script generator
script_generator = ScriptGenerator()

# Create script from facts
script_data = script_generator.create_script_with_sections(
    facts=facts,
    title="Amazing Facts About Science",
    include_sources=True
)
