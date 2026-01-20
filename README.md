# Italian Verb Study Organizer

A Python NLP tool that analyzes Italian text files to extract verbs, rank by frequency, and generate optimized study schedules.

## Motivation
Built this to solve a personal problem: I wanted to learn Italian verbs from authentic texts, but manually extracting and organizing them was tedious. This tool automates the entire workflow.

## Features
- **Automatic verb extraction** using spaCy NLP and lemmatization
- **Frequency-based ranking** - study the most common verbs first
- **Smart categorization** - separates -are, -ere, -ire, and irregular verbs
- **Balanced study plans** - distributes verbs across multiple days (3 regular + 1 irregular per day)
- **Full conjugation tables** - supports 8 tenses across 3 moods (Indicativo, Congiuntivo, Condizionale)
- **Rich terminal UI** - color-coded output with frequency counts
- **Works with any Italian text** - just pass a .txt file as argument

## Demo Results
Processed the *Gospel of Giovanni* (18,000+ words):
- Extracted **434 unique verbs**
- Organized into **82 balanced study days**
- Ranked by frequency (top verb appeared 646 times)

## Installation
```bash
# Clone the repository
git clone https://github.com/danjack0/Verb-And-Conjugation-Project.git
cd Verb-And-Conjugation-Project

# Install dependencies
pip install -r requirements.txt

# Download Italian language model
python -m spacy download it_core_news_md
```

## Usage
```bash
# Run with your own Italian text file
python main.py your_text.txt

# Or run with default sample text
python main.py
```

The program will:
1. Analyze the text and extract all verbs
2. Show a frequency table of top verbs
3. Prompt you to select which tenses to study
4. Display conjugations organized by study day

## Tech Stack
- **Python 3.x**
- **spaCy** - Natural language processing and part-of-speech tagging
- **mlconjug3** - Italian verb conjugation engine
- **Rich** - Terminal formatting and tables

## Screenshots
*Coming soon - terminal output examples*

## Future Enhancements
- [ ] Export to Anki flashcard format
- [ ] Progress tracking with SQLite database
- [ ] Web interface using Streamlit
- [ ] Support for Spanish, French, Portuguese
- [ ] Spaced repetition algorithm

## License
MIT License - feel free to use and modify!
