#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Localization system for Advanced Subtitle Translator
نظام التعريب لمترجم الترجمات المتقدم
"""

class LocalizationManager:
    """إدارة تعدد اللغات للواجهة"""
    
    def __init__(self, language='en'):
        self.language = language
        self.strings = self._load_strings()
    
    def _load_strings(self):
        """تحميل النصوص حسب اللغة المحددة"""
        
        if self.language == 'ar':
            return {
                # Main window
                'app_title': 'مترجم الترجمات المتقدم v2.0',
                
                # Tabs
                'tab_single_file': '📄 ملف واحد',
                'tab_batch_process': '📁 معالجة دفعية',
                'tab_settings': '⚙️ الإعدادات',
                'tab_statistics': '📊 الإحصائيات',
                
                # File Selection
                'file_selection': 'اختيار الملف',
                'input_file': 'الملف المدخل:',
                'output_file': 'ملف المخرج:',
                'browse': 'تصفح',
                'clear': 'مسح',
                'auto': 'تلقائي',
                
                # Language Detection
                'language_detection': 'كشف اللغة',
                'auto_detect_source': 'كشف لغة المصدر تلقائياً',
                'source_language': 'لغة المصدر:',
                'target_language': 'اللغة المستهدفة:',
                'detect_now': 'كشف الآن',
                'auto_detected': 'مكتشف تلقائياً',
                
                # Format Options
                'format_options': 'خيارات التنسيق',
                'input_format': 'تنسيق المدخل:',
                'output_format': 'تنسيق المخرج:',
                'auto_detect': 'كشف تلقائي',
                
                # Translation Options
                'translation_options': 'خيارات الترجمة',
                'engine': 'المحرك:',
                'create_backup': 'إنشاء نسخة احتياطية',
                'use_cache': 'استخدام التخزين المؤقت',
                
                # Progress
                'progress': 'التقدم',
                'ready': 'جاهز',
                'translating_subtitle': 'جاري ترجمة الترجمة',
                
                # Buttons
                'start_translation': '🚀 بدء الترجمة',
                'stop': '⏹ إيقاف',
                'preview': '👁 معاينة',
                'open_output_folder': '📁 فتح مجلد المخرج',
                
                # Batch Processing
                'files_to_translate': 'الملفات المراد ترجمتها',
                'file_name': 'اسم الملف',
                'format': 'التنسيق',
                'source': 'المصدر',
                'target': 'الهدف',
                'status': 'الحالة',
                'add_files': '➕ إضافة ملفات',
                'add_folder': '📁 إضافة مجلد',
                'remove_selected': '🗑 حذف المحدد',
                'clear_all': '🗑 مسح الكل',
                'start_batch_translation': '🚀 بدء الترجمة الدفعية',
                'batch_progress': 'تقدم المعالجة الدفعية',
                'ready_for_batch': 'جاهز للمعالجة الدفعية',
                
                # Settings
                'translation_settings': 'إعدادات الترجمة',
                'default_source_language': 'لغة المصدر الافتراضية:',
                'default_target_language': 'اللغة المستهدفة الافتراضية:',
                'default_translation_engine': 'محرك الترجمة الافتراضي:',
                'performance_settings': 'إعدادات الأداء',
                'delay_between_requests': 'التأخير بين الطلبات (ثانية):',
                'maximum_retries': 'الحد الأقصى للمحاولات:',
                'file_settings': 'إعدادات الملف',
                'create_backup_auto': 'إنشاء ملفات احتياطية تلقائياً',
                'enable_translation_cache': 'تفعيل تخزين الترجمة مؤقتاً',
                'output_file_suffix': 'لاحقة ملف المخرج:',
                'interface_settings': 'إعدادات الواجهة',
                'interface_language': 'لغة الواجهة:',
                'save_settings': '💾 حفظ الإعدادات',
                'reset_to_defaults': '🔄 إعادة تعيين للافتراضي',
                'open_config_file': '📁 فتح ملف الإعدادات',
                
                # Statistics
                'session_statistics': 'إحصائيات الجلسة',
                'cache_statistics': 'إحصائيات التخزين المؤقت',
                'refresh': '🔄 تحديث',
                'clear_cache': '🗑 مسح التخزين المؤقت',
                'export_stats': '📊 تصدير الإحصائيات',
                
                # Status Bar
                'files': 'الملفات',
                
                # Drag & Drop
                'drag_drop_area': '🎯 منطقة السحب والإفلات',
                'drag_files_here': '📁 اسحب ملفات الترجمة هنا (.srt, .ass, .vtt)\n💡 أو انقر هنا للتصفح',
                'ready_for_files': 'جاهز للملفات',
                
                # Messages
                'warning': 'تحذير',
                'error': 'خطأ',
                'success': 'نجح',
                'info': 'معلومة',
                'select_input_file_first': 'الرجاء اختيار ملف الإدخال أولاً',
                'file_loaded': 'تم تحميل الملف',
                'translation_started': 'بدأت الترجمة',
                'translation_completed': 'اكتملت الترجمة',
                'translation_stopped': 'توقفت الترجمة',
                'no_files_selected': 'لم يتم اختيار ملفات',
                
                # File types
                'all_subtitle_files': 'جميع ملفات الترجمة',
                'srt_files': 'ملفات SRT',
                'ass_files': 'ملفات ASS', 
                'vtt_files': 'ملفات VTT',
                'all_files': 'جميع الملفات',
                'select_subtitle_file': 'اختر ملف الترجمة',
                'save_subtitle_file': 'احفظ ملف الترجمة'
            }
        
        else:  # Default English
            return {
                # Main window
                'app_title': 'Advanced Subtitle Translator v2.0',
                
                # Tabs
                'tab_single_file': '📄 Single File',
                'tab_batch_process': '📁 Batch Process',
                'tab_settings': '⚙️ Settings',
                'tab_statistics': '📊 Statistics',
                
                # File Selection
                'file_selection': 'File Selection',
                'input_file': 'Input File:',
                'output_file': 'Output File:',
                'browse': 'Browse',
                'clear': 'Clear',
                'auto': 'Auto',
                
                # Language Detection
                'language_detection': 'Language Detection',
                'auto_detect_source': 'Auto-detect source language',
                'source_language': 'Source Language:',
                'target_language': 'Target Language:',
                'detect_now': 'Detect Now',
                'auto_detected': 'Auto-detected',
                
                # Format Options
                'format_options': 'Format Options',
                'input_format': 'Input Format:',
                'output_format': 'Output Format:',
                'auto_detect': 'Auto-detect',
                
                # Translation Options
                'translation_options': 'Translation Options',
                'engine': 'Engine:',
                'create_backup': 'Create backup',
                'use_cache': 'Use cache',
                
                # Progress
                'progress': 'Progress',
                'ready': 'Ready',
                'translating_subtitle': 'Translating subtitle',
                
                # Buttons
                'start_translation': '🚀 Start Translation',
                'stop': '⏹ Stop',
                'preview': '👁 Preview',
                'open_output_folder': '📁 Open Output Folder',
                
                # Batch Processing
                'files_to_translate': 'Files to Translate',
                'file_name': 'File Name',
                'format': 'Format',
                'source': 'Source',
                'target': 'Target',
                'status': 'Status',
                'add_files': '➕ Add Files',
                'add_folder': '📁 Add Folder',
                'remove_selected': '🗑 Remove Selected',
                'clear_all': '🗑 Clear All',
                'start_batch_translation': '🚀 Start Batch Translation',
                'batch_progress': 'Batch Progress',
                'ready_for_batch': 'Ready for batch processing',
                
                # Settings
                'translation_settings': 'Translation Settings',
                'default_source_language': 'Default Source Language:',
                'default_target_language': 'Default Target Language:',
                'default_translation_engine': 'Default Translation Engine:',
                'performance_settings': 'Performance Settings',
                'delay_between_requests': 'Delay between requests (seconds):',
                'maximum_retries': 'Maximum retries:',
                'file_settings': 'File Settings',
                'create_backup_auto': 'Create backup files automatically',
                'enable_translation_cache': 'Enable translation cache',
                'output_file_suffix': 'Output file suffix:',
                'interface_settings': 'Interface Settings',
                'interface_language': 'Interface Language:',
                'save_settings': '💾 Save Settings',
                'reset_to_defaults': '🔄 Reset to Defaults',
                'open_config_file': '📁 Open Config File',
                
                # Statistics
                'session_statistics': 'Session Statistics',
                'cache_statistics': 'Cache Statistics',
                'refresh': '🔄 Refresh',
                'clear_cache': '🗑 Clear Cache',
                'export_stats': '📊 Export Stats',
                
                # Status Bar
                'files': 'Files',
                
                # Drag & Drop
                'drag_drop_area': '🎯 Drag & Drop Area',
                'drag_files_here': '📁 Drag subtitle files here (.srt, .ass, .vtt)\n💡 or click here to browse',
                'ready_for_files': 'Ready for files',
                
                # Messages
                'warning': 'Warning',
                'error': 'Error',
                'success': 'Success',
                'info': 'Info',
                'select_input_file_first': 'Please select an input file first',
                'file_loaded': 'File loaded',
                'translation_started': 'Translation started',
                'translation_completed': 'Translation completed',
                'translation_stopped': 'Translation stopped',
                'no_files_selected': 'No files selected',
                
                # File types
                'all_subtitle_files': 'All Subtitle Files',
                'srt_files': 'SRT Files',
                'ass_files': 'ASS Files',
                'vtt_files': 'VTT Files',
                'all_files': 'All Files',
                'select_subtitle_file': 'Select Subtitle File',
                'save_subtitle_file': 'Save Subtitle File'
            }
    
    def get(self, key, default=None):
        """الحصول على النص المحلي"""
        return self.strings.get(key, default or key)
    
    def set_language(self, language):
        """تغيير اللغة"""
        self.language = language
        self.strings = self._load_strings()
    
    def get_available_languages(self):
        """الحصول على اللغات المتاحة"""
        return {
            'en': 'English',
            'ar': 'العربية'
        }
