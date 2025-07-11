# Jeopardy NER Subset Curation

This project extracts specific subsets from a large Jeopardy question dataset (about 217k entries). The goal is to create small, focused test sets that help us evaluate how well Named Entity Recognition (NER) models handle different types of language.



---

## What This Project Does

I generate three sets of 1000 questions each:

| Subset                      | What's In It                                          |
| --------------------------- | ----------------------------------------------------- |
| **Numbers**                 | Questions with dates, prices, or numeric info         |
| **Non-English**             | Questions with words from other languages             |
| **Uncommon Named Entities** | Questions that mention rare people, places, or titles |

These are useful to test if an NER model struggles with specific kinds of inputs


---

## How It Works(curation process)

1. Load the full dataset from `JEOPARDY_QUESTIONS1.json`.
2. Go through each question and the answer.
3. Use simple tools like regular expressions, language detection, and spaCy to filter for the target patterns.
4. Once we collect 1000 matching questions for each case, we save them into .jsonl files.
5. We stop collecting as soon as we hit 1000 matches per type, so processing stays fast.
   

---
## Helper Functions and Libraries Used

- `contains_number(text)`  
  Uses regular expressions to catch numbers like years, prices, and quantities.
  `re` : Python’s built-in regex module, used to match number patterns.


- `is_non_english(text)`  
  Uses langid to check if a question contains non-English words.
  `langid` : language identification library. It’s a quick way to flag multilingual content.

  
- `rare_subset(text)`  
  Uses spaCy to extract named entities and checks if they appear rarely across the dataset
  `spaCy` : NLP library useful for Named Entity Recognition.


- `tqdm`: shows a progress bar


---

## Output Files

1. numbers_subset.jsonl
2. non_english_subset.jsonl
3. rare_proper_nouns_subset.jsonl

Each has 1000 curated questions.


---

## Total Estimation


<img width="700" height="118" alt="Screenshot 2025-07-10 at 23 46 40" src="https://github.com/user-attachments/assets/11f7146a-4269-4e75-a142-1aca457cafe5" />

---

### Setups(optional)

```bash
# Create virtual environment(optional)
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy en_core model
python -m spacy download en_core_web_sm
```

---

### Notes and trade-offs
- Using `langid` for language detection
I tried other options, `langdetect` gave unstable results on short text, and `pycld3` didn’t work on Macbook setup. `langid` ran smoothly and worked well for short Jeopardy questions.

- Using `spaCy` for named entity detection
I needed to find people, places, and other named entities — and see how common they were. `spaCy` gave me both, with good speed and easy-to-understand labels.

- Why I focused on the question and answer fields
I looked at other fields like category or round, but they didn’t help much for NER. The real value is in the question text itself, so I kept it simple and focused on that.

