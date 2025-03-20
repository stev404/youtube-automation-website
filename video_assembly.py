# Example usage
from video_assembly import VideoAssembler

# Initialize video assembler
video_assembler = VideoAssembler()

# Create video from script
video_path = video_assembler.create_video(
    script_data=script_data,
    output_path="amazing_facts_video.mp4",
    text_to_speech=True,
    visual_style="standard"
)
