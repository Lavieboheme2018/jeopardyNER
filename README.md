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

## 🧩 Curation Process Overview

The curation pipeline is designed to extract three controlled subsets of Jeopardy questions to evaluate NER model performance under specific linguistic conditions. The overall process works as follows:

1. **Load the full dataset** (~217,000 entries) from `JEOPARDY_QUESTIONS1.json`.
2. **Pass 1**: For each data point, analyze the `question` (and occasionally the `answer`) field to detect one of the following patterns:
   - Numeric content (e.g., years, amounts)
   - Non-English phrases
   - Named entities that are rare across the dataset
3. **Use heuristics or lightweight NLP tools** (e.g., regex, language detection, entity frequency) to filter relevant items.
4. **Collect 1000 matching entries per category**, stopping early for efficiency once the count is met.
5. **Output results** in newline-delimited JSON (`.jsonl`) for easy downstream use.

Each subset is mutually independent and uniformly sized, enabling fair model evaluation and performance comparison across different types of language challenges.

---
## 🛠️ Helper Functions

The core logic uses a few small helper functions across scripts:

- `contains_number(text)`  
  Uses regular expressions to detect numeric content such as years (`\b\d+(\.\d+)?\b`). Applied to both questions and answers.

- `is_non_english(text)`  
  Uses `langid` to detect the language of a string. Returns `True` if not English (`'en'`). Handles short phrases robustly.

- `entity_counter[text]`  
  Built using `spaCy` to count frequency of named entities (`PERSON`, `ORG`, `GPE`) across the full dataset. Used to identify rare entities below a defined threshold.

---
## 📦 Third-Party Libraries Used

This project uses a few carefully selected open-source tools to assist with lightweight NLP processing and iteration:

- [`spaCy`](https://spacy.io)  
  An industrial-strength NLP library used here to perform Named Entity Recognition (NER). It provides a fast and efficient `en_core_web_sm` English model for identifying entity types like `PERSON`, `ORG`, and `GPE`.

- [`langid`](https://github.com/saffsd/langid.py)  
  A compact and offline language identification library. It works well with short texts like Jeopardy questions and does not require external models or internet access.

- [`tqdm`](https://tqdm.github.io)  
  A simple Python library for displaying progress bars during data iteration. Improves script feedback and runtime visibility, especially when processing ~200k entries.

- `re` (Python standard library)  
  Used for pattern-based text filtering (e.g., finding numeric tokens) via regular expressions.

All third-party tools were selected for their speed, interpretability, and low external dependencies.

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

## 🧠 How to Use for Model Comparison

We can use these subsets to compare NER models (e.g., spaCy, BERT, GPT) on challenging inputs:

- Recall and precision per category
- Entity type diversity (e.g., date vs person vs org)
- Mislabeling patterns (e.g., confusing money with ordinal)

Optional `ner-demo` branch runs `spaCy` NER on each subset and prints outputs for qualitative inspection.
