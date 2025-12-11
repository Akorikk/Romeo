import json

class StoryParser:
    def __init__(self, llm, prompts_path="prompts/extract_characters.txt"):
        self.llm = llm
        with open(prompts_path, "r", encoding="utf-8") as f:
            self.prompt = f.read()

    def extract_structure(self, story_name, raw_metadata):
        formatted_prompt = self.prompt.format(
            story_name=story_name,
            metadata=raw_metadata
        )
        return self.llm(formatted_prompt)
