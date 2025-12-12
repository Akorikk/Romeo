from src.parser import StoryParser
from src.transformer import UniverseTransformer
from src.chain import PromptChain
from src.story_builder import StoryBuilder
from src.utils import load_metadata, save_output
import time

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Fast LLM
def llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content


def main():

    print("\nLoading original metadata...")
    metadata = load_metadata()

    print("\nExtracting narrative structure...")
    parser = StoryParser(llm)
    extracted = parser.extract_structure("Romeo & Juliet", metadata)
    print("✓ Narrative structure extracted.")

    print("\nTransforming universe...")
    transformer = UniverseTransformer(llm)
    transformed = transformer.transform(extracted)
    print("✓ Universe transformed.")

    print("\nGenerating story beats...")
    chain = PromptChain(llm)
    beats_output = chain.run("prompts/generate_beats.txt", transformed_json=transformed)
    print("✓ Beats generated.")

    print("\nWriting scenes (batch mode)...")
    scenes_text = chain.run("prompts/write_scenes_batch.txt", beats=beats_output)

    scenes = [sc.strip() for sc in scenes_text.split("### ") if sc.strip()]
    scenes = ["### " + sc for sc in scenes]

    print("\nAssembling final story...")
    builder = StoryBuilder(llm)
    final_story = builder.assemble(scenes)

    save_output(final_story, "final_story.txt")
    print("\n🎉 Story generated successfully! File saved as final_story.txt")


if __name__ == "__main__":
    main()