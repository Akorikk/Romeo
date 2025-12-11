class UniverseTransformer:
    def __init__(self, llm, prompts_path="prompts/transform_universe.txt"):
        self.llm = llm
        with open(prompts_path, "r", encoding="utf-8") as f:
            self.prompt = f.read()

    def transform(self, extracted_json, universe="Rival AGI Labs"):
        p = self.prompt.format(
            extracted_json=extracted_json,
            universe=universe
        )
        return self.llm(p)
