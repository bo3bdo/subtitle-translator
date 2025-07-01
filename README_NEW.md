# Advanced Subtitle Translator 🎬✨

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![Translation](https://img.shields.io/badge/Translation-Multi--Engine-purple.svg)](https://pypi.org/project/deep-translator/)

## 🚀 Overview

**Advanced Subtitle Translator** is a powerful, user-friendly desktop application for translating subtitle files with support for multiple formats (SRT, ASS, VTT) and languages. Features a modern GUI, intelligent caching, batch processing, and automatic language detection.

## 📸 Screenshots

### Main Interface - Translation in Progress
![Advanced Subtitle Translator GUI](docs/screenshots/main-interface.png)

*The modern GUI interface showing a translation in progress with all features visible: file selection, language detection, format options, and real-time progress tracking.*

### Key Interface Features Shown:
- **File Selection**: Easy browse and auto-generate output file names
- **Language Detection**: Auto-detect source language with "Auto-detected: en" 
- **Format Support**: SRT input with customizable output format (.srt, .ass, .vtt)
- **Translation Options**: Google Translate engine with backup and cache options
- **Progress Tracking**: Real-time progress bar showing "Translating subtitle 255/1887..."
- **Action Buttons**: Start/Stop translation, Preview, and Open Output Folder
- **Drag & Drop Area**: Intuitive file handling with visual feedback
- **Tabbed Interface**: Single File, Batch Process, Settings, and Statistics tabs

### ✨ Key Features

- 🖱️ **Drag & Drop Interface** - Simply drag subtitle files to translate
- 🌍 **Auto Language Detection** - Smart detection of source language
- 📁 **Batch Processing** - Translate multiple files simultaneously
- 💾 **Intelligent Caching** - Reduces API calls and improves speed
- 🎨 **Modern GUI** - Clean, professional interface with real-time progress
- 📊 **Multiple Formats** - Support for SRT, ASS, and VTT subtitle formats
- 🔧 **Customizable Settings** - Flexible configuration options
- 📈 **Statistics & Analytics** - Track translation performance

## 🎯 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/advanced-subtitle-translator.git
cd advanced-subtitle-translator

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_gui.py
```

### Basic Usage

1. **Launch the application**: Run `python run_gui.py`
2. **Load a subtitle file**: Drag & drop or use the Browse button
3. **Select target language**: Choose your desired translation language
4. **Start translation**: Click "🚀 Start Translation"
5. **View results**: Translated file is automatically saved

## 🔧 Features In Detail

### 🎬 Subtitle Format Support

| Format | Read | Write | Features |
|--------|------|-------|----------|
| **SRT** | ✅ | ✅ | Standard SubRip format |
| **ASS** | ✅ | ✅ | Advanced SubStation Alpha with styling |
| **VTT** | ✅ | ✅ | WebVTT for web videos |

### 🌍 Language Support

**Auto-Detection**: Automatically detects source language from content

**Supported Languages**: Arabic, English, French, Spanish, German, Italian, Russian, Japanese, Korean, Chinese, Portuguese, Dutch, Swedish, Turkish

### 🚀 Translation Engines

- **Google Translate** - High quality, fast translation
- **Microsoft Translator** - Alternative translation service
- **Configurable Delays** - Respect API rate limits
- **Retry Logic** - Automatic retry on failures

### 💾 Intelligent Caching

- **SQLite Database** - Persistent translation cache
- **Duplicate Detection** - Avoid re-translating identical text
- **Cache Management** - View and clear cache statistics
- **Performance Boost** - 70-90% cache hit rate

## 📚 Documentation

### User Guides
- [GUI User Guide](GUI_USER_GUIDE.md) - Complete GUI documentation
- [Command Line Guide](USER_GUIDE_v2.md) - Advanced usage and CLI options

## �️ Feature Gallery

### Interface Overview
<div align="center">

| Feature | Screenshot | Description |
|---------|------------|-------------|
| **Main Interface** | ![Main GUI](docs/screenshots/main-interface.png) | Complete translation interface with all controls |
| **Batch Processing** | ![Batch](docs/screenshots/batch-processing.png) | Process multiple subtitle files simultaneously |
| **Settings Panel** | ![Settings](docs/screenshots/settings-panel.png) | Comprehensive configuration options |
| **Statistics View** | ![Stats](docs/screenshots/statistics-view.png) | Performance analytics and cache statistics |

</div>

### Key Features in Action

#### 🎯 Translation Process
The main interface shows a real translation in progress:
- **File**: Movie subtitle file (1,887 subtitles)
- **Progress**: Currently translating subtitle 255/1,887
- **Languages**: Auto-detected English → Arabic
- **Engine**: Google Translate with caching enabled
- **Format**: SRT format with backup creation

#### 🔧 Professional Features
- **Smart File Handling**: Auto-generate output names with customizable suffixes
- **Visual Progress**: Real-time progress bars and status updates  
- **Format Flexibility**: Support for SRT, ASS, and VTT formats
- **Quality Options**: Backup creation and intelligent caching
- **User Experience**: Clean, intuitive interface with drag & drop support

## �🛠️ Advanced Usage

### Batch Processing

```python
# Add files to batch
app.add_file_to_batch("movie1.srt")
app.add_file_to_batch("movie2.ass")
app.add_directory_to_batch("/path/to/subtitles/")

# Start batch translation
app.start_batch_translation()
```

### Custom Configuration

```json
{
  "translation_engine": "google",
  "default_source_language": "en",
  "default_target_language": "ar",
  "cache_enabled": true,
  "create_backup": true,
  "output_suffix": "_translated"
}
```

### Command Line Usage

```bash
# Single file translation
python translate_subtitles.py input.srt --target ar --output output.srt

# Batch translation
python translate_subtitles.py --batch /path/to/files/ --target ar

# With custom engine
python translate_subtitles.py input.srt --engine microsoft --target fr
```

## 📊 Performance

### Benchmarks

| Metric | Performance |
|--------|-------------|
| **Startup Time** | < 2 seconds |
| **Translation Speed** | 1-2 seconds per subtitle |
| **Memory Usage** | < 50MB |
| **Cache Hit Rate** | 70-90% |
| **Max File Size** | 10MB+ |

### System Requirements

- **Python**: 3.7 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 50MB free space
- **Network**: Internet connection for translation APIs
- **OS**: Windows, macOS, Linux

## 🔧 Configuration Options

### Translation Settings
- Default source/target languages
- Translation engine selection
- Request delays and retry limits
- Cache management options

### UI Settings
- Interface language (English/Arabic)
- Theme and appearance
- Progress display options
- File naming conventions

### Performance Settings
- Cache size limits
- Concurrent translation limits
- Network timeout settings
- Backup file management

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python test_program.py

# Run GUI tests
python test_gui.py

# Run specific module tests
python -m pytest tests/
```

### Test Coverage

- Unit tests for all core modules
- GUI interaction testing
- Translation engine testing
- Format handler testing
- Cache system testing

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/yourusername/advanced-subtitle-translator.git
cd advanced-subtitle-translator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run in development mode
python gui_translator.py
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Write comprehensive docstrings
- Maintain test coverage above 80%

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Deep-translator** library for translation API integration
- **Python tkinter** community for GUI framework
- **SQLite** for reliable data storage
- All contributors and beta testers

## 📞 Support & Community

### Getting Help
- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/advanced-subtitle-translator/issues)
- 💬 [Discussions](https://github.com/yourusername/advanced-subtitle-translator/discussions)

### Community
- ⭐ Star this repository if you find it useful
- 🍴 Fork and create your own improvements
- 📢 Share with friends and colleagues
- 🐛 Report bugs and suggest features

---

## 📈 Roadmap

### Upcoming Features (v2.2)
- [ ] **Real-time Translation** - Live translation preview
- [ ] **Cloud Sync** - Sync settings across devices
- [ ] **Plugin System** - Custom translation engines
- [ ] **Mobile App** - Android/iOS companion app

### Future Enhancements
- [ ] **AI-powered Translation** - Integration with GPT models
- [ ] **Voice Recognition** - Audio-to-subtitle conversion
- [ ] **Collaborative Translation** - Team translation features
- [ ] **Quality Metrics** - Translation quality scoring

---

<div align="center">

**Made with ❤️ by the Advanced Subtitle Translator Team**

[⬆ Back to Top](#advanced-subtitle-translator-)

</div>
