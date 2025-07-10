import json
import spacy
from tqdm import tqdm
from collections import Counter

# Load spaCy's English model for NER
nlp = spacy.load("en_core_web_sm")

# Load full dataset
with open("data/JEOPARDY_QUESTIONS1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# First pass: Count all named entities
entity_counter = Counter()

for item in tqdm(data, desc="Counting named entities"):
    doc = nlp(item.get("question", ""))
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            entity_counter[ent.text.strip()] += 1

# Define threshold for rarity
RARE_THRESHOLD = 3

# Second pass: collect questions with rare named entities
rare_subset = []

for item in tqdm(data, desc="Selecting rare named entity examples"):
    doc = nlp(item.get("question", ""))
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            if entity_counter[ent.text.strip()] <= RARE_THRESHOLD:
                rare_subset.append(item)
                break  # Only need one rare entity match
    if len(rare_subset) >= 1000:
        break

# Save as JSONL
with open("subsets/rare_proper_nouns_subset.jsonl", "w", encoding="utf-8") as f:
    for item in rare_subset:
        f.write(json.dumps(item) + "\n")

print("Collected", len(rare_subset), "questions with rare named entities.")
