from src.parser import StoryParser
from src.transformer import UniverseTransformer
from src.chain import PromptChain
from src.story_builder import StoryBuilder
from src.utils import load_metadata, save_output

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Real LLM function
def llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # or gpt-4.1 or gpt-4o
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]


# -------------------------
# MAIN PIPELINE
# -------------------------
def main():

    print("\nLoading original metadata...")
    metadata = load_metadata()

    print("\nExtracting narrative structure...")
    parser = StoryParser(llm)
    extracted = parser.extract_structure("Romeo & Juliet", metadata)

    print("\nTransforming universe...")
    transformer = UniverseTransformer(llm)
    transformed = transformer.transform(extracted)

    print("\nGenerating story beats...")
    chain = PromptChain(llm)
    beats_output = chain.run("prompts/generate_beats.txt", transformed_json=transformed)

    print("\nWriting scenes...")
    beats = beats_output.split("\n")
    scenes = []
    for b in beats:
        if len(b.strip()) < 3:
            continue
        scene = chain.run("prompts/write_scenes.txt", beat=b)
        scenes.append(scene)

    print("\nAssembling final story...")
    builder = StoryBuilder(llm)
    final_story = builder.assemble(scenes)

    save_output(final_story, "final_story.txt")
    print("\nStory generated successfully! File saved as final_story.txt")


# Entry point
if __name__ == "__main__":
    main()
