#!/usr/bin/env python3
"""
Version information for Advanced Subtitle Translator
"""

__version__ = '2.2.2'
__title__ = 'Advanced Subtitle Translator'
__description__ = 'Advanced GUI application for translating subtitle files'
__author__ = 'Advanced Subtitle Translator Team'
__author_email__ = 'contact@subtitle-translator.dev'
__license__ = 'MIT'
__copyright__ = 'Copyright 2025 Advanced Subtitle Translator Team'

# Version components
VERSION_MAJOR = 2
VERSION_MINOR = 1
VERSION_PATCH = 0
VERSION_BUILD = 0

# Build version string
def get_version():
    """Get the version string."""
    return f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

def get_version_info():
    """Get detailed version information."""
    return {
        'version': __version__,
        'title': __title__,
        'description': __description__,
        'author': __author__,
        'license': __license__,
        'major': VERSION_MAJOR,
        'minor': VERSION_MINOR,
        'patch': VERSION_PATCH,
        'build': VERSION_BUILD
    }

if __name__ == '__main__':
    print(f"{__title__} v{__version__}")
    print(__description__)
    print(f"By {__author__}")
    print(f"License: {__license__}")
