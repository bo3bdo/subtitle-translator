#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Subtitle Translator - Universal Launcher
مشغل عالمي لمترجم الترجمات المتقدم
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to launch the GUI application"""
    try:
        print("🚀 Starting Advanced Subtitle Translator...")
        print("📱 Initializing GUI Application...")
        
        # Import and create GUI
        from gui_translator import SubtitleTranslatorGUI
        
        # Create and run application
        app = SubtitleTranslatorGUI()
        
        # Show startup message in English (console always English)
        from config import Config
        config = Config()
        ui_lang = config.get('ui_language', 'en')
        
        if ui_lang == 'ar':
            print("✅ Arabic interface loaded successfully!")
            print("📱 GUI ready with Arabic interface")
        else:
            print("✅ English interface loaded successfully!")
            print("📱 GUI ready with English interface")
        
        print("🎯 Application started successfully!")
        
        # Start the application
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Please install required dependencies:")
        print("   pip install -r requirements.txt")
        print("\n📦 Required packages:")
        print("   - googletrans==4.0.0rc1")
        print("   - langdetect")
        print("   - chardet")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
