import json

with open("data/JEOPARDY_QUESTIONS1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Print total number of entries and the structure of one sample item
print("Total records:", len(data))
print("Sample item:")
print(json.dumps(data[0], indent=2))
