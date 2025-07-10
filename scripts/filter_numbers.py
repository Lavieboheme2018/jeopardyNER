import json
import re
from tqdm import tqdm

# Return True if the text contains any digit or decimal number
def contains_number(text):
    return bool(re.search(r'\b\d+(\.\d+)?\b', text))

with open("data/JEOPARDY_QUESTIONS1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

numeric_subset = []

# Loop through entries and collect those with numeric phrases
for item in tqdm(data):
    question = item.get("question", "")
    answer = item.get("answer", "")
    if contains_number(question) or contains_number(answer):
        numeric_subset.append(item)
    if len(numeric_subset) >= 1000:
        break

# Save the filtered subset
with open("subsets/numbers_subset.jsonl", "w", encoding="utf-8") as f:
    for item in numeric_subset:
        f.write(json.dumps(item) + "\n")

print("Collected", len(numeric_subset), "questions with numbers.")
