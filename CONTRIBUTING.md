# Contributing to Advanced Subtitle Translator

Thank you for your interest in contributing to the Advanced Subtitle Translator! This document provides guidelines and information for contributors.

## 🌟 How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title**: Descriptive summary of the issue
- **Environment details**: OS, Python version, application version
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Screenshots**: If applicable, add screenshots to help explain
- **Log files**: Include relevant error messages or log outputs

#### Bug Report Template

```markdown
**Bug Summary**
Brief description of the bug

**Environment**
- OS: [Windows 10/11, macOS, Linux]
- Python Version: [3.7, 3.8, 3.9, etc.]
- App Version: [2.1.0]

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Screenshots**
Add screenshots if helpful

**Additional Context**
Any other relevant information
```

### ✨ Suggesting Features

Feature suggestions are welcome! Please:

- **Check existing requests**: Look through open issues for similar requests
- **Provide context**: Explain why this feature would be useful
- **Be specific**: Clear description of the proposed functionality
- **Consider scope**: Ensure the feature aligns with project goals

#### Feature Request Template

```markdown
**Feature Summary**
Brief description of the feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Any alternative solutions you've considered

**Additional Context**
Screenshots, mockups, or other relevant information
```

### 🔧 Code Contributions

#### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/advanced-subtitle-translator.git
   cd advanced-subtitle-translator
   ```

2. **Create development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number
   ```

#### Code Guidelines

**Python Style**
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints where appropriate

**Documentation**
- Write docstrings for all functions and classes
- Use Google-style docstrings
- Update relevant documentation files
- Include inline comments for complex logic

**Testing**
- Write tests for new functionality
- Ensure existing tests pass
- Aim for >80% test coverage
- Test GUI components where possible

#### Example Code Style

```python
def translate_subtitle_file(
    input_file: str,
    target_language: str,
    output_file: Optional[str] = None
) -> bool:
    """
    Translate a subtitle file to the target language.
    
    Args:
        input_file: Path to the input subtitle file
        target_language: Target language code (e.g., 'ar', 'fr')
        output_file: Optional output file path. If None, auto-generate
        
    Returns:
        True if translation successful, False otherwise
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        TranslationError: If translation service fails
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Implementation here
    return True
```

#### Commit Guidelines

**Commit Message Format**
```
type(scope): brief description

Longer description if needed

Fixes #issue-number
```

**Types**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**
```bash
feat(gui): add drag and drop support for subtitle files

- Implemented drag and drop area in main interface
- Added visual feedback for file drop operations
- Updated file handling to support multiple formats

Fixes #123
```

```bash
fix(translation): resolve thread safety issue in batch processing

- Fixed race condition in translation worker threads
- Added proper synchronization for shared resources
- Improved error handling for concurrent operations

Fixes #456
```

#### Pull Request Process

1. **Update documentation**: Ensure README, docstrings, and guides are updated
2. **Add tests**: Include tests for new functionality
3. **Run tests**: Ensure all tests pass locally
4. **Update changelog**: Add entry to CHANGELOG.md
5. **Create pull request**: Use the PR template below

#### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Screenshots
Include screenshots for UI changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Documentation updated
- [ ] Changes generate no new warnings
```

### 📝 Documentation Contributions

Documentation improvements are always welcome:

- **User guides**: Improve existing guides or create new ones
- **Code documentation**: Add or improve docstrings and comments
- **README updates**: Keep the README current and helpful
- **Translation**: Help translate documentation to other languages

### 🎨 Design Contributions

Help improve the user interface and experience:

- **UI mockups**: Create mockups for new features
- **Icon design**: Design icons for the application
- **UX improvements**: Suggest interface improvements
- **Accessibility**: Help make the app more accessible

## 🚀 Development Guidelines

### Architecture Overview

```
advanced-subtitle-translator/
├── gui_translator.py          # Main GUI application
├── translate_subtitles.py     # Core translation engine
├── config.py                  # Configuration management
├── subtitle_formats.py        # Format handlers (SRT/ASS/VTT)
├── language_detector.py       # Language detection
├── cache.py                  # Translation caching
├── tests/                    # Test files
├── docs/                     # Documentation
└── requirements.txt          # Dependencies
```

### Key Components

**GUI Layer** (`gui_translator.py`)
- Main application interface
- Event handling and user interaction
- Progress tracking and status updates

**Translation Engine** (`translate_subtitles.py`)
- Core translation logic
- API integration with translation services
- Error handling and retry logic

**Format Handlers** (`subtitle_formats.py`)
- Parsing and writing subtitle formats
- Format detection and validation
- Cross-format conversion

**Caching System** (`cache.py`)
- SQLite-based translation cache
- Cache management and optimization
- Performance analytics

### Testing Guidelines

**Unit Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_translation.py

# Run with coverage
python -m pytest --cov=. tests/
```

**GUI Testing**
```bash
# Run GUI tests
python test_gui.py

# Manual testing checklist
python -m pytest tests/test_gui_manual.py
```

**Integration Tests**
```bash
# Test full translation workflow
python test_program.py
```

### Performance Guidelines

**Memory Usage**
- Minimize memory footprint for large files
- Use generators for processing large datasets
- Implement proper cleanup for resources

**Speed Optimization**
- Cache frequently accessed data
- Use efficient algorithms and data structures
- Profile code to identify bottlenecks

**Network Efficiency**
- Implement proper rate limiting
- Use connection pooling where appropriate
- Handle network errors gracefully

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful**: Treat all contributors with respect
- **Be inclusive**: Welcome contributors from all backgrounds
- **Be collaborative**: Work together to improve the project
- **Be constructive**: Provide helpful feedback and suggestions

### Communication

**GitHub Issues**
- Use for bug reports and feature requests
- Provide clear, detailed information
- Follow issue templates when available

**Discussions**
- Use GitHub Discussions for questions and ideas
- Help other community members
- Share your experiences and use cases

**Pull Request Reviews**
- Be constructive in code reviews
- Ask questions to understand changes
- Suggest improvements when appropriate
- Approve when changes meet standards

## 🏆 Recognition

### Contributors

We recognize contributors in several ways:

- **README mentions**: Active contributors listed in README
- **Release notes**: Major contributions highlighted in releases
- **GitHub profile**: Contributions visible on your GitHub profile
- **Community recognition**: Thanks in discussions and issues

### Contribution Types

All types of contributions are valued:

- 💻 **Code contributions**: Features, bug fixes, improvements
- 📖 **Documentation**: Guides, tutorials, API docs
- 🐛 **Testing**: Bug reports, test cases, quality assurance
- 🎨 **Design**: UI/UX improvements, icons, mockups
- 🌍 **Translation**: Interface and documentation translation
- 💡 **Ideas**: Feature suggestions and feedback

## 📚 Resources

### Development Tools

**Recommended IDE Setup**
- **VS Code**: With Python extension
- **PyCharm**: Professional Python IDE
- **Vim/Neovim**: For terminal-based development

**Useful Extensions/Plugins**
- Python language support
- Git integration
- Linting and formatting tools
- Testing frameworks

### Learning Resources

**Python Development**
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [Python PEP 8 Style Guide](https://pep8.org/)

**GUI Development**
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Tkinter Tutorial](https://tkdocs.com/)

**Testing**
- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing 101](https://realpython.com/python-testing/)

## 📞 Getting Help

### Support Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and community support
- **Documentation**: Check existing docs first
- **Code Comments**: Look at inline documentation

### Response Times

- **Issues**: Response within 2-3 days
- **Pull Requests**: Initial review within 1 week
- **Discussions**: Community-driven, varies

## 🎉 Thank You!

Thank you for contributing to the Advanced Subtitle Translator! Your efforts help make this tool better for everyone. Whether you're fixing a typo, adding a feature, or helping other users, every contribution matters.

---

**Happy Contributing! 🚀**
