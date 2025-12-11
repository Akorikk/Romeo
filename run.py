from src.parser import StoryParser
from src.transformer import UniverseTransformer
from src.chain import PromptChain
from src.story_builder import StoryBuilder
from src.utils import load_metadata, save_output

# Replace with your model call (OpenAI, Gemini, etc.)
def dummy_llm(prompt):
    # For debugging — replace with real model call
    return "LLM_OUTPUT_FOR: " + prompt[:150]

def main():
    llm = dummy_llm  # Replace with real model
    
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
    print("\nStory generated successfully!")

if __name__ == "__main__":
    main()
