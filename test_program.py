#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع للبرنامج المحدث
Quick test for the updated program
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic functionality without translation"""
    print("🧪 Testing Subtitle Translator v2.2.2...")
    
    try:
        from translate_subtitles import SubtitleTranslator
        from config import Config
        from cache import TranslationCache
        
        print("✅ All modules imported successfully")
        
        # Test config
        config = Config()
        print(f"✅ Config loaded - UI Language: {config.get('ui_language')}")
        
        # Test translator initialization
        translator = SubtitleTranslator()
        print(f"✅ Translator initialized - Engine: {translator.current_engine}")
        
        # Test UI text retrieval
        welcome_text = config.get_ui_text('welcome')
        print(f"✅ UI Text: {welcome_text}")
        
        # Test cache
        if translator.cache:
            stats = translator.cache.get_cache_stats()
            print(f"✅ Cache system working - Size: {stats.get('database_size_mb', 0)} MB")
        
        print("\n🎉 All basic tests passed!")
        print("🔥 Ready to run the full program!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    
    if success:
        print("\n" + "="*50)
        print("Ready to run the main program!")
        print("Use: python translate_subtitles.py")
        print("="*50)
    else:
        print("\n❌ Fix the errors before running the main program")
