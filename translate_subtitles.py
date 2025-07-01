#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة ترجمة الترجمات
Subtitle Translation Tool
تترجم ملفات الترجمة SRT من الإنجليزية إلى العربية
Translates SRT subtitle files from English to Arabic
https://github.com/bo3bdo/subtitle-translator 
"""

import re
import os
import glob
from deep_translator import GoogleTranslator, MicrosoftTranslator
import time
import argparse
import shutil
from datetime import datetime
import concurrent.futures
import threading
from config import Config
from cache import TranslationCache

class SubtitleTranslator:
    def __init__(self, config_file="config.json"):
        # تحميل الإعدادات
        self.config = Config(config_file)
        
        # إعداد محرك الترجمة
        self.setup_translator()
        
        # إعداد نظام التخزين المؤقت
        if self.config.get('cache_enabled'):
            self.cache = TranslationCache()
        else:
            self.cache = None
        
        # إحصائيات الجلسة
        self.session_stats = {
            'files_processed': 0,
            'subtitles_translated': 0,
            'cache_hits': 0,
            'translation_errors': 0,
            'start_time': datetime.now()
        }
    
    def setup_translator(self):
        """إعداد محرك الترجمة حسب الإعدادات"""
        engine = self.config.get('translation_engine', 'google')
        source_lang = self.config.get('default_source_language', 'en')
        target_lang = self.config.get('default_target_language', 'ar')
        
        try:
            if engine == 'google':
                self.translator = GoogleTranslator(source=source_lang, target=target_lang)
            elif engine == 'microsoft':
                self.translator = MicrosoftTranslator(source=source_lang, target=target_lang)
            else:
                # Default to Google
                self.translator = GoogleTranslator(source=source_lang, target=target_lang)
            
            self.current_engine = engine
            print(f"Translation engine setup: {engine}")
            
        except Exception as e:
            print(f"Error setting up translation engine: {e}")
            # Fall back to Google Translator
            self.translator = GoogleTranslator(source=source_lang, target=target_lang)
            self.current_engine = 'google'
    
    def find_srt_files(self, directory="."):
        """Find all SRT files in the specified directory"""
        srt_files = glob.glob(os.path.join(directory, "*.srt"))
        return [f for f in srt_files if not f.endswith("_arabic.srt")]
        
    def parse_srt_file(self, file_path):
        """Parse SRT file and extract subtitle entries"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split by double newlines to separate subtitle blocks
        blocks = re.split(r'\n\s*\n', content.strip())
        
        subtitles = []
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # Extract subtitle number
                try:
                    number = int(lines[0])
                except ValueError:
                    continue
                
                # Extract timestamp
                timestamp = lines[1]
                
                # Extract text (may be multiple lines)
                text = '\n'.join(lines[2:])
                
                subtitles.append({
                    'number': number,
                    'timestamp': timestamp,
                    'text': text
                })
        
        return subtitles
    
    def translate_text(self, text, target_lang=None, max_retries=None):
        """ترجمة النص مع دعم الذاكرة المؤقتة وإعادة المحاولة"""
        if not text.strip():
            return text
            
        # استخدام اللغة المستهدفة من الإعدادات إذا لم تُحدد
        if target_lang is None:
            target_lang = self.config.get('default_target_language', 'ar')
        
        if max_retries is None:
            max_retries = self.config.get('max_retries', 3)
        
        source_lang = self.config.get('default_source_language', 'en')
        
        # تخطي الأسطر الفارغة أو الرموز الخاصة فقط
        if text.strip() in ['', '-', '--', '...', '♪', '♫']:
            return text
        
        # البحث في الذاكرة المؤقتة أولاً
        if self.cache:
            cached_result = self.cache.get_cached_translation(text, source_lang, target_lang)
            if cached_result:
                self.session_stats['cache_hits'] += 1
                return cached_result
        
        # محاولة الترجمة مع إعادة المحاولة
        for attempt in range(max_retries):
            try:
                # تحديث محرك الترجمة إذا تغيرت اللغة المستهدفة
                if hasattr(self.translator, 'target') and self.translator.target != target_lang:
                    self.translator.target = target_lang
                
                result = self.translator.translate(text)
                
                # حفظ في الذاكرة المؤقتة
                if self.cache and result:
                    self.cache.save_translation(text, result, source_lang, target_lang, self.current_engine)
                
                return result if result else text
                
            except Exception as e:
                print(f"خطأ في المحاولة {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    # انتظار متزايد بين المحاولات
                    time.sleep(0.5 * (attempt + 1))
                else:
                    self.session_stats['translation_errors'] += 1
                    print(f"Translation failed for: '{text[:50]}...'" + ("" if len(text) <= 50 else ""))
                    return text  # Return original text if translation fails
    
    def translate_subtitles(self, subtitles, target_lang='ar', delay=0.1):
        """Translate all subtitle entries"""
        translated_subtitles = []
        total = len(subtitles)
        
        print(f"Translating {total} subtitle entries...")
        
        for i, subtitle in enumerate(subtitles):
            print(f"Progress: {i+1}/{total} ({((i+1)/total)*100:.1f}%)", end='\r')
            
            # Translate the text
            translated_text = self.translate_text(subtitle['text'], target_lang)
            
            translated_subtitles.append({
                'number': subtitle['number'],
                'timestamp': subtitle['timestamp'],
                'text': translated_text
            })
            
            # Add delay to avoid rate limiting
            if delay > 0:
                time.sleep(delay)
        
        print(f"\nTranslation completed!")
        return translated_subtitles
    
    def save_srt_file(self, subtitles, output_path):
        """Save translated subtitles to SRT file"""
        with open(output_path, 'w', encoding='utf-8') as file:
            for subtitle in subtitles:
                file.write(f"{subtitle['number']}\n")
                file.write(f"{subtitle['timestamp']}\n")
                file.write(f"{subtitle['text']}\n\n")
        
        print(f"Translated subtitles saved to: {os.path.basename(output_path)}")
    
    def translate_srt_file(self, input_path, output_path=None, target_lang=None):
        """الدالة الرئيسية لترجمة ملف SRT مع التحسينات الجديدة"""
        if not os.path.exists(input_path):
            print(f"خطأ: الملف '{input_path}' غير موجود")
            return None
        
        # Validate file
        is_valid, validation_message = self.validate_srt_file(input_path)
        if not is_valid:
            print(f"File validation error: {validation_message}")
            return None
        
        # إنشاء نسخة احتياطية
        self.create_backup(input_path)
        
        # تحديد مسار الملف المترجم
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            suffix = self.config.get('output_suffix', '_arabic')
            output_path = f"{base_name}{suffix}.srt"
        
        # استخدام اللغة المستهدفة من الإعدادات إذا لم تُحدد
        if target_lang is None:
            target_lang = self.config.get('default_target_language', 'ar')
        
        print(f"📖 قراءة ملف الترجمة: {os.path.basename(input_path)}")
        subtitles = self.parse_srt_file(input_path)
        print(f"✅ تم العثور على {len(subtitles)} ترجمة")
        
        # إحصائيات قبل البدء
        if self.cache:
            cache_stats = self.cache.get_cache_stats()
            print(f"💾 الذاكرة المؤقتة: {cache_stats.get('total_translations', 0)} ترجمة محفوظة")
        
        # بدء الترجمة
        start_time = datetime.now()
        translated_subtitles = self.translate_subtitles(subtitles, target_lang)
        end_time = datetime.now()
        
        # حفظ الملف المترجم
        self.save_srt_file(translated_subtitles, output_path)
        
        # تحديث الإحصائيات
        self.session_stats['files_processed'] += 1
        self.session_stats['subtitles_translated'] += len(subtitles)
        
        # عرض الإحصائيات
        duration = (end_time - start_time).total_seconds()
        print(f"\n⏱️  وقت الترجمة: {duration:.1f} ثانية")
        print(f"🎯 معدل الترجمة: {len(subtitles)/duration:.1f} ترجمة/ثانية")
        if self.session_stats['cache_hits'] > 0:
            print(f"⚡ استفادة من الذاكرة المؤقتة: {self.session_stats['cache_hits']} ترجمة")
        
        return output_path
    
    def translate_all_srt_files(self, directory="."):
        """Translate all SRT files in specified directory"""
        srt_files = self.find_srt_files(directory)
        
        if not srt_files:
            print("No SRT files found in the specified directory")
            return []
        
        print(f"Found {len(srt_files)} subtitle files:")
        
        for i, file_path in enumerate(srt_files, 1):
            print(f"{i}. {os.path.basename(file_path)}")
        
        translated_files = []
        for i, file_path in enumerate(srt_files, 1):
            print(f"\n{'='*60}")
            print(f"Translating file {i}/{len(srt_files)}: {os.path.basename(file_path)}")
            print(f"{'='*60}")
            
            try:
                output_file = self.translate_srt_file(file_path)
                if output_file:
                    translated_files.append(output_file)
            except Exception as e:
                print(f"Error translating file {os.path.basename(file_path)}: {e}")
        
        return translated_files
    
    def interactive_mode(self):
        """Enhanced interactive mode with multi-language support"""
        print(f"🎬 {self.config.get_ui_text('app_title')}")
        print("="*50)
        print(self.config.get_ui_text('welcome'))
        
        while True:
            print(f"\n🔧 {self.config.get_ui_text('main_menu')}")
            print("="*30)
            menu_options = self.config.get_ui_text('menu_options')
            for key, text in menu_options.items():
                icon = ["📄", "📁", "🔍", "⚙️", "📊", "❓", "🚪"][int(key)-1]
                print(f"{key}. {icon} {text}")
            
            choice = input(f"\n{self.config.get_ui_text('choose_option')}").strip()
            
            if choice == '1':
                self.handle_single_file_translation()
                
            elif choice == '2':
                print(f"\n🔄 {self.config.get_ui_text('menu_options.2')}...")
                self.translate_all_srt_files(".")
                
            elif choice == '3':
                self.handle_directory_translation()
                
            elif choice == '4':
                self.show_settings_menu()
                
            elif choice == '5':
                self.show_session_stats()
                
            elif choice == '6':
                self.show_help()
                
            elif choice == '7':
                print(f"\n👋 {self.config.get_ui_text('goodbye')}")
                self.show_session_stats()
                break
                
            else:
                print(f"❌ {self.config.get_ui_text('invalid_choice')}")

    def handle_single_file_translation(self):
        """Handle single file translation with multi-language support"""
        file_path = input(f"\n📂 {self.config.get_ui_text('enter_file_path')}").strip().strip('"')
        
        if not os.path.exists(file_path):
            print(f"❌ {self.config.get_ui_text('file_not_found')}")
            return
            
        if not file_path.lower().endswith('.srt'):
            print(f"❌ {self.config.get_ui_text('not_srt_file')}")
            return
        
        # Choose target language (optional)
        current_lang = self.config.get('default_target_language')
        print(f"\n🎯 {self.config.get_ui_text('current_target_lang')} {current_lang}")
        change_lang = input(self.config.get_ui_text('change_target_lang')).strip().lower()
        
        target_lang = None
        if change_lang == 'y':
            target_lang = input(self.config.get_ui_text('enter_lang_code')).strip()
            if not target_lang:
                target_lang = current_lang
        
        print(f"\n🚀 {self.config.get_ui_text('translation_started')} {os.path.basename(file_path)}")
        result = self.translate_srt_file(file_path, target_lang=target_lang)
        
        if result:
            print(f"✅ {self.config.get_ui_text('translation_saved')} {os.path.basename(result)}")
        else:
            print(f"❌ {self.config.get_ui_text('translation_failed')}")

    def handle_directory_translation(self):
        """Handle directory translation with multi-language support"""
        directory = input(f"\n📁 {self.config.get_ui_text('enter_directory_path')}").strip().strip('"')
        
        if not os.path.exists(directory):
            print(f"❌ {self.config.get_ui_text('directory_not_found')}")
            return
            
        if not os.path.isdir(directory):
            print(f"❌ {self.config.get_ui_text('path_not_directory')}")
            return
        
        print(f"\n🔍 {self.config.get_ui_text('searching_in')} {directory}")
        self.translate_all_srt_files(directory)

    def show_help(self):
        """Show help with multi-language support"""
        ui_lang = self.config.get('ui_language', 'en')
        
        if ui_lang == 'ar':
            help_text = """
🔹 مساعدة مترجم الترجمات v2.2.2
================================

📋 الميزات الجديدة:
• نظام إعدادات متقدم مع حفظ التفضيلات
• ذاكرة مؤقتة ذكية لتجنب إعادة الترجمة
• نسخ احتياطية تلقائية للملفات
• دعم محركات ترجمة متعددة
• إحصائيات مفصلة للاستخدام
• واجهة محسنة مع دعم العربية والإنجليزية

🎯 نصائح للاستخدام:
• استخدم ملفات SRT صحيحة التنسيق
• تأكد من اتصال الإنترنت المستقر
• راجع الإعدادات قبل الترجمة الجماعية
• استفد من الذاكرة المؤقتة للملفات المتشابهة

⚙️ الإعدادات:
• يمكن تخصيص اللغات والمحركات
• تفعيل/تعطيل النسخ الاحتياطية
• إدارة الذاكرة المؤقتة
• تغيير لغة الواجهة

📞 الدعم:
• لمزيد من المساعدة: github.com/bo3bdo/subtitle-translator
"""
        else:
            help_text = """
🔹 Subtitle Translator v2.2.2 Help
================================

📋 New Features:
• Advanced settings system with preference saving
• Smart cache to avoid re-translation
• Automatic file backups
• Multiple translation engine support
• Detailed usage statistics
• Enhanced interface with Arabic and English support

🎯 Usage Tips:
• Use properly formatted SRT files
• Ensure stable internet connection
• Review settings before batch translation
• Utilize cache for similar files

⚙️ Settings:
• Customize languages and engines
• Enable/disable automatic backups
• Manage translation cache
• Change interface language

📞 Support:
• For more help: github.com/bo3bdo/subtitle-translator
"""
        
        print(help_text)
    def create_backup(self, file_path):
        """إنشاء نسخة احتياطية من الملف"""
        if not self.config.get('create_backup', True):
            return None
            
        try:
            # إنشاء مجلد النسخ الاحتياطية
            backup_dir = os.path.join(os.path.dirname(file_path), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # إنشاء اسم النسخة الاحتياطية مع الوقت
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            backup_filename = f"{name}_backup_{timestamp}{ext}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Copy the file
            shutil.copy2(file_path, backup_path)
            print(f"Backup created: {backup_filename}")
            return backup_path
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None

    def validate_srt_file(self, file_path):
        """Validate SRT file format"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Basic format check
            if not content.strip():
                return False, "File is empty"
            
            # Check for subtitle numbers and timestamps
            import re
            srt_pattern = r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
            if not re.search(srt_pattern, content):
                return False, "Invalid SRT format"
            
            return True, "File is valid"
            
        except UnicodeDecodeError:
            return False, "File encoding issue"
        except Exception as e:
            return False, f"Error: {e}"
    
    def show_session_stats(self):
        """Show session statistics with multi-language support"""
        print("\n" + "="*50)
        print(f"📊 {self.config.get_ui_text('session_stats')}")
        print("="*50)
        
        session_duration = datetime.now() - self.session_stats['start_time']
        hours, remainder = divmod(session_duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print(f"⏱️  {self.config.get_ui_text('session_duration')}: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        print(f"📁 {self.config.get_ui_text('files_processed')}: {self.session_stats['files_processed']}")
        print(f"📝 {self.config.get_ui_text('total_translations')}: {self.session_stats['subtitles_translated']}")
        print(f"⚡ {self.config.get_ui_text('cache_hits')}: {self.session_stats['cache_hits']}")
        print(f"❌ {self.config.get_ui_text('translation_errors')}: {self.session_stats['translation_errors']}")
        
        if self.cache:
            cache_stats = self.cache.get_cache_stats()
            print(f"💾 {self.config.get_ui_text('cache_size')}: {cache_stats.get('database_size_mb', 0)} MB")
            print(f"🎯 {self.config.get_ui_text('cache_hit_rate')}: {cache_stats.get('cache_hit_potential', 0)}%")
        
        print("="*50)

    def show_settings_menu(self):
        """Settings management menu with multi-language support"""
        while True:
            print("\n" + "="*40)
            print(f"⚙️  {self.config.get_ui_text('settings_menu')}")
            print("="*40)
            settings_options = self.config.get_ui_text('settings_options')
            for key, text in settings_options.items():
                print(f"{key}. {text}")
            
            choice = input(f"\n{self.config.get_ui_text('choose_option').replace('[1-7]', '[1-7]')}: ").strip()
            
            if choice == '1':
                self.show_current_settings()
            elif choice == '2':
                self.change_target_language()
            elif choice == '3':
                self.change_translation_engine()
            elif choice == '4':
                self.manage_cache()
            elif choice == '5':
                self.config.change_ui_language()
            elif choice == '6':
                self.reset_settings()
            elif choice == '7':
                break
            else:
                print(f"❌ {self.config.get_ui_text('invalid_choice')}")

    def show_current_settings(self):
        """Show current settings with multi-language support"""
        print("\n" + "="*40)
        print(f"📋 {self.config.get_ui_text('current_settings')}")
        print("="*40)
        
        settings_display = {
            self.config.get_ui_text('target_language'): self.config.get('default_target_language'),
            self.config.get_ui_text('source_language'): self.config.get('default_source_language'),
            self.config.get_ui_text('translation_engine'): self.config.get('translation_engine'),
            self.config.get_ui_text('cache_status'): self.config.get_ui_text('enabled') if self.config.get('cache_enabled') else self.config.get_ui_text('disabled'),
            self.config.get_ui_text('backup_status'): self.config.get_ui_text('enabled') if self.config.get('create_backup') else self.config.get_ui_text('disabled'),
            self.config.get_ui_text('delay_time'): f"{self.config.get('delay_between_requests')} {self.config.get_ui_text('seconds')}",
            self.config.get_ui_text('max_retries'): self.config.get('max_retries')
        }
        
        for key, value in settings_display.items():
            print(f"{key}: {value}")

    def change_target_language(self):
        """Change target language - Always display in English"""
        languages = {
            '1': ('ar', 'Arabic'),
            '2': ('en', 'English'),
            '3': ('fr', 'French'),
            '4': ('es', 'Spanish'),
            '5': ('de', 'German'),
            '6': ('it', 'Italian'),
            '7': ('ru', 'Russian'),
            '8': ('ja', 'Japanese'),
            '9': ('ko', 'Korean'),
            '10': ('zh', 'Chinese')
        }
        
        print("\nSelect target language:")
        for key, (code, name) in languages.items():
            print(f"{key}. {name} ({code})")
        
        choice = input("\nChoose [1-10]: ").strip()
        if choice in languages:
            lang_code, lang_name = languages[choice]
            self.config.set('default_target_language', lang_code)
            self.config.save_config()
            self.setup_translator()  # Reinitialize translator
            print(f"✅ Target language changed to: {lang_name}")
        else:
            print("❌ Invalid choice")

    def change_translation_engine(self):
        """Change translation engine - Always display in English"""
        engines = {
            '1': ('google', 'Google Translate'),
            '2': ('microsoft', 'Microsoft Translator')
        }
        
        print("\nSelect translation engine:")
        for key, (code, name) in engines.items():
            print(f"{key}. {name}")
        
        choice = input("\nChoose [1-2]: ").strip()
        if choice in engines:
            engine_code, engine_name = engines[choice]
            self.config.set('translation_engine', engine_code)
            self.config.save_config()
            self.setup_translator()  # Reinitialize translator
            print(f"✅ Translation engine changed to: {engine_name}")
        else:
            print("❌ Invalid choice")

    def manage_cache(self):
        """Manage cache - Always display in English"""
        if not self.cache:
            print("❌ Cache is not enabled")
            return
        
        while True:
            print("\n" + "="*40)
            print("💾 Cache Management")
            print("="*40)
            print("1. Show statistics")
            print("2. Clean old translations")
            print("3. Clear all translations")
            print("4. Back")
            
            choice = input("\nChoose [1-4]: ").strip()
            
            if choice == '1':
                stats = self.cache.get_cache_stats()
                print(f"\n📊 Cache Statistics:")
                print(f"Total translations: {stats.get('total_translations', 0)}")
                print(f"Total usage: {stats.get('total_usage', 0)}")
                print(f"Database size: {stats.get('database_size_mb', 0)} MB")
                
            elif choice == '2':
                days = input("Days to keep translations (default 30): ").strip()
                days = int(days) if days.isdigit() else 30
                deleted = self.cache.clean_old_entries(days)
                print(f"✅ Deleted {deleted} old translations")
                
            elif choice == '3':
                confirm = input("Are you sure you want to clear all translations? (y/N): ").strip().lower()
                if confirm == 'y':
                    if self.cache.clear_cache():
                        print("✅ All saved translations cleared")
                    else:
                        print("❌ Failed to clear cache")
                        
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice")

    def reset_settings(self):
        """Reset settings to defaults - Always display in English"""
        confirm = input("\n⚠️  Are you sure you want to reset all settings to defaults? (y/N): ").strip().lower()
        if confirm == 'y':
            self.config.reset_to_defaults()
            self.setup_translator()  # Reinitialize translator
            print("✅ Settings reset to defaults")
        else:
            print("❌ Operation cancelled")

def main():
    parser = argparse.ArgumentParser(description='Translate SRT subtitle files')
    parser.add_argument('input_file', nargs='?', help='Input SRT file path')
    parser.add_argument('-o', '--output', help='Output SRT file path')
    parser.add_argument('-l', '--lang', default='ar', help='Target language code (default: ar for Arabic)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run interactive mode')
    parser.add_argument('-a', '--all', action='store_true', help='Translate all SRT files in current directory')
    
    args = parser.parse_args()
    
    translator = SubtitleTranslator()
    
    if args.interactive:
        translator.interactive_mode()
    elif args.all:
        translator.translate_all_srt_files(".")
    elif args.input_file:
        translator.translate_srt_file(args.input_file, args.output, args.lang)
    else:
        # If no option is specified, run interactive mode
        translator.interactive_mode()

if __name__ == "__main__":
    # Run interactive mode by default
    import sys
    if len(sys.argv) == 1:
        # No arguments, run interactive mode
        translator = SubtitleTranslator()
        translator.interactive_mode()
    else:
        main()
