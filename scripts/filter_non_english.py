import json
import langid
from tqdm import tqdm

# Return True if the language detected is not English
def is_non_english(text):
    lang, _ = langid.classify(text)
    return lang != 'en'

with open("data/JEOPARDY_QUESTIONS1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

foreign_subset = []

# Iterate over the dataset and collect non-English entries
for item in tqdm(data):
    question = item.get("question", "")
    answer = item.get("answer", "")
    if is_non_english(question) or is_non_english(answer):
        foreign_subset.append(item)
    if len(foreign_subset) >= 1000:
        break

# Save the filtered subset
with open("subsets/non_english_subset.jsonl", "w", encoding="utf-8") as f:
    for item in foreign_subset:
        f.write(json.dumps(item) + "\n")

print("Collected", len(foreign_subset), "questions with non-English content.")
