#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Progress Saver for Advanced Subtitle Translator
نظام حفظ التقدم لمترجم الترجمات المتقدم
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

class ProgressSaver:
    """نظام حفظ التقدم واستكمال الترجمة"""
    
    def __init__(self):
        self.progress_dir = Path("progress")
        self.progress_dir.mkdir(exist_ok=True)
        self.current_session = None
    
    def create_session(self, input_file, output_file, source_lang, target_lang, total_subtitles):
        """إنشاء جلسة ترجمة جديدة"""
        session_id = self._generate_session_id(input_file)
        
        session_data = {
            'session_id': session_id,
            'input_file': str(input_file),
            'output_file': str(output_file),
            'source_lang': source_lang,
            'target_lang': target_lang,
            'total_subtitles': total_subtitles,
            'completed_subtitles': 0,
            'translated_items': [],
            'status': 'in_progress',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'engine': 'google',
            'backup_created': False
        }
        
        self.current_session = session_data
        self._save_session(session_data)
        
        print(f"🔄 Created translation session: {session_id}")
        return session_id
    
    def save_progress(self, completed_count, translated_item=None):
        """حفظ التقدم الحالي"""
        if not self.current_session:
            return
        
        self.current_session['completed_subtitles'] = completed_count
        self.current_session['updated_at'] = datetime.now().isoformat()
        
        if translated_item:
            # حفظ النص المترجم
            item_data = {
                'index': len(self.current_session['translated_items']),
                'original': translated_item.get('original', ''),
                'translated': translated_item.get('translated', ''),
                'start_time': translated_item.get('start_time', ''),
                'end_time': translated_item.get('end_time', ''),
                'timestamp': datetime.now().isoformat()
            }
            self.current_session['translated_items'].append(item_data)
        
        self._save_session(self.current_session)
        
        # طباعة تقدم كل 10 ترجمات
        if completed_count % 10 == 0:
            progress_percent = (completed_count / self.current_session['total_subtitles']) * 100
            print(f"💾 Progress saved: {completed_count}/{self.current_session['total_subtitles']} ({progress_percent:.1f}%)")
    
    def complete_session(self):
        """إنهاء الجلسة بنجاح"""
        if not self.current_session:
            return
        
        self.current_session['status'] = 'completed'
        self.current_session['completed_at'] = datetime.now().isoformat()
        self._save_session(self.current_session)
        
        print(f"✅ Translation session completed successfully!")
        self.current_session = None
    
    def cancel_session(self):
        """إلغاء الجلسة"""
        if not self.current_session:
            return
        
        self.current_session['status'] = 'cancelled'
        self.current_session['cancelled_at'] = datetime.now().isoformat()
        self._save_session(self.current_session)
        
        print(f"❌ Translation session cancelled")
        self.current_session = None
    
    def find_incomplete_sessions(self):
        """البحث عن جلسات غير مكتملة"""
        incomplete_sessions = []
        
        for progress_file in self.progress_dir.glob("*.json"):
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                if session_data.get('status') == 'in_progress':
                    # التحقق من أن الملف المصدر ما زال موجود
                    if os.path.exists(session_data.get('input_file', '')):
                        incomplete_sessions.append(session_data)
                    else:
                        # حذف الجلسة إذا كان الملف المصدر محذوف
                        progress_file.unlink()
            
            except (json.JSONDecodeError, KeyError):
                # حذف الملفات التالفة
                progress_file.unlink()
        
        return incomplete_sessions
    
    def resume_session(self, session_data):
        """استكمال جلسة موجودة"""
        self.current_session = session_data
        self.current_session['resumed_at'] = datetime.now().isoformat()
        self._save_session(self.current_session)
        
        completed = session_data.get('completed_subtitles', 0)
        total = session_data.get('total_subtitles', 0)
        
        print(f"🔄 Resuming translation session...")
        print(f"📁 File: {Path(session_data['input_file']).name}")
        print(f"🌍 Languages: {session_data['source_lang']} → {session_data['target_lang']}")
        print(f"📊 Progress: {completed}/{total} ({(completed/total)*100:.1f}%)")
        
        return session_data
    
    def get_translated_items(self):
        """الحصول على العناصر المترجمة مسبقاً"""
        if not self.current_session:
            return []
        
        return self.current_session.get('translated_items', [])
    
    def get_completed_count(self):
        """الحصول على عدد الترجمات المكتملة"""
        if not self.current_session:
            return 0
        
        return self.current_session.get('completed_subtitles', 0)
    
    def cleanup_old_sessions(self, days=7):
        """تنظيف الجلسات القديمة"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        cleaned_count = 0
        
        for progress_file in self.progress_dir.glob("*.json"):
            try:
                file_time = progress_file.stat().st_mtime
                if file_time < cutoff_time:
                    progress_file.unlink()
                    cleaned_count += 1
            except:
                pass
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} old session files")
    
    def get_session_stats(self):
        """إحصائيات الجلسات"""
        total_sessions = 0
        completed_sessions = 0
        in_progress_sessions = 0
        
        for progress_file in self.progress_dir.glob("*.json"):
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                total_sessions += 1
                status = session_data.get('status', 'unknown')
                
                if status == 'completed':
                    completed_sessions += 1
                elif status == 'in_progress':
                    in_progress_sessions += 1
            
            except:
                pass
        
        return {
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'in_progress_sessions': in_progress_sessions,
            'success_rate': (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        }
    
    def _generate_session_id(self, input_file):
        """إنشاء معرف فريد للجلسة"""
        file_name = Path(input_file).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{file_name}_{timestamp}"
    
    def _save_session(self, session_data):
        """حفظ بيانات الجلسة"""
        session_file = self.progress_dir / f"{session_data['session_id']}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Warning: Could not save progress: {e}")
    
    def delete_session(self, session_id):
        """حذف جلسة محددة"""
        session_file = self.progress_dir / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()
            print(f"🗑️ Deleted session: {session_id}")
    
    def export_session(self, session_id, export_path):
        """تصدير جلسة للنسخ الاحتياطي"""
        session_file = self.progress_dir / f"{session_id}.json"
        if session_file.exists():
            import shutil
            shutil.copy2(session_file, export_path)
            print(f"📤 Exported session to: {export_path}")
            return True
        return False
