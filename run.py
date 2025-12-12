from src.parser import StoryParser
from src.transformer import UniverseTransformer
from src.chain import PromptChain
from src.story_builder import StoryBuilder
from src.utils import load_metadata, save_output

import time
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------------------------------
# LLM WRAPPER
# -------------------------------
def llm(prompt):
    """Groq LLaMA-3.1-8B-Instant wrapper with higher token limit"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2800,  # Prevent early cut-off
        temperature=0.8
    )
    return response.choices[0].message.content


# -------------------------------
# MAIN PIPELINE
# -------------------------------
def main():

    print("\nLoading metadata...")
    metadata = load_metadata()

    # ---------------------------
    # 1. Extract Story Structure
    # ---------------------------
    print("\nExtracting story structure...")
    parser = StoryParser(llm)
    structure = parser.extract_structure("Romeo & Juliet", metadata)
    print("✓ Structure extracted")

    # ---------------------------
    # 2. Transform Universe
    # ---------------------------
    print("\nTransforming universe...")
    transformer = UniverseTransformer(llm)
    transformed = transformer.transform(structure)
    print("✓ Universe transformed")

    # ---------------------------
    # 3. Generate Beats
    # ---------------------------
    print("\nGenerating beats...")
    chain = PromptChain(llm)
    beats_output = chain.run("prompts/generate_beats.txt", transformed_json=transformed)

    print("\nRaw beats output:")
    print(beats_output)

    # Clean beats
    clean_beats = [
        b.strip()
        for b in beats_output.split("\n")
        if len(b.strip()) > 3 and b[0].isdigit()
    ]

    print("\nCleaned 7 beats:")
    for i, beat in enumerate(clean_beats, start=1):
        print(f"{i}. {beat}")

    # Safety check
    if len(clean_beats) != 7:
        raise ValueError("❌ ERROR: Model did NOT produce exactly 7 beats! Fix prompts or retry.")

    # ---------------------------
    # 4. Generate Full Story (Batch)
    # ---------------------------
    print("\nWriting full story (batch scenes)...")

    batch_chain = PromptChain(llm)

    def generate_full_story():
        return batch_chain.run(
            "prompts/write_scenes_batch.txt",
            beats="\n".join(clean_beats)
        )

    final_story = generate_full_story()

    # Count scenes
    scene_count = final_story.count("### Scene")
    print(f"\nScene count generated: {scene_count}")

    # ---------------------------
    # Retry Logic (Force 7 scenes)
    # ---------------------------
    if scene_count != 7:
        print("⚠️ WARNING: Incorrect number of scenes. Retrying with strict instructions...\n")
        time.sleep(1)

        final_story = generate_full_story()
        scene_count = final_story.count("### Scene")

        print(f"Retry scene count: {scene_count}")

        if scene_count != 7:
            print("❌ Model FAILED to produce 7 scenes even after retry.")
            print("Saving anyway, but story may be incomplete.")

    # ---------------------------
    # 5. Save Final Story
    # ---------------------------
    save_output(final_story, "final_story.txt")
    print("\n🎉 Optimized story generated successfully! Saved as final_story.txt")


# Entry
if __name__ == "__main__":
    main()