#!/bin/bash

mkdir -p prompts
mkdir -p data
mkdir -p src

touch prompts/extract_characters.text
touch prompts/transform_universe.txt
touch prompts/generate_beats.txt
touch prompts/write_scenes.txt
touch prompts/assemble_story.txt

touch data/metadata_romeo_juliet.json


touch src/parser.py
touch src/transformer.py
touch src/chain.py
touch src/story_builder.py
touch src/utils.py

touch notebooks/invoice_pipeline_demo.ipynb

touch requirements.txt


echo "Fresh project created!"