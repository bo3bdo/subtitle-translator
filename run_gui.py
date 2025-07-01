#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start - Advanced Subtitle Translator GUI
تشغيل سريع للواجهة الرسومية
"""

import os
import sys

def main():
    """Quick start function"""
    print("🚀 Starting Advanced Subtitle Translator GUI...")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Import and start GUI directly
        from gui_translator import SubtitleTranslatorGUI
        
        print("✅ Loading GUI...")
        app = SubtitleTranslatorGUI()
        
        # Check for command line file
        if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
            app.input_file_var.set(sys.argv[1])
            app.auto_output_file()
            app.detect_input_format()
        
        print("🎯 GUI Ready!")
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Try installing missing dependencies:")
        print("   pip install googletrans==4.0.0rc1")
        print("   pip install langdetect")
        print("   pip install chardet")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
