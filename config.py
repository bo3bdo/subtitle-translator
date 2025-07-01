#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف الإعدادات لمترجم الترجمات
Configuration file for Subtitle Translator
"""

import json
import os

class Config:
    """إدارة إعدادات التطبيق"""
    
    DEFAULT_CONFIG = {
        "default_target_language": "ar",
        "default_source_language": "en", 
        "translation_engine": "google",
        "batch_size": 10,
        "delay_between_requests": 0.1,
        "cache_enabled": True,
        "auto_detect_encoding": True,
        "preserve_formatting": True,
        "create_backup": True,
        "max_retries": 3,
        "supported_formats": [".srt", ".ass", ".vtt"],
        "output_suffix": "_arabic",
        "ui_language": "en"  # Changed default to English
    }
    
    # UI Language translations
    UI_TEXTS = {
        "en": {
            "app_title": "Advanced Subtitle Translator v2.0",
            "welcome": "Welcome to the enhanced version 2!",
            "main_menu": "Main Menu:",
            "menu_options": {
                "1": "Translate specific file",
                "2": "Translate all SRT files in current directory", 
                "3": "Search in another directory",
                "4": "Translator settings",
                "5": "Show statistics",
                "6": "Help",
                "7": "Exit"
            },
            "choose_option": "Choose from [1-7]: ",
            "invalid_choice": "Invalid choice, please try again",
            "goodbye": "Thank you for using Subtitle Translator!",
            "file_not_found": "File not found",
            "not_srt_file": "File is not an SRT file",
            "translation_started": "Starting translation:",
            "translation_saved": "Translation saved to:",
            "translation_failed": "Failed to translate file",
            "enter_file_path": "Enter file path: ",
            "enter_directory_path": "Enter directory path: ",
            "directory_not_found": "Directory not found",
            "path_not_directory": "Path is not a directory",
            "searching_in": "Searching in:",
            "current_target_lang": "Current target language:",
            "change_target_lang": "Do you want to change target language? (y/N): ",
            "enter_lang_code": "Enter language code (e.g.: ar, en, fr): ",
            "settings_menu": "Translator Settings",
            "settings_options": {
                "1": "Show current settings",
                "2": "Change target language", 
                "3": "Change translation engine",
                "4": "Manage cache",
                "5": "Change UI language",
                "6": "Reset to defaults",
                "7": "Back to main menu"
            },
            "current_settings": "Current Settings:",
            "target_language": "Target Language",
            "source_language": "Source Language", 
            "translation_engine": "Translation Engine",
            "cache_status": "Cache",
            "backup_status": "Backup",
            "delay_time": "Delay Time",
            "max_retries": "Max Retries",
            "enabled": "Enabled",
            "disabled": "Disabled",
            "seconds": "seconds",
            "cache_not_enabled": "Cache is not enabled",
            "cache_management": "Cache Management",
            "cache_options": {
                "1": "Show statistics",
                "2": "Clean old translations",
                "3": "Clear all translations", 
                "4": "Back"
            },
            "session_stats": "Session Statistics",
            "session_duration": "Session Duration",
            "files_processed": "Files Processed",
            "total_translations": "Total Translations",
            "cache_hits": "Cache Hits",
            "translation_errors": "Translation Errors",
            "cache_size": "Cache Size",
            "cache_hit_rate": "Cache Hit Rate",
            "help_title": "Subtitle Translator v2.0 Help",
            "error_loading_config": "Error loading config:",
            "error_saving_config": "Error saving config:",
            "settings_reset": "Settings reset to defaults",
            "operation_cancelled": "Operation cancelled"
        },
        "ar": {
            "app_title": "مترجم الترجمات المتقدم v2.0",
            "welcome": "مرحباً بك في الإصدار الثاني المحسن!",
            "main_menu": "القائمة الرئيسية:",
            "menu_options": {
                "1": "ترجمة ملف محدد",
                "2": "ترجمة جميع ملفات SRT في المجلد الحالي",
                "3": "البحث في مجلد آخر", 
                "4": "إعدادات المترجم",
                "5": "عرض الإحصائيات",
                "6": "مساعدة",
                "7": "خروج"
            },
            "choose_option": "اختر من [1-7]: ",
            "invalid_choice": "اختيار غير صحيح، يرجى المحاولة مرة أخرى",
            "goodbye": "شكراً لاستخدام مترجم الترجمات!",
            "file_not_found": "الملف غير موجود",
            "not_srt_file": "الملف ليس من نوع SRT",
            "translation_started": "بدء ترجمة:",
            "translation_saved": "تم حفظ الترجمة في:",
            "translation_failed": "فشل في ترجمة الملف",
            "enter_file_path": "أدخل مسار الملف: ",
            "enter_directory_path": "أدخل مسار المجلد: ",
            "directory_not_found": "المجلد غير موجود",
            "path_not_directory": "المسار المدخل ليس مجلداً",
            "searching_in": "البحث في:",
            "current_target_lang": "اللغة المستهدفة الحالية:",
            "change_target_lang": "هل تريد تغيير اللغة المستهدفة؟ (y/N): ",
            "enter_lang_code": "أدخل رمز اللغة (مثل: ar, en, fr): ",
            "settings_menu": "إعدادات المترجم",
            "settings_options": {
                "1": "عرض الإعدادات الحالية",
                "2": "تغيير اللغة المستهدفة",
                "3": "تغيير محرك الترجمة",
                "4": "إدارة الذاكرة المؤقتة",
                "5": "تغيير لغة الواجهة",
                "6": "إعادة تعيين إلى الافتراضي",
                "7": "العودة للقائمة الرئيسية"
            },
            "current_settings": "الإعدادات الحالية:",
            "target_language": "اللغة المستهدفة",
            "source_language": "اللغة المصدر",
            "translation_engine": "محرك الترجمة", 
            "cache_status": "الذاكرة المؤقتة",
            "backup_status": "النسخ الاحتياطي",
            "delay_time": "زمن التأخير",
            "max_retries": "عدد المحاولات",
            "enabled": "مفعلة",
            "disabled": "معطلة",
            "seconds": "ثانية",
            "cache_not_enabled": "الذاكرة المؤقتة غير مفعلة",
            "cache_management": "إدارة الذاكرة المؤقتة",
            "cache_options": {
                "1": "عرض الإحصائيات",
                "2": "تنظيف الترجمات القديمة",
                "3": "مسح جميع الترجمات",
                "4": "العودة"
            },
            "session_stats": "إحصائيات الجلسة",
            "session_duration": "مدة الجلسة",
            "files_processed": "الملفات المعالجة",
            "total_translations": "إجمالي الترجمات", 
            "cache_hits": "استخدام الذاكرة المؤقتة",
            "translation_errors": "أخطاء الترجمة",
            "cache_size": "حجم الذاكرة المؤقتة",
            "cache_hit_rate": "معدل الاستفادة من الذاكرة",
            "help_title": "مساعدة مترجم الترجمات v2.0",
            "error_loading_config": "خطأ في تحميل الإعدادات:",
            "error_saving_config": "خطأ في حفظ الإعدادات:",
            "settings_reset": "تم إعادة تعيين الإعدادات إلى القيم الافتراضية",
            "operation_cancelled": "تم إلغاء العملية"
        }
    }
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """تحميل الإعدادات من الملف"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # دمج الإعدادات الافتراضية مع المحملة
                config = self.DEFAULT_CONFIG.copy()
                config.update(loaded_config)
                return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """حفظ الإعدادات إلى الملف"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """الحصول على قيمة إعداد"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """تعيين قيمة إعداد"""
        self.config[key] = value
    
    def reset_to_defaults(self):
        """إعادة تعيين الإعدادات إلى القيم الافتراضية"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
    
    def update_config(self, updates):
        """تحديث عدة إعدادات مرة واحدة"""
        self.config.update(updates)
        self.save_config()
    
    def get_ui_text(self, key, default=""):
        """الحصول على النص المترجم حسب لغة الواجهة"""
        ui_lang = self.get('ui_language', 'en')
        
        # التنقل في النصوص المتداخلة
        keys = key.split('.')
        text_dict = self.UI_TEXTS.get(ui_lang, self.UI_TEXTS['en'])
        
        try:
            for k in keys:
                text_dict = text_dict[k]
            return text_dict
        except (KeyError, TypeError):
            # إذا لم يوجد النص، حاول الإنجليزية
            try:
                text_dict = self.UI_TEXTS['en']
                for k in keys:
                    text_dict = text_dict[k]
                return text_dict
            except (KeyError, TypeError):
                return default or key
    
    def change_ui_language(self):
        """Change interface language - Always display in English to avoid console issues"""
        current_lang = self.get('ui_language', 'en')
        
        # Always show in English to avoid console encoding issues
        print(f"\nCurrent UI language: {'English' if current_lang == 'en' else 'Arabic'}")
        print("Available languages:")
        print("1. English (Recommended for most consoles)")
        print("2. Arabic (May not display correctly in some consoles)")
        choice = input("Choose [1-2]: ").strip()
        
        if choice == '1':
            self.set('ui_language', 'en')
            self.save_config()
            print("✅ UI language changed to English")
        elif choice == '2':
            self.set('ui_language', 'ar')
            self.save_config()
            print("✅ UI language changed to Arabic")
            print("⚠️  Note: Arabic text may not display correctly in all consoles")
        else:
            print("❌ Invalid choice")
    
    def check_console_support(self):
        """Check if console supports Arabic text properly"""
        try:
            # Try to encode Arabic text
            test_text = "مرحبا"
            test_text.encode('utf-8')
            return True
        except:
            return False
    
    def safe_print(self, text, fallback_text=""):
        """Safely print text, fall back to English if Arabic fails"""
        try:
            print(text)
        except UnicodeEncodeError:
            if fallback_text:
                print(fallback_text)
            else:
                # Convert to ASCII representation
                print(text.encode('ascii', 'ignore').decode('ascii'))
