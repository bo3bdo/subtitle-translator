# Subtitle Translator

A Python tool for translating SRT subtitle files from English to Arabic using Google Translate.

## Features

- ✅ Translate single SRT files
- ✅ Batch translate multiple SRT files in a directory
- ✅ Interactive mode for easy file selection
- ✅ Command-line interface support
- ✅ Automatic detection of SRT files
- ✅ Progress tracking during translation
- ✅ Error handling and recovery
- ✅ UTF-8 encoding support

## Requirements

- Python 3.6 or higher
- `deep_translator` library

## Quick Start

1. **Download/Clone** this repository
2. **Install Python 3.6+** if not already installed
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run the tool**: `python translate_subtitles.py`
5. **Select option 1** and enter your SRT file path
6. **Wait for translation** to complete
7. **Find your translated file** with `_arabic.srt` suffix

## Installation

1. Clone this repository:
```bash
git clone https://github.com/bo3bdo/subtitle-translator.git
cd subtitle-translator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install deep-translator>=1.11.4
```

## Usage

### Interactive Mode (Recommended)

Simply run the script without any arguments to enter interactive mode:

```bash
python translate_subtitles.py
```

This will present you with a menu:
```
Movie Subtitle Arabic Translator
==================================================

Choose one of the following options:
1. Translate specific file
2. Translate all SRT files in current directory
3. Search in another directory
4. Exit

Enter your choice [1-4]:
```

### Command Line Usage

#### Translate a specific file:
```bash
python translate_subtitles.py input_file.srt
```

#### Translate with custom output file:
```bash
python translate_subtitles.py input_file.srt -o output_file.srt
```

#### Translate all SRT files in current directory:
```bash
python translate_subtitles.py -a
```

#### Force interactive mode:
```bash
python translate_subtitles.py -i
```

#### Translate to a different language:
```bash
python translate_subtitles.py input_file.srt -l fr  # French
python translate_subtitles.py input_file.srt -l es  # Spanish
```

### Command Line Options

- `input_file`: Path to the input SRT file (optional)
- `-o, --output`: Output file path (optional, defaults to `input_file_arabic.srt`)
- `-l, --lang`: Target language code (default: `ar` for Arabic)
- `-i, --interactive`: Force interactive mode
- `-a, --all`: Translate all SRT files in current directory
- `-h, --help`: Show help message

## Arabic Language Support

This tool is specifically optimized for Arabic translation with the following features:

### RTL (Right-to-Left) Support
- Full Unicode support for Arabic characters
- Proper handling of Arabic diacritics and special characters
- UTF-8 encoding ensures compatibility with all media players

### Translation Quality
- Uses Google Translate's Arabic engine for high-quality translations
- Preserves context within subtitle timing constraints
- Handles both formal and colloquial English-to-Arabic translation

### Media Player Compatibility
The generated Arabic SRT files work with:
- VLC Media Player
- MPC-HC (Media Player Classic)
- PotPlayer
- Kodi/XBMC
- Most modern video players with subtitle support

## Supported Languages

The tool uses Google Translate, so it supports all languages that Google Translate supports. Common language codes:

- `ar` - Arabic
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

## File Structure

```
subtitle-translator/
├── translate_subtitles.py    # Main script with SubtitleTranslator class
├── README.md                 # This documentation file
├── requirements.txt          # Python dependencies (deep-translator>=1.11.4)
├── test_movie.srt           # Example SRT file for testing
└── examples/                 # Additional example SRT files (optional)
```

## Example

### Sample Translation Session
```
Movie Subtitle Arabic Translator
==================================================

Choose one of the following options:
1. Translate specific file
2. Translate all SRT files in current directory
3. Search in another directory
4. Exit

Enter your choice [1-4]: 1
Enter file path: test_movie.srt
Reading subtitle file: test_movie.srt
Found 2 subtitle entries
Translating 2 subtitle entries...
Progress: 2/2 (100.0%)
Translation completed!
Translated subtitles saved to: test_movie_arabic.srt
```

### Input file (movie.srt):
```
1
00:00:01,000 --> 00:00:04,000
Hello, how are you today?

2
00:00:05,000 --> 00:00:08,000
I'm doing great, thank you!
```

### Output file (movie_arabic.srt):
```
1
00:00:01,000 --> 00:00:04,000
مرحبا، كيف حالك اليوم؟

2
00:00:05,000 --> 00:00:08,000
أنا بخير، شكرا لك!
```

## Features Explanation

### Automatic File Detection
The tool automatically finds all `.srt` files in the specified directory and excludes already translated files (those ending with `_arabic.srt`).

### Progress Tracking
During translation, you'll see real-time progress:
```
Translating 150 subtitle entries...
Progress: 45/150 (30.0%)
```

### Error Handling
- Network connection issues are handled gracefully
- Invalid SRT format files are skipped
- Translation errors fallback to original text

### Rate Limiting
The tool includes a small delay between translations to respect Google Translate's rate limits and avoid being blocked.

## Technical Details

### Architecture
The tool is built using object-oriented programming with a main `SubtitleTranslator` class that handles:
- File parsing and validation
- Translation using Google Translate API
- Progress tracking and error handling
- Output file generation

### SRT File Parsing
The tool properly parses SRT files by:
1. Splitting content by double newlines to separate subtitle blocks
2. Using regex to extract subtitle number, timestamp, and text
3. Handling multi-line subtitle text correctly
4. Preserving original formatting and timing

### Translation Process
1. Each subtitle entry is translated individually using deep-translator
2. Empty lines and special characters (-, --, ...) are preserved as-is
3. Network errors are caught and handled gracefully
4. Original text is kept if translation fails
5. Progress is displayed in real-time during translation

### Error Handling & Rate Limiting
- Built-in retry mechanism for failed translations
- 0.1-second delay between translations to respect API limits
- Comprehensive error logging with helpful messages
- Graceful fallback to original text when translation fails

## Troubleshooting

### Common Issues

**"No SRT files found"**
- Make sure you're in the correct directory
- Check that your files have the `.srt` extension
- Ensure files are not already translated (`_arabic.srt`)

**Translation errors**
- Check your internet connection
- The tool will retry failed translations automatically
- Original text is preserved if translation fails

**Encoding issues**
- All files are handled with UTF-8 encoding
- Make sure your SRT files are properly encoded
- Arabic text is fully supported

**Rate limiting**
- If you get rate limited, wait a few minutes and try again
- The tool includes 0.1 second delays between translations to minimize this issue
- For large files, consider translating in smaller batches

**File path issues**
- Use absolute paths when possible
- Enclose paths with spaces in quotes
- Ensure file has `.srt` extension

## Advanced Usage

### Custom Language Translation
The tool supports translation to any language supported by Google Translate:

```bash
# Translate to French
python translate_subtitles.py movie.srt -l fr

# Translate to Spanish  
python translate_subtitles.py movie.srt -l es

# Translate to German
python translate_subtitles.py movie.srt -l de
```

### Batch Processing
For processing multiple files efficiently:

```bash
# Process all SRT files in current directory
python translate_subtitles.py -a

# Or use interactive mode for more control
python translate_subtitles.py -i
```

## Tips for Better Results

### Subtitle Quality
- Ensure your source SRT files are properly formatted
- Clean up any encoding issues before translation
- Remove excessive formatting or special characters that might interfere

### Translation Accuracy
- The tool works best with properly punctuated English subtitles
- Long subtitle lines may be split during translation
- Review translated content for context-specific terms

### Performance Optimization
- For large files (>1000 subtitles), translation may take several minutes
- Stable internet connection is required for best results
- Close other applications using internet bandwidth during translation

### File Management
- Translated files are automatically named with `_arabic.srt` suffix
- Original files are never modified or overwritten
- Keep backups of important subtitle files

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool uses Google Translate for translations. Translation quality depends on Google's service. For professional subtitles, manual review and editing of translated content is recommended.

## Changelog

### v1.0.0 (Current)
- ✅ Initial release with complete functionality
- ✅ Object-oriented architecture with SubtitleTranslator class
- ✅ Interactive menu system for easy file selection
- ✅ Command line interface with multiple options
- ✅ Batch translation support for entire directories
- ✅ Real-time progress tracking during translation
- ✅ Comprehensive error handling and recovery
- ✅ UTF-8 encoding support for Arabic text
- ✅ Automatic output file naming with `_arabic.srt` suffix
- ✅ Rate limiting to prevent API blocking
- ✅ Support for all Google Translate languages

## Frequently Asked Questions (FAQ)

**Q: Can I translate to languages other than Arabic?**
A: Yes! Use the `-l` parameter with any language code (e.g., `-l fr` for French, `-l es` for Spanish).

**Q: Will this work with burned-in subtitles?**
A: No, this tool only works with separate SRT subtitle files, not embedded/burned-in subtitles.

**Q: How accurate are the translations?**
A: Translation quality depends on Google Translate. For professional use, manual review is recommended.

**Q: Can I translate from languages other than English?**
A: Currently optimized for English-to-Arabic, but you can modify the source language in the code.

**Q: What if my internet connection is slow?**
A: The tool includes timeouts and retry mechanisms, but stable internet is recommended for best results.

**Q: Are there any file size limits?**
A: No specific limits, but very large files (1000+ subtitles) will take longer to process.

## Author

Created with ❤️ for the subtitle translation community.

## Support

If you find this tool helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting issues
- 💡 Suggesting new features
- 🤝 Contributing to the code

---

**Happy translating! 🎬📝**
