import json
import re
import langid
import spacy
from tqdm import tqdm
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load dataset
with open("data/JEOPARDY_QUESTIONS1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Regex to detect numeric content
def contains_number(text):
    return bool(re.search(r'\b\d+(\.\d+)?\b', text))

# Language detection
def is_non_english(text):
    try:
        lang, _ = langid.classify(text)
        return lang != 'en'
    except:
        return False

# First pass: count all named entities to detect rare ones
entity_counter = Counter()
for item in tqdm(data, desc="Counting named entities"):
    doc = nlp(item.get("question", ""))
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            entity_counter[ent.text.strip()] += 1

# rarity threshold
RARE_THRESHOLD = 3

# Counters 
number_count = 0
foreign_count = 0
rare_entity_count = 0

# Final pass 
for item in tqdm(data, desc="Estimating category totals"):
    q = item.get("question", "")
    a = item.get("answer", "")

    # 1: contains numbers
    if contains_number(q) or contains_number(a):
        number_count += 1

    # 2: contains non-English text
    if is_non_english(q) or is_non_english(a):
        foreign_count += 1

    # 3: contains rare named entities
    doc = nlp(q)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            if entity_counter[ent.text.strip()] <= RARE_THRESHOLD:
                rare_entity_count += 1
                break  


print("\n=== Estimation Summary ===")
print(f"Total questions: {len(data)}")
print(f"Questions with numbers: {number_count}")
print(f"Questions with non-English words: {foreign_count}")
print(f"Questions with rare named entities: {rare_entity_count}")
