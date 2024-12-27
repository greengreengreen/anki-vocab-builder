# Anki Vocab Builder

A tool to convert Kindle highlights into Anki flashcards using GPT-4.

## Features

- **Easy Import from Kindle**
  - Simply copy your My Clippings.txt file to the input folder
  - Automatically generates appropriate quiz types (fill-in-blank or Q&A)
  - Preserves source context

- **Smart Quiz Generation**
  - Uses GPT-4 to create meaningful questions
  - Generates both vocabulary and concept-based cards
  - Includes relevant quotes and examples

## Quick Start

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Set up your OpenAI API key:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

3. Copy your Kindle's "My Clippings.txt" to the input folder

4. Generate Anki cards:
   ```bash
   python -m anki_vocab_builder
   ```

5. Import the generated deck (output/kindle_highlights.apkg) into Anki

## For Developers

### Project Structure

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