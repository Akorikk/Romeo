class StoryBuilder:
    def __init__(self, llm):
        self.llm = llm

    def assemble(self, scenes):
        story_text = "\n\n".join(scenes)
        return story_text
