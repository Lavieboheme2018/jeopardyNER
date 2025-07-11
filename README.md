# Jeopardy NER Subset Curation

This project curates structured test subsets from a Jeopardy trivia dataset (≈217k questions), designed to evaluate Named Entity Recognition (NER) models under real-world linguistic challenges.



---

## 🎯 Project Goal

Create three equal-sized 1000-question subsets for evaluating NER model performance in distinct edge cases:

| Subset | Purpose |
|--------|---------|
| **Numbers** | Evaluate entity detection of numeric phrases (dates, money, quantities) |
| **Non-English** | Test robustness to multilingual content or foreign word interference |
| **Rare Named Entities** | Challenge models to detect uncommon people, places, or organizations |

Each subset serves as a test stratum to compare how consistently a given NER model performs across different linguistic phenomena.



---

## 📂 Project Structure

```bash

jeopardyNER/
├── data/               # Original dataset
├── scripts/            # Filtering + estimation scripts
├── subsets/            # Final JSONL outputs (3 x 1000)
├── requirement.txt     # installation requirements
└── README.md
```


---

## 💻 Installation

```bash
# Create virtual environment(optional)
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy en_core model
python -m spacy download en_core_web_sm
```


---

## 📐 Design Rationale

This project is not just a data extraction task — it's a **controlled dataset engineering problem**. Each design choice reflects an intentional trade-off between coverage, accuracy, and practicality.

### ✅ Why I used regular expressions for numbers:
- Numeric expressions (e.g., `1984`, `5.0`, `$100`) follow predictable patterns.
- I chose `regex` over spaCy token-level parsing for **speed** and **simplicity**, given the high frequency of such patterns.

### ✅ Why I used `langid` over `langdetect` or `pycld3` for language detection:
- `langdetect` has unstable results on short text, and `pycld3` failed to compile in macOS + Python 3.12.
- `langid` offers a **reliable offline alternative** with good accuracy on short phrases like Jeopardy questions.

### ✅ Why I used `spaCy` for NER and rare entity detection:
- I needed to extract named entities and measure their frequency across the corpus.
- `spaCy` provides a **lightweight, production-grade NER** with interpretable entity labels and fast runtime.
- I filtered for rare entities (e.g., people or locations mentioned ≤3 times), assuming these are most likely to challenge general NER models.

### ✅ Why I focused on ‘question’ and ‘answer’ fields:
- I reviewed fields like category and round, but found they didn’t add meaningful variation for NER testing,(weakly correlated with entity extraction or introduced topic-based biases). So I kept the filtering based purely on the question and answer texts.



---

## 📁 Dataset

- **Source**: [`JEOPARDY_QUESTIONS1.json`](https://www.reddit.com/r/datasets/comments/3ggj2d/200000_jeopardy_clues_with_questions_answers/)
- **Fields used**: `question`, `answer`
- **Subsets created**:
  - `numbers_subset.jsonl`
  - `non_english_subset.jsonl`
  - `rare_proper_nouns_subset.jsonl`

Each file contains 1000 examples in JSON Lines format.



---

## 📊 Full Dataset Estimation

I ran a scan over the entire dataset to estimate how common each challenge type is, here's my result:

<img width="700" height="118" alt="Screenshot 2025-07-10 at 23 46 40" src="https://github.com/user-attachments/assets/11f7146a-4269-4e75-a142-1aca457cafe5" />




---

## ⚙️ Scripts

| Script | Description |
|--------|-------------|
| `filter_numbers.py` | Extracts examples containing numeric phrases using regex |
| `filter_non_english.py` | Filters non-English examples using `langid` |
| `filter_rare_proper_nouns.py` | Uses `spaCy` to identify rare entities from `PERSON`, `ORG`, `GPE` |
| `estimate_category_counts.py` | Scans full dataset and prints estimated counts for each category |

All outputs are saved to the `subsets/` folder.



---

## 🧠 How to Use for Model Comparison

We can use these subsets to compare NER models (e.g., spaCy, BERT, GPT) on challenging inputs:

- Recall and precision per category
- Entity type diversity (e.g., date vs person vs org)
- Mislabeling patterns (e.g., confusing money with ordinal)

Optional `ner-demo` branch runs `spaCy` NER on each subset and prints outputs for qualitative inspection.
