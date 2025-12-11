import json

def load_metadata(path="data/metadata_romeo_juliet.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_output(text, filename="output_story.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
