
class StoryBuilder:
    def __init__(self, llm=None):
        self.llm = llm

    def assemble(self, scenes_text):
        """
        Cleans spacing, normalizes formatting, and ensures scenes appear correctly.
        """
        lines = scenes_text.split("\n")
        cleaned = []

        for line in lines:
            # remove vertical chopped lines (S\nc\ne\nn\ne)
            if len(line.strip()) == 1:
                continue

            cleaned.append(line)

        # Remove accidental double spaces
        final_story = "\n".join(cleaned)
        final_story = final_story.replace("  ", " ")

        return final_story
