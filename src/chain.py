class PromptChain:
    def __init__(self, llm):
        self.llm = llm

    def run(self, prompt_path, **kwargs):
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()

        final_prompt = template.format(**kwargs)
        return self.llm(final_prompt)
