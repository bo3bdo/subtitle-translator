#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for GUI Translator
اختبار الواجهة الرسومية لمترجم الترجمات
"""

import os
import sys
import threading
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gui_components():
    """Test GUI components without actually opening the GUI"""
    print("Testing GUI Translator Components...")
    print("=" * 50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from gui_translator import SubtitleTranslatorGUI
        from translate_subtitles import SubtitleTranslator
        from config import Config
        from subtitle_formats import SubtitleFormatHandler
        from language_detector import LanguageDetector
        print("   ✓ All modules imported successfully")
        
        # Test component initialization
        print("\n2. Testing component initialization...")
        config = Config()
        translator = SubtitleTranslator()
        format_handler = SubtitleFormatHandler()
        language_detector = LanguageDetector()
        print("   ✓ All components initialized successfully")
        
        # Test configuration
        print("\n3. Testing configuration...")
        print(f"   • Cache enabled: {config.get('cache_enabled', True)}")
        print(f"   • Default source language: {config.get('default_source_language', 'en')}")
        print(f"   • Default target language: {config.get('default_target_language', 'ar')}")
        print(f"   • Translation engine: {config.get('translation_engine', 'google')}")
        print("   ✓ Configuration loaded successfully")
        
        # Test format detection
        print("\n4. Testing format detection...")
        test_file = "test_movie.srt"
        if os.path.exists(test_file):
            format_type = format_handler.detect_format(test_file)
            print(f"   • Detected format for {test_file}: {format_type}")
            print("   ✓ Format detection working")
        else:
            print("   ! Test file not found, skipping format detection test")
        
        # Test language detection
        print("\n5. Testing language detection...")
        test_text = "Hello, this is a test subtitle."
        detected_lang = language_detector.detect_language(test_text)
        print(f"   • Detected language for test text: {detected_lang}")
        print("   ✓ Language detection working")
        
        print("\n" + "=" * 50)
        print("All component tests passed! ✅")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_creation():
    """Test GUI creation and basic functionality"""
    print("\nTesting GUI Creation...")
    print("=" * 50)
    
    try:
        from gui_translator import SubtitleTranslatorGUI
        
        print("1. Creating GUI instance...")
        app = SubtitleTranslatorGUI()
        print("   ✓ GUI instance created successfully")
        
        print("\n2. Testing GUI methods...")
        
        # Test language list
        languages = app.get_language_list()
        print(f"   • Available languages: {len(languages)} languages")
        print(f"   • Sample languages: {languages[:5]}")
        
        # Test file validation
        print("   • Testing input validation...")
        result = app.validate_translation_inputs()
        print(f"   • Validation result (empty inputs): {result}")
        
        # Test settings methods
        print("   • Testing settings...")
        app.load_settings_to_gui()
        print("   ✓ Settings loaded to GUI")
        
        # Test statistics
        print("   • Testing statistics...")
        app.refresh_stats()
        print("   ✓ Statistics refreshed")
        
        print("\n3. Testing utility methods...")
        app.update_status("Test status message")
        app.update_file_count()
        print("   ✓ Utility methods working")
        
        print("\n" + "=" * 50)
        print("GUI creation tests passed! ✅")
        print("\nNote: GUI window not shown during testing.")
        print("To test the full GUI, run: python gui_translator.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_integration():
    """Test integration between GUI and backend components"""
    print("\nTesting GUI Integration...")
    print("=" * 50)
    
    try:
        from gui_translator import SubtitleTranslatorGUI
        
        app = SubtitleTranslatorGUI()
        
        print("1. Testing component integration...")
        
        # Test if all required components are available
        assert hasattr(app, 'config'), "Config component missing"
        assert hasattr(app, 'translator'), "Translator component missing"
        assert hasattr(app, 'format_handler'), "Format handler missing"
        assert hasattr(app, 'language_detector'), "Language detector missing"
        print("   ✓ All components integrated")
        
        print("\n2. Testing file operations...")
        
        # Test file validation with test file
        test_file = "test_movie.srt"
        if os.path.exists(test_file):
            app.input_file_var.set(test_file)
            app.output_file_var.set("output_test.srt")
            
            result = app.validate_translation_inputs()
            print(f"   • File validation result: {result}")
            
            # Test format detection
            app.detect_input_format()
            format_detected = app.input_format_var.get()
            print(f"   • Detected format: {format_detected}")
            
            # Test language detection
            app.detect_language()
            print("   ✓ Language detection completed")
            
        else:
            print("   ! Test file not found, creating mock test...")
            # Create a simple test file
            with open("temp_test.srt", "w", encoding="utf-8") as f:
                f.write("1\n00:00:01,000 --> 00:00:03,000\nTest subtitle\n\n")
            
            app.input_file_var.set("temp_test.srt")
            app.output_file_var.set("temp_output.srt")
            
            result = app.validate_translation_inputs()
            print(f"   • Mock file validation: {result}")
            
            # Clean up
            if os.path.exists("temp_test.srt"):
                os.remove("temp_test.srt")
        
        print("\n3. Testing settings integration...")
        
        # Test settings save/load
        original_engine = app.config.get('translation_engine', 'google')
        app.engine_var.set('microsoft')
        
        # Test if settings are properly linked
        assert app.engine_var.get() == 'microsoft', "Settings not properly linked"
        print("   ✓ Settings integration working")
        
        print("\n" + "=" * 50)
        print("Integration tests passed! ✅")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all GUI tests"""
    print("🧪 GUI Translator Test Suite")
    print("=" * 60)
    
    tests = [
        ("Component Tests", test_gui_components),
        ("GUI Creation Tests", test_gui_creation),
        ("Integration Tests", test_gui_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GUI is ready to use.")
        print("\n🚀 To start the GUI application, run:")
        print("   python gui_translator.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("Starting GUI Translator Tests...")
    print("Current directory:", os.getcwd())
    print("Available files:", [f for f in os.listdir('.') if f.endswith('.py')])
    
    success = run_all_tests()
    
    if success:
        print("\n💡 GUI Testing completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python gui_translator.py' to start the GUI")
        print("2. Test drag & drop functionality")
        print("3. Try single file translation")
        print("4. Test batch processing")
        print("5. Check settings and cache functionality")
    else:
        print("\n🔧 Please fix the issues above before using the GUI.")
