# Romeo

# Rival AI Labs Narrative Transformation Pipeline

* Transform Romeo & Juliet into a Rival AI Labs narrative using an end-to-end LLM-driven pipeline.

This repository implements a reproducible, prompt-driven pipeline that takes an input story and metadata, extracts narrative components, transforms the universe to a Rival AI Labs setting, generates structured story beats, and converts those beats into a polished 7-scene story. The pipeline is designed for clarity, repeatability, and assignment-grade deliverables.

# Repository structure
Romeo/
├── data/
│ └── metadata_romeo_juliet.json
├── prompts/
│ ├── extract_characters.txt
│ ├── transform_universe.txt
│ ├── generate_beats.txt
│ └── write_scenes_batch.txt
├── src/
│ ├── chain.py
│ ├── parser.py
│ ├── transformer.py
│ ├── story_builder.py
│ └── utils.py
├── final_story.txt
├── run.py
├── requirements.txt
├── .env (NOT checked in)
└── README.md

# What this project does
This project demonstrates an LLM-based multi-stage narrative pipeline that:

Parses an input (metadata + story title) to extract characters, relationships, themes, conflicts, and core plot beats.

Transforms the extracted narrative into a different universe ("Rival AI Labs").

Generates a compact list of 7 story beats that form a coherent emotional arc.

Writes a full, polished 7-scene story in a single batch LLM call (to maintain coherence).

Saves the final output to final_story.txt for submission or review.

This pipeline is deterministic enough for assignment use while remaining flexible for experimentation.


# File-by-file explanation
* Below is an explanation of each file and its role in the pipeline.

Top-level files

* run.py — Entry point for the entire pipeline. Orchestrates the sequence: load metadata → parse → transform → generate beats → write scenes (batch) → save output. Uses PromptChain and the LLM wrapper (Groq client in this implementation). Also performs validation (ensures exactly 7 beats and 7 scenes) and has retry logic.

* requirements.txt — Lists Python package requirements. Make sure this matches the runtime you use. Example packages: groq (or openai depending on provider), python-dotenv, and any other utilities.

* .env — Environment file where you store secrets like GROQ_API_KEY. This file must be listed in .gitignore and never committed.

* final_story.txt — The output story produced by the pipeline. This file is the final deliverable for the assignment.

* data/metadata_romeo_juliet.json — Input metadata for the pipeline. It can contain fields like author, summary, period, target_audience, or any additional keys you want the pipeline to consider when transforming the story.

# src folder (core code)
* parser.py — StoryParser class. Responsibilities:Read prompts/extract_characters.txt and call the LLM to extract structured narrative information from the original story or its metadata.
Returns a JSON-like structure of characters, relationships, themes, conflicts, and core_beats for downstream components.

* transformer.py — UniverseTransformer class. Responsibilities:Read prompts/transform_universe.txt and convert the parsed Romeo & Juliet structure into the Rival AI Labs setting (mapping Montague/Capulet → NeuroSpark/EchoMind, Romeo → Julian, Juliet → Aditi, etc.).
Produces a transformed JSON used by the beat generator.

* chain.py — PromptChain class. Responsibilities:Read a prompt file, substitute placeholders (e.g. {beats}, {transformed_json}), and call the LLM.Encapsulates prompt templating logic so prompts stay simple and files are small.

* story_builder.py — StoryBuilder class. Responsibilities:Assemble scenes into a clean story string.
Normalize spacing, remove broken characters, and ensure consistent ### Scene X headings.

* utils.py — Small utilities (load/save JSON, save output text, safe file helpers, validation helpers). This is intentionally small and focused.

# prompts folder (written prompts)
Each prompt is the single source of truth for what the LLM is asked to do. Keep prompts in plain text, carefully versioned.

* extract_characters.txt — Instructs the model to extract characters, relationships, themes, conflicts, and 5–7 core plot beats from the original story. Returns JSON only.

* transform_universe.txt — Instructs the model to map extracted elements onto the Rival AI Labs universe. This prompt contains mapping rules (e.g. Montagues → NeuroSpark) and must force the bittersweet ending requirement.

* generate_beats.txt — Requests EXACTLY 7 beats (numbered 1–7). Provides a required high-level arc (Expo, forced collaboration, tension, flaw discovery, crisis, sacrifice, bittersweet resolution) and strict rules (no runaway AI, no physical destruction, focus on interpersonal conflict). Returns a plain numbered list.

* write_scenes_batch.txt — The most important prompt. It asks the model to write ALL 7 scenes in one call, each starting with ### Scene X and being 2–3 paragraphs. The prompt is intentionally strict: mandatory formatting, mandatory 7 scenes, and mandatory thematic constraints. This prevents drift and ensures coherency.

# data folder
* metadata_romeo_juliet.json — Example metadata used by the parser that the system can use to ground or bias the transformation.

# Outputs
* final_story.txt — The final, polished story (7 scenes) generated by the pipeline.

# Pipeline overview (end-to-end)
* Load metadata (run.py uses utils.load_metadata).

* Extract structure (StoryParser) — uses extract_characters.txt and the LLM to return core characters, relationships, themes, and initial beats.

* Transform universe (UniverseTransformer) — uses transform_universe.txt to map elements to Rival AI Labs.

* Generate beats (PromptChain + generate_beats.txt) — create exactly 7 beats describing the full narrative arc.

* Write scenes (batch) (PromptChain + write_scenes_batch.txt) — produce all 7 scenes in one LLM call, improving global coherence.

* Assemble & save (StoryBuilder, utils.save_output) — cleanup, validation (7 scenes), and saving to final_story.txt.

# requirements
python-dotenv==1.0.0
click==8.1.7
groq
openai==1.8.0
langchain==0.1.5
tiktoken==0.5.2
python0>=3.9
pydantic==1.10.11
rich==13.6.0
pytest==7.4.2
black==24.3.0

# Design choices & prompt engineering notes
Batch scene generation (write all scenes in one call) is critical for coherence. Generating scenes one-by-one increases drift and allows the LLM to deviate from earlier beats.

Strict, explicit prompts reduce hallucination. Each prompt uses explicit "MUST" statements and formatting constraints to reduce variability.

Validation layers (scripts check for exactly 7 beats and 7 scenes) force the model to be strict or the pipeline to fail early, which is desirable when producing assignment-grade deliverables.

Separation of concerns: parsing, transformation, beat generation, and scene writing are separated into individual components for clarity and easier debugging.

# Troubleshooting & common errors
1. FileNotFoundError: prompts/extract_characters.txt

Ensure the file exists and the name/extension is correct (.txt, not .text).

2. Too few beats returned

Check prompts/generate_beats.txt to ensure it forces 7 beats and that placeholders like {transformed_json} are present and populated.

3. Fewer than 7 scenes generated

Increase max_tokens in the llm() wrapper (e.g., to 1800–2800).

Make the write_scenes_batch.txt prompt more forceful about "MUST output 7 scenes".

4. API / Rate limit errors

You might see RateLimitError or insufficient_quota. Add billing or slow your request rate; add retry/backoff logic in run.py.

5. "Wrong" characters, extra names, or drift

Verify transform_universe.txt explicitly lists the canonical character mappings.

Ensure the batch writer enforces: "DO NOT introduce new major characters."


# Testing
Unit tests: You can write unit tests to validate that clean_beats() returns 7 items and final_story.txt contains 7 ### Scene headings.

Manual inspection: Run python run.py locally, open final_story.txt, and verify constraints.

Prompt regression: Keep versions of prompt files (e.g., prompts/v1/) to roll back if editing introduces regressions.