# Anki Vocab Builder

An automated tool to build your vocabulary with Anki flashcards. Easily collect words from any source (Kindle, web browsing, reading apps) and automatically generate comprehensive Anki cards with definitions, pronunciations, and example sentences.

## Features

- **Easy Word Collection**
  - Collect words with a simple keyboard shortcut (Ctrl+Shift+A)
  - Works with any text you can highlight
  - System tray app for convenient access

- **Rich Anki Cards**
  - Definitions from reliable dictionary sources
  - Audio pronunciations
  - Example sentences
  - Source context preservation

## Quick Start for Users

### Installation

1. Ensure you have Python 3.8+ installed
2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/vocab-builder.git
   cd vocab-builder
   ```

3. Set up virtual environment and install dependencies:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

### Usage

1. Start the word collector:
   ```bash
   python scripts/collect_words.py
   ```
   - Look for the app icon in your system tray
   - Highlight any word and press Ctrl+Shift+A to save it

2. Generate Anki cards:
   ```bash
   python scripts/generate_cards.py
   ```
   - Find the generated Anki deck at `output/vocabulary.apkg`
   - Import the deck into Anki

## For Developers

### Project Structure

```
vocab-builder/
├── vocab_builder/           # Main package
│   ├── collectors/         # Word collection implementations
│   ├── storage/           # Data storage handling
│   ├── enrichment/        # Word data enrichment (definitions, audio)
│   └── anki/              # Anki card generation
├── tests/                  # Test suite
├── scripts/               # CLI scripts
└── output/                # Generated files
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

- [ ] Kindle highlights integration
- [ ] iOS reading app integration
- [ ] Image support for cards
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