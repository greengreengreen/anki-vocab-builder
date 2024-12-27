# Anki Vocab Builder

A tool to convert Kindle highlights into Anki flashcards using GPT-4, with beautiful modern card designs.

## Features

- **Smart Card Generation**
  - Automatically creates two types of cards:
    - Fill-in-blank for vocabulary learning
    - Q&A for concept understanding
  - Beautiful modern card design with responsive layout
  - Consistent typography and color scheme

- **Kindle Integration**
  - Direct import from Kindle's "My Clippings.txt"
  - Preserves book context and citations
  - Batch processing with caching support

- **Enhanced Learning Content**
  - Vocabulary cards include:
    - Contextual examples
    - Word families
    - Synonyms and antonyms
    - Clear definitions
  - Concept cards include:
    - Related concepts
    - Key terms with definitions
    - Supporting quotes from source

## Quick Start

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. Copy your Kindle's "My Clippings.txt" to the input folder:
   ```bash
   mkdir -p .anki_vocab_builder/input/kindle
   cp /path/to/My\ Clippings.txt .anki_vocab_builder/input/kindle/
   ```

4. Generate Anki cards:
   ```bash
   python -m anki_vocab_builder
   ```

5. Import the generated deck (output/kindle_highlights.apkg) into Anki

## Card Types

### Type-In Cards (Vocabulary Focus)
- Front shows context with blank word
- Back includes:
  - Correct answer with typing feedback
  - Word definition and usage examples
  - Synonyms and antonyms
  - Complete word family

### Q&A Cards (Concept Focus)
- Front shows conceptual question
- Back includes:
  - Concise answer
  - Supporting quotes from source
  - Related key terms and concepts
  - Additional context

## Project Structure

```
anki_vocab_builder/
├── anki_vocab_builder/      # Main package
│   ├── card_generator/     # Anki card generation
│   ├── enrichment/        # OpenAI integration
│   ├── parsers/          # Kindle highlights parsing
│   └── storage/          # Quiz models
├── tests/                # Test suite
└── input/               # Place for My Clippings.txt
```

### Development Setup

1. Clone and set up development environment:
   ```bash
   git clone https://github.com/yourusername/vocab-builder.git
   cd vocab-builder
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

3. Format code:
   ```bash
   black vocab_builder/
   ```

### Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Use type hints in Python code
- Handle errors gracefully

## Core Components

### Word Collector
- Runs in system tray
- Monitors clipboard
- Saves words to CSV storage
- Preserves original context

### Card Generator
- Processes collected words
- Fetches definitions and examples
- Generates audio pronunciations
- Creates Anki cards

## Roadmap

- [x] Kindle highlights integration
- [x] Modern card design with responsive layout
- [x] GPT-4 powered quiz generation
- [ ] iOS reading app integration
- [ ] Audio pronunciation support
- [ ] Custom dictionary sources
- [ ] GUI for word management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Free Dictionary API for definitions
- Anki for spaced repetition
- gTTS for audio generation

## Troubleshooting

### Common Issues

1. System tray icon not appearing
   - Check if your system supports system tray icons
   - Try running with administrator privileges

2. Keyboard shortcut not working
   - Verify no other app is using Ctrl+Shift+A
   - Check keyboard permissions on your OS

3. Anki card generation failing
   - Verify internet connection for API calls
   - Check if Anki is closed while importing

For more issues, please check the [Issues](https://github.com/yourusername/vocab-builder/issues) page.

## Support

- Open an issue for bugs or feature requests
- Check existing issues before opening new ones
- Provide detailed information when reporting bugs

---