#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام التخزين المؤقت للترجمات
Translation caching system
"""

import sqlite3
import hashlib
import os
import json
from datetime import datetime, timedelta

class TranslationCache:
    """نظام تخزين مؤقت للترجمات لتجنب إعادة الترجمة"""
    
    def __init__(self, db_path="translation_cache.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text_hash TEXT UNIQUE NOT NULL,
                    original_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    engine TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 1
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_text_hash ON translations(text_hash)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_languages ON translations(source_lang, target_lang)
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"خطأ في إنشاء قاعدة البيانات: {e}")
    
    def _generate_hash(self, text, source_lang, target_lang):
        """إنشاء hash فريد للنص واللغات"""
        content = f"{text.strip()}|{source_lang}|{target_lang}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get_cached_translation(self, text, source_lang, target_lang):
        """البحث عن ترجمة محفوظة"""
        if not text.strip():
            return None
            
        text_hash = self._generate_hash(text, source_lang, target_lang)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT translated_text FROM translations 
                WHERE text_hash = ? AND source_lang = ? AND target_lang = ?
            ''', (text_hash, source_lang, target_lang))
            
            result = cursor.fetchone()
            
            if result:
                # تحديث آخر استخدام وعداد الاستخدام
                cursor.execute('''
                    UPDATE translations 
                    SET last_used = CURRENT_TIMESTAMP, usage_count = usage_count + 1
                    WHERE text_hash = ?
                ''', (text_hash,))
                conn.commit()
                
                conn.close()
                return result[0]
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"خطأ في البحث في الذاكرة المؤقتة: {e}")
            return None
    
    def save_translation(self, original_text, translated_text, source_lang, target_lang, engine="google"):
        """حفظ ترجمة جديدة في الذاكرة المؤقتة"""
        if not original_text.strip() or not translated_text.strip():
            return False
            
        text_hash = self._generate_hash(original_text, source_lang, target_lang)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO translations 
                (text_hash, original_text, translated_text, source_lang, target_lang, engine)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (text_hash, original_text, translated_text, source_lang, target_lang, engine))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"خطأ في حفظ الترجمة: {e}")
            return False
    
    def get_cache_stats(self):
        """إحصائيات الذاكرة المؤقتة"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM translations')
            total_translations = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(usage_count) FROM translations')
            total_usage = cursor.fetchone()[0] or 0
            
            cursor.execute('''
                SELECT target_lang, COUNT(*) 
                FROM translations 
                GROUP BY target_lang 
                ORDER BY COUNT(*) DESC
            ''')
            language_stats = cursor.fetchall()
            
            # حساب حجم قاعدة البيانات
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            conn.close()
            
            return {
                'total_translations': total_translations,
                'total_usage': total_usage,
                'language_stats': language_stats,
                'database_size_mb': round(db_size / (1024 * 1024), 2),
                'cache_hit_potential': round((total_usage / max(total_translations, 1) - 1) * 100, 1)
            }
            
        except Exception as e:
            print(f"خطأ في حساب الإحصائيات: {e}")
            return {}
    
    def clean_old_entries(self, days_old=30):
        """تنظيف الترجمات القديمة"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            cursor.execute('''
                DELETE FROM translations 
                WHERE last_used < ? AND usage_count = 1
            ''', (cutoff_date,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deleted_count
            
        except Exception as e:
            print(f"خطأ في تنظيف الذاكرة المؤقتة: {e}")
            return 0
    
    def clear_cache(self):
        """مسح جميع الترجمات المحفوظة"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM translations')
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"خطأ في مسح الذاكرة المؤقتة: {e}")
            return False
