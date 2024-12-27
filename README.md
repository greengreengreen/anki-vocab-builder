# Anki Vocab Builder

> Transform your Kindle highlights into beautiful, AI-powered Anki flashcards

## ✨ Features

### 🎯 Smart Card Generation
- **Two Card Types:**
  - 📝 Fill-in-blank for vocabulary mastery
  - 🤔 Q&A for deeper concept understanding
- **Modern Design:**
  - Responsive layout
  - Clean typography
  - Consistent color scheme

### 📱 Kindle Integration
- Direct import from "My Clippings.txt"
- Preserves book context and citations
- Smart batch processing with caching

### 🧠 Enhanced Learning
- **Vocabulary Cards Include:**
  - Contextual examples
  - Word families
  - Synonyms & antonyms
  - Clear definitions
- **Concept Cards Include:**
  - Related concepts
  - Key term definitions
  - Supporting quotes

## 🚀 Quick Start

1. **Install Poetry:**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone & Setup:**
   ```bash
   git clone https://github.com/yourusername/anki-vocab-builder.git
   cd anki-vocab-builder
   poetry install
   ```

3. **Set Environment:**
   ```bash
   poetry shell
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. **Import Kindle Highlights:**
   ```bash
   mkdir -p .anki_vocab_builder/input/kindle
   cp /path/to/My\ Clippings.txt .anki_vocab_builder/input/kindle/
   ```

5. **Generate Cards:**
   ```bash
   python -m anki_vocab_builder
   ```

6. **Import into Anki** - Find your deck at `output/kindle_highlights.apkg`

## 🎨 Card Types

### Type-In Cards (Vocabulary Focus)
<p align="center">
  <img src="docs/assets/type-in-card.png" alt="Type-In Card Example" width="400">
</p>

- Front shows context with blank word
- Back includes:
  - Typing feedback
  - Word definition & usage
  - Synonyms & antonyms
  - Complete word family

### Q&A Cards (Concept Focus)
<p align="center">
  <img src="docs/assets/qa-card.png" alt="Q&A Card Example" width="400">
</p>

- Front shows conceptual question
- Back includes:
  - Concise answer
  - Supporting quotes
  - Related concepts
  - Additional context

## 🗺️ Roadmap

- [x] Kindle highlights integration
- [x] Modern card design
- [x] GPT-4 powered generation
- [ ] Deduplication support
- [ ] Clipboard integration
- [ ] Audio pronunciation

---

<p align="center">
  Made with ❤️ for lifelong learners
</p>
