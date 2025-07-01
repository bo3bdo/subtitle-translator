#!/usr/bin/env python3
"""
Setup script for Advanced Subtitle Translator
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open('README_NEW.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Get version
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'version.py')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            exec(f.read())
            return locals()['__version__']
    return '2.2.2'

setup(
    name='advanced-subtitle-translator',
    version=get_version(),
    description='Advanced GUI application for translating subtitle files with intelligent caching and multi-format support',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Advanced Subtitle Translator Team',
    author_email='contact@subtitle-translator.dev',
    url='https://github.com/yourusername/advanced-subtitle-translator',
    download_url='https://github.com/yourusername/advanced-subtitle-translator/archive/v2.2.2.tar.gz',
    
    packages=find_packages(),
    py_modules=[
        'gui_translator',
        'translate_subtitles', 
        'config',
        'subtitle_formats',
        'language_detector',
        'cache',
        'run_gui',
        'start_gui'
    ],
    
    install_requires=read_requirements(),
    
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'flake8>=6.0.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'mypy>=1.0.0'
        ],
        'docs': [
            'sphinx>=6.0.0',
            'sphinx-rtd-theme>=1.2.0',
            'myst-parser>=1.0.0'
        ]
    },
    
    entry_points={
        'console_scripts': [
            'subtitle-translator=translate_subtitles:main',
            'subtitle-translator-gui=run_gui:main',
        ],
        'gui_scripts': [
            'subtitle-translator-gui=run_gui:main',
        ]
    },
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Environment :: X11 Applications',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Natural Language :: English',
        'Natural Language :: Arabic',
    ],
    
    keywords=[
        'subtitle', 'translation', 'srt', 'ass', 'vtt', 'gui', 'tkinter',
        'video', 'movies', 'tv-shows', 'multilingual', 'batch-processing',
        'drag-drop', 'caching', 'language-detection'
    ],
    
    python_requires='>=3.7',
    
    package_data={
        '': ['*.md', '*.txt', '*.json', '*.ini'],
    },
    
    include_package_data=True,
    zip_safe=False,
    
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/advanced-subtitle-translator/issues',
        'Source': 'https://github.com/yourusername/advanced-subtitle-translator',
        'Documentation': 'https://github.com/yourusername/advanced-subtitle-translator/blob/main/README_NEW.md',
        'Changelog': 'https://github.com/yourusername/advanced-subtitle-translator/blob/main/CHANGELOG.md',
        'Funding': 'https://github.com/sponsors/yourusername',
    },
)
