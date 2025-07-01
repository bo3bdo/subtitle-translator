# Subtitle Translator v2.0 - User Guide

## 🌟 What's New in Version 2.0

### ✨ **Major Features Added:**
- **Multi-language UI**: Switch between English and Arabic interface
- **Smart Caching**: Avoid re-translating the same text
- **Automatic Backups**: Protect your original files
- **Advanced Settings**: Customizable preferences with persistent storage
- **Multiple Translation Engines**: Google Translate and Microsoft Translator
- **Session Statistics**: Track your translation progress
- **Console-Safe Interface**: Works properly in all terminals

### 🔧 **Technical Improvements:**
- Object-oriented architecture with clean separation
- SQLite-based caching system
- JSON configuration management
- Better error handling and recovery
- Progress tracking with real-time updates

## 🚀 Quick Start (Version 2.0)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the program:**
   ```bash
   python translate_subtitles.py
   ```

3. **Choose your preference:**
   - Interface will start in English by default
   - You can change to Arabic in Settings > Change UI Language
   - Select option 1 to translate a specific file

## 📋 Menu Options Explained

### Main Menu:
1. **Translate specific file** - Translate a single SRT file
2. **Translate all SRT files in current directory** - Batch process all SRT files
3. **Search in another directory** - Process files from a different folder
4. **Translator settings** - Configure the application
5. **Show statistics** - View session and cache statistics
6. **Help** - Display help information
7. **Exit** - Close the application

### Settings Menu:
1. **Show current settings** - Display all current configurations
2. **Change target language** - Switch between Arabic, English, French, etc.
3. **Change translation engine** - Switch between Google and Microsoft
4. **Manage cache** - View and manage translation cache
5. **Change UI language** - Switch between English and Arabic interface
6. **Reset to defaults** - Restore original settings
7. **Back to main menu** - Return to main menu

## 💾 Cache Management

The new caching system saves translations to avoid repeating work:

- **Automatic**: Translations are cached automatically
- **Persistent**: Cache survives program restarts
- **Statistics**: View cache hit rates and storage usage
- **Cleanup**: Remove old or unused translations
- **Manual Control**: Clear cache when needed

## ⚙️ Configuration Options

All settings are stored in `config.json`:

```json
{
    "default_target_language": "ar",
    "default_source_language": "en",
    "translation_engine": "google",
    "ui_language": "en",
    "cache_enabled": true,
    "create_backup": true,
    "max_retries": 3,
    "delay_between_requests": 0.1
}
```

## 🛡️ Safety Features

### Automatic Backups:
- Original files are backed up before translation
- Backups stored in `/backups` folder
- Timestamped for easy identification

### File Validation:
- SRT format verification before processing
- Encoding detection and handling
- Error recovery and fallback options

## 🌍 Language Support

### Interface Languages:
- **English** (Recommended for all consoles)
- **Arabic** (May not display correctly in some terminals)

### Translation Languages:
- Arabic (ar)
- English (en)
- French (fr)
- Spanish (es)
- German (de)
- Italian (it)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

## 📊 Statistics and Monitoring

View detailed information about your translation sessions:
- Files processed
- Total translations completed
- Cache hit rate
- Translation errors
- Session duration
- Database size

## 🔧 Command Line Usage

```bash
# Interactive mode (default)
python translate_subtitles.py

# Translate specific file
python translate_subtitles.py movie.srt

# Translate with custom output
python translate_subtitles.py movie.srt -o movie_french.srt -l fr

# Translate all files in directory
python translate_subtitles.py -a

# Force interactive mode
python translate_subtitles.py -i
```

## 🐛 Troubleshooting

### Common Issues:

**Arabic text displays incorrectly:**
- Switch to English interface: Settings > Change UI Language > English
- This is a console limitation, not a program bug

**Translation fails:**
- Check internet connection
- Try switching translation engines
- Review error messages in the output

**Cache issues:**
- Clear cache: Settings > Manage Cache > Clear all translations
- Disable cache temporarily in settings

**File not found:**
- Use absolute file paths
- Ensure file has .srt extension
- Check file permissions

## 📞 Support

- **GitHub**: [Your Repository URL]
- **Issues**: Report bugs and request features
- **Documentation**: Full API documentation available

## 🔄 Version History

### v2.0.0 (Current)
- Multi-language interface support
- Smart caching system
- Automatic backups
- Advanced settings management
- Multiple translation engines
- Session statistics
- Console compatibility improvements

### v1.0.0 (Previous)
- Basic SRT translation
- Simple interactive mode
- Google Translate integration

---

**Happy Translating! 🎬✨**
