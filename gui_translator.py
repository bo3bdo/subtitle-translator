#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Subtitle Translator GUI
واجهة رسومية متقدمة لمترجم الترجمات
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from datetime import datetime
import queue
from pathlib import Path
import tkinter.dnd as tkdnd

# Import our modules
from translate_subtitles import SubtitleTranslator
from config import Config
from subtitle_formats import SubtitleFormatHandler
from language_detector import LanguageDetector
from localization import LocalizationManager

class SubtitleTranslatorGUI:
    """Advanced GUI for Subtitle Translator with drag & drop support"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Initialize components
        self.config = Config()
        self.translator = SubtitleTranslator()
        self.format_handler = SubtitleFormatHandler()
        self.language_detector = LanguageDetector()
        
        # Initialize localization
        ui_language = self.config.get('ui_language', 'en')
        self.localization = LocalizationManager(ui_language)
        
        # Setup window after localization is ready
        self.setup_window()
        
        # GUI state
        self.file_queue = queue.Queue()
        self.is_translating = False
        self.translation_thread = None
        self.dialog_open = False  # Prevent multiple dialogs
        
        # Setup GUI
        self.create_widgets()
        self.setup_drag_drop()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title(self.localization.get('app_title'))
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_translation_tab()
        self.create_batch_tab()
        self.create_settings_tab()
        self.create_statistics_tab()
        
        # Create status bar
        self.create_status_bar()
        
    def create_translation_tab(self):
        """Create single file translation tab"""
        # Translation tab
        self.translation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.translation_frame, text=self.localization.get('tab_single_file'))
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.translation_frame, text=self.localization.get('file_selection'), padding=10)
        file_frame.pack(fill='x', padx=10, pady=5)
        
        # Input file
        ttk.Label(file_frame, text=self.localization.get('input_file')).grid(row=0, column=0, sticky='w', pady=2)
        self.input_file_var = tk.StringVar()
        self.input_entry = ttk.Entry(file_frame, textvariable=self.input_file_var, width=50)
        self.input_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Button(file_frame, text=self.localization.get('browse'), command=self.browse_input_file).grid(row=0, column=2, padx=5, pady=2)
        ttk.Button(file_frame, text=self.localization.get('clear'), command=self.clear_input_file).grid(row=0, column=3, padx=5, pady=2)
        
        # Output file
        ttk.Label(file_frame, text=self.localization.get('output_file')).grid(row=1, column=0, sticky='w', pady=2)
        self.output_file_var = tk.StringVar()
        self.output_entry = ttk.Entry(file_frame, textvariable=self.output_file_var, width=50)
        self.output_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Button(file_frame, text=self.localization.get('browse'), command=self.browse_output_file).grid(row=1, column=2, padx=5, pady=2)
        ttk.Button(file_frame, text=self.localization.get('auto'), command=self.auto_output_file).grid(row=1, column=3, padx=5, pady=2)
        
        file_frame.columnconfigure(1, weight=1)
        
        # Language detection frame
        detection_frame = ttk.LabelFrame(self.translation_frame, text=self.localization.get('language_detection'), padding=10)
        detection_frame.pack(fill='x', padx=10, pady=5)
        
        # Auto-detect source language
        self.auto_detect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(detection_frame, text=self.localization.get('auto_detect_source'), 
                       variable=self.auto_detect_var, command=self.toggle_source_detection).pack(anchor='w')
        
        # Source language selection
        lang_frame = ttk.Frame(detection_frame)
        lang_frame.pack(fill='x', pady=5)
        
        ttk.Label(lang_frame, text=self.localization.get('source_language')).pack(side='left')
        self.source_lang_var = tk.StringVar(value='auto')
        self.source_combo = ttk.Combobox(lang_frame, textvariable=self.source_lang_var, 
                                        values=self.get_language_list(), state='disabled', width=15)
        self.source_combo.pack(side='left', padx=10)
        
        # Detect button
        self.detect_button = ttk.Button(lang_frame, text=self.localization.get('detect_now'), command=self.detect_language)
        self.detect_button.pack(side='left', padx=10)
        
        # Detection result
        self.detection_result = ttk.Label(lang_frame, text="", foreground='blue')
        self.detection_result.pack(side='left', padx=10)
        
        # Target language
        ttk.Label(lang_frame, text=self.localization.get('target_language')).pack(side='right')
        self.target_lang_var = tk.StringVar(value=self.config.get('default_target_language', 'ar'))
        self.target_combo = ttk.Combobox(lang_frame, textvariable=self.target_lang_var, 
                                        values=self.get_language_list(), width=15)
        self.target_combo.pack(side='right', padx=10)
        
        # Format selection frame
        format_frame = ttk.LabelFrame(self.translation_frame, text=self.localization.get('format_options'), padding=10)
        format_frame.pack(fill='x', padx=10, pady=5)
        
        # Input format detection
        ttk.Label(format_frame, text=self.localization.get('input_format')).grid(row=0, column=0, sticky='w')
        self.input_format_var = tk.StringVar(value=self.localization.get('auto_detect'))
        self.input_format_label = ttk.Label(format_frame, textvariable=self.input_format_var, foreground='green')
        self.input_format_label.grid(row=0, column=1, sticky='w', padx=10)
        
        # Output format selection
        ttk.Label(format_frame, text=self.localization.get('output_format')).grid(row=0, column=2, sticky='w', padx=(20,5))
        self.output_format_var = tk.StringVar(value='.srt')
        self.output_format_combo = ttk.Combobox(format_frame, textvariable=self.output_format_var, 
                                               values=['.srt', '.ass', '.vtt'], width=10)
        self.output_format_combo.grid(row=0, column=3, sticky='w', padx=10)
        
        # Translation options
        options_frame = ttk.LabelFrame(self.translation_frame, text=self.localization.get('translation_options'), padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        # Translation engine
        ttk.Label(options_frame, text=self.localization.get('engine')).grid(row=0, column=0, sticky='w')
        self.engine_var = tk.StringVar(value=self.config.get('translation_engine', 'google'))
        self.engine_combo = ttk.Combobox(options_frame, textvariable=self.engine_var, 
                                        values=['google', 'microsoft'], width=15)
        self.engine_combo.grid(row=0, column=1, sticky='w', padx=10)
        
        # Backup option
        self.backup_var = tk.BooleanVar(value=self.config.get('create_backup', True))
        ttk.Checkbutton(options_frame, text=self.localization.get('create_backup'), variable=self.backup_var).grid(row=0, column=2, padx=20)
        
        # Cache option
        self.cache_var = tk.BooleanVar(value=self.config.get('cache_enabled', True))
        ttk.Checkbutton(options_frame, text=self.localization.get('use_cache'), variable=self.cache_var).grid(row=0, column=3, padx=20)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(self.translation_frame, text=self.localization.get('progress'), padding=10)
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', pady=5)
        
        # Progress label
        self.progress_label = ttk.Label(progress_frame, text=self.localization.get('ready'))
        self.progress_label.pack()
        
        # Buttons frame
        button_frame = ttk.Frame(self.translation_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        # Main buttons
        self.translate_button = ttk.Button(button_frame, text=self.localization.get('start_translation'), 
                                          command=self.start_translation, style='Accent.TButton')
        self.translate_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(button_frame, text=self.localization.get('stop'), 
                                     command=self.stop_translation, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        # Preview button
        ttk.Button(button_frame, text=self.localization.get('preview'), command=self.preview_file).pack(side='left', padx=5)
        
        # Open output folder
        ttk.Button(button_frame, text=self.localization.get('open_output_folder'), 
                  command=self.open_output_folder).pack(side='right', padx=5)
        
    def create_batch_tab(self):
        """Create batch translation tab"""
        self.batch_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.batch_frame, text=self.localization.get('tab_batch_process'))
        
        # File list frame
        list_frame = ttk.LabelFrame(self.batch_frame, text=self.localization.get('files_to_translate'), padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # File list with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill='both', expand=True)
        
        # Create treeview for file list
        columns = ('Name', 'Format', 'Source Lang', 'Target Lang', 'Status')
        self.file_tree = ttk.Treeview(list_container, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.file_tree.heading('Name', text=self.localization.get('file_name'))
        self.file_tree.heading('Format', text=self.localization.get('format'))
        self.file_tree.heading('Source Lang', text=self.localization.get('source'))
        self.file_tree.heading('Target Lang', text=self.localization.get('target'))
        self.file_tree.heading('Status', text=self.localization.get('status'))
        
        self.file_tree.column('Name', width=300)
        self.file_tree.column('Format', width=80)
        self.file_tree.column('Source Lang', width=100)
        self.file_tree.column('Target Lang', width=100)
        self.file_tree.column('Status', width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=self.file_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_container, orient='horizontal', command=self.file_tree.xview)
        self.file_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.file_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        list_container.grid_rowconfigure(0, weight=1)
        list_container.grid_columnconfigure(0, weight=1)
        
        # Batch controls
        batch_controls = ttk.Frame(self.batch_frame)
        batch_controls.pack(fill='x', padx=10, pady=5)
        
        # Add files buttons
        ttk.Button(batch_controls, text=self.localization.get('add_files'), command=self.add_batch_files).pack(side='left', padx=5)
        ttk.Button(batch_controls, text=self.localization.get('add_folder'), command=self.add_batch_folder).pack(side='left', padx=5)
        ttk.Button(batch_controls, text=self.localization.get('remove_selected'), command=self.remove_selected_files).pack(side='left', padx=5)
        ttk.Button(batch_controls, text=self.localization.get('clear_all'), command=self.clear_all_files).pack(side='left', padx=5)
        
        # Batch translation button
        ttk.Button(batch_controls, text=self.localization.get('start_batch_translation'), 
                  command=self.start_batch_translation, style='Accent.TButton').pack(side='right', padx=5)
        
        # Batch progress
        batch_progress_frame = ttk.LabelFrame(self.batch_frame, text=self.localization.get('batch_progress'), padding=10)
        batch_progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.batch_progress_var = tk.DoubleVar()
        self.batch_progress_bar = ttk.Progressbar(batch_progress_frame, variable=self.batch_progress_var, maximum=100)
        self.batch_progress_bar.pack(fill='x', pady=5)
        
        self.batch_progress_label = ttk.Label(batch_progress_frame, text=self.localization.get('ready_for_batch'))
        self.batch_progress_label.pack()
        
    def create_settings_tab(self):
        """Create settings tab"""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text=self.localization.get('tab_settings'))
        
        # Create scrollable frame for settings
        canvas = tk.Canvas(self.settings_frame)
        scrollbar = ttk.Scrollbar(self.settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Translation settings
        trans_settings = ttk.LabelFrame(scrollable_frame, text=self.localization.get('translation_settings'), padding=10)
        trans_settings.pack(fill='x', padx=10, pady=5)
        
        # Default languages
        ttk.Label(trans_settings, text=self.localization.get('default_source_language')).grid(row=0, column=0, sticky='w', pady=2)
        self.default_source_var = tk.StringVar(value=self.config.get('default_source_language', 'en'))
        ttk.Combobox(trans_settings, textvariable=self.default_source_var, 
                    values=self.get_language_list(), width=15).grid(row=0, column=1, sticky='w', padx=10, pady=2)
        
        ttk.Label(trans_settings, text=self.localization.get('default_target_language')).grid(row=1, column=0, sticky='w', pady=2)
        self.default_target_var = tk.StringVar(value=self.config.get('default_target_language', 'ar'))
        ttk.Combobox(trans_settings, textvariable=self.default_target_var, 
                    values=self.get_language_list(), width=15).grid(row=1, column=1, sticky='w', padx=10, pady=2)
        
        # Engine settings
        ttk.Label(trans_settings, text=self.localization.get('default_translation_engine')).grid(row=2, column=0, sticky='w', pady=2)
        self.default_engine_var = tk.StringVar(value=self.config.get('translation_engine', 'google'))
        ttk.Combobox(trans_settings, textvariable=self.default_engine_var, 
                    values=['google', 'microsoft'], width=15).grid(row=2, column=1, sticky='w', padx=10, pady=2)
        
        # Performance settings
        perf_settings = ttk.LabelFrame(scrollable_frame, text=self.localization.get('performance_settings'), padding=10)
        perf_settings.pack(fill='x', padx=10, pady=5)
        
        # Delay between requests
        ttk.Label(perf_settings, text=self.localization.get('delay_between_requests')).grid(row=0, column=0, sticky='w', pady=2)
        self.delay_var = tk.DoubleVar(value=self.config.get('delay_between_requests', 0.1))
        delay_spin = tk.Spinbox(perf_settings, from_=0.0, to=5.0, increment=0.1, textvariable=self.delay_var, width=10)
        delay_spin.grid(row=0, column=1, sticky='w', padx=10, pady=2)
        
        # Max retries
        ttk.Label(perf_settings, text=self.localization.get('maximum_retries')).grid(row=1, column=0, sticky='w', pady=2)
        self.retries_var = tk.IntVar(value=self.config.get('max_retries', 3))
        retry_spin = tk.Spinbox(perf_settings, from_=1, to=10, textvariable=self.retries_var, width=10)
        retry_spin.grid(row=1, column=1, sticky='w', padx=10, pady=2)
        
        # File settings
        file_settings = ttk.LabelFrame(scrollable_frame, text=self.localization.get('file_settings'), padding=10)
        file_settings.pack(fill='x', padx=10, pady=5)
        
        # Backup settings
        self.backup_setting_var = tk.BooleanVar(value=self.config.get('create_backup', True))
        ttk.Checkbutton(file_settings, text=self.localization.get('create_backup_auto'), 
                       variable=self.backup_setting_var).grid(row=0, column=0, sticky='w', pady=2)
        
        # Cache settings
        self.cache_setting_var = tk.BooleanVar(value=self.config.get('cache_enabled', True))
        ttk.Checkbutton(file_settings, text=self.localization.get('enable_translation_cache'), 
                       variable=self.cache_setting_var).grid(row=1, column=0, sticky='w', pady=2)
        
        # Output suffix
        ttk.Label(file_settings, text=self.localization.get('output_file_suffix')).grid(row=2, column=0, sticky='w', pady=2)
        self.suffix_var = tk.StringVar(value=self.config.get('output_suffix', '_arabic'))
        ttk.Entry(file_settings, textvariable=self.suffix_var, width=15).grid(row=2, column=1, sticky='w', padx=10, pady=2)
        
        # UI settings
        ui_settings = ttk.LabelFrame(scrollable_frame, text=self.localization.get('interface_settings'), padding=10)
        ui_settings.pack(fill='x', padx=10, pady=5)
        
        # UI language
        ttk.Label(ui_settings, text=self.localization.get('interface_language')).grid(row=0, column=0, sticky='w', pady=2)
        self.ui_lang_var = tk.StringVar(value=self.config.get('ui_language', 'en'))
        ui_lang_combo = ttk.Combobox(ui_settings, textvariable=self.ui_lang_var, 
                    values=['en', 'ar'], width=15)
        ui_lang_combo.grid(row=0, column=1, sticky='w', padx=10, pady=2)
        
        # Language display mapping
        lang_display = {'en': 'English', 'ar': 'العربية'}
        ui_lang_combo.configure(values=[f"{k} - {v}" for k, v in lang_display.items()])
        current_lang = self.config.get('ui_language', 'en')
        ui_lang_combo.set(f"{current_lang} - {lang_display.get(current_lang, 'English')}")
        
        # Bind language change event
        def on_lang_change(event):
            selected = ui_lang_combo.get()
            lang_code = selected.split(' - ')[0]
            self.ui_lang_var.set(lang_code)
        
        ui_lang_combo.bind('<<ComboboxSelected>>', on_lang_change)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill='x', padx=10, pady=20)
        
        ttk.Button(button_frame, text=self.localization.get('save_settings'), command=self.save_settings).pack(side='left', padx=5)
        ttk.Button(button_frame, text=self.localization.get('reset_to_defaults'), command=self.reset_settings).pack(side='left', padx=5)
        ttk.Button(button_frame, text=self.localization.get('open_config_file'), command=self.open_config_file).pack(side='right', padx=5)
        
    def create_statistics_tab(self):
        """Create statistics tab"""
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text=self.localization.get('tab_statistics'))
        
        # Session stats
        session_frame = ttk.LabelFrame(self.stats_frame, text=self.localization.get('session_statistics'), padding=10)
        session_frame.pack(fill='x', padx=10, pady=5)
        
        # Create text widget for stats
        self.stats_text = scrolledtext.ScrolledText(session_frame, height=8, state='disabled')
        self.stats_text.pack(fill='both', expand=True)
        
        # Cache stats
        cache_frame = ttk.LabelFrame(self.stats_frame, text=self.localization.get('cache_statistics'), padding=10)
        cache_frame.pack(fill='x', padx=10, pady=5)
        
        self.cache_stats_text = scrolledtext.ScrolledText(cache_frame, height=6, state='disabled')
        self.cache_stats_text.pack(fill='both', expand=True)
        
        # Control buttons
        stats_buttons = ttk.Frame(self.stats_frame)
        stats_buttons.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(stats_buttons, text=self.localization.get('refresh'), command=self.refresh_stats).pack(side='left', padx=5)
        ttk.Button(stats_buttons, text=self.localization.get('clear_cache'), command=self.clear_cache).pack(side='left', padx=5)
        ttk.Button(stats_buttons, text=self.localization.get('export_stats'), command=self.export_stats).pack(side='right', padx=5)
        ttk.Button(stats_buttons, text="📊 Export Stats", command=self.export_stats).pack(side='right', padx=5)
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill='x', side='bottom')
        
        # Status label
        self.status_label = ttk.Label(self.status_frame, text=self.localization.get('ready'), relief='sunken')
        self.status_label.pack(side='left', fill='x', expand=True, padx=2, pady=2)
        
        # File count label
        self.file_count_label = ttk.Label(self.status_frame, text=f"{self.localization.get('files')}: 0", relief='sunken')
        self.file_count_label.pack(side='right', padx=2, pady=2)
        
    def setup_drag_drop(self):
        """Setup drag and drop functionality using tkinter's built-in support"""
        # Create a simple drag and drop area
        self.create_drop_area()
        
        # No need to bind events to main window or input entry
        # This prevents the flickering issue
    
    def create_drop_area(self):
        """Create a visual drop area"""
        self.drop_frame = ttk.LabelFrame(self.translation_frame, text=self.localization.get('drag_drop_area'), padding=20)
        self.drop_frame.pack(fill='x', padx=10, pady=10)
        
        # Create a more attractive drop area
        drop_container = ttk.Frame(self.drop_frame)
        drop_container.pack(fill='x', expand=True)
        
        self.drop_label = ttk.Label(drop_container, 
                                   text=self.localization.get('drag_files_here'),
                                   justify='center',
                                   foreground='#666666',
                                   font=('Arial', 10),
                                   cursor='hand2')  # Add hand cursor to indicate clickable
        self.drop_label.pack(expand=True, pady=10)
        
        # Add visual feedback frame
        self.drop_visual_frame = ttk.Frame(drop_container, relief='solid', borderwidth=2)
        self.drop_visual_frame.pack(fill='x', pady=5, padx=20)
        
        # Status label for drop feedback
        self.drop_status = ttk.Label(self.drop_visual_frame, text=self.localization.get('ready_for_files'), 
                                    foreground='green', font=('Arial', 8),
                                    cursor='hand2')  # Add hand cursor
        self.drop_status.pack(pady=5)
        
        # Make the drop area interactive - only bind to specific elements
        self.bind_drop_events(self.drop_label)
        self.bind_drop_events(self.drop_visual_frame)
        
        # Add click to browse functionality only for specific areas
        self.drop_label.bind('<Button-1>', self.on_drop_area_click)
        self.drop_visual_frame.bind('<Button-1>', self.on_drop_area_click)
    
    def on_drop_area_click(self, event):
        """Handle click on drop area specifically"""
        self.browse_input_file()
    
    def bind_drop_events(self, widget):
        """Bind drop events to a widget - simplified to avoid hover flickering"""
        # Only bind to specific drop areas, not all widgets
        if widget in [self.drop_label, self.drop_visual_frame]:
            widget.bind('<Enter>', self.on_enter_drop_widget)
            widget.bind('<Leave>', self.on_leave_drop_widget)
    
    def on_enter_drop_widget(self, event):
        """Handle mouse enter drop widget - less aggressive styling"""
        if hasattr(event.widget, 'config'):
            try:
                # Only change background color slightly
                if event.widget == self.drop_label:
                    event.widget.config(foreground='#0066cc')
                elif event.widget == self.drop_visual_frame:
                    event.widget.config(relief='solid', borderwidth=1)
            except:
                pass
    
    def on_leave_drop_widget(self, event):
        """Handle mouse leave drop widget - restore original styling"""
        if hasattr(event.widget, 'config'):
            try:
                # Restore original colors
                if event.widget == self.drop_label:
                    # Check if file is loaded to determine color
                    if self.input_file_var.get():
                        event.widget.config(foreground='#0066cc')
                    else:
                        event.widget.config(foreground='#666666')
                elif event.widget == self.drop_visual_frame:
                    event.widget.config(relief='solid', borderwidth=2)
            except:
                pass
    
    # Simpler drag and drop using file association
    def setup_file_associations(self):
        """Setup file associations for drag and drop"""
        # This would work with external file associations
        # For now, we'll use the browse button as primary method
        pass
    
    def handle_dropped_files(self, files):
        """Handle files dropped onto the application"""
        if not files:
            return
            
        # Check if we're in single file mode or batch mode
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 0:  # Single file tab
            # Take the first file for single file translation
            if files:
                self.input_file_var.set(files[0])
                self.auto_output_file()
                self.detect_input_format()
                self.update_status(f"File loaded: {os.path.basename(files[0])}")
        else:  # Batch tab
            # Add all files to batch
            for file_path in files:
                if self.is_subtitle_file(file_path):
                    self.add_file_to_batch(file_path)
    
    def is_subtitle_file(self, file_path):
        """Check if file is a supported subtitle file"""
        subtitle_extensions = ['.srt', '.ass', '.vtt']
        return any(file_path.lower().endswith(ext) for ext in subtitle_extensions)
                
    def get_language_list(self):
        """Get list of supported languages"""
        languages = [
            'auto', 'ar', 'en', 'fr', 'es', 'de', 'it', 'ru', 'ja', 'ko', 'zh', 'pt', 'nl', 'sv', 'tr'
        ]
        return languages
    
    # File Management Methods
    def browse_input_file(self):
        """Browse for input file"""
        # Prevent multiple dialogs from opening
        if self.dialog_open:
            return
        
        self.dialog_open = True
        
        try:
            filetypes = [
                (self.localization.get('all_subtitle_files'), "*.srt;*.ass;*.vtt"),
                (self.localization.get('srt_files'), "*.srt"),
                (self.localization.get('ass_files'), "*.ass"), 
                (self.localization.get('vtt_files'), "*.vtt"),
                (self.localization.get('all_files'), "*.*")
            ]
            
            filename = filedialog.askopenfilename(
                title=self.localization.get('select_subtitle_file'),
                filetypes=filetypes,
                parent=self.root  # Set parent to keep dialog modal
            )
            
            if filename:
                self.input_file_var.set(filename)
                self.auto_output_file()
                self.detect_input_format()
                self.update_status(f"{self.localization.get('file_loaded')}: {os.path.basename(filename)}")
                
                # Update drop area status
                self.drop_status.config(text=f"✅ {self.localization.get('file_loaded')}: {os.path.basename(filename)}", 
                                       foreground='green')
                self.drop_label.config(text=f"📄 {os.path.basename(filename)}\n💡 {self.localization.get('browse')}",
                                      foreground='#0066cc')
        finally:
            self.dialog_open = False
    
    def browse_output_file(self):
        """Browse for output file"""
        if self.dialog_open:
            return
            
        if not self.input_file_var.get():
            messagebox.showwarning("Warning", "Please select an input file first", parent=self.root)
            return
        
        self.dialog_open = True
        
        try:
            filetypes = [
                ("SRT Files", "*.srt"),
                ("ASS Files", "*.ass"),
                ("VTT Files", "*.vtt"),
                ("All Files", "*.*")
            ]
            
            filename = filedialog.asksaveasfilename(
                title="Save Translated File As",
                filetypes=filetypes,
                defaultextension=self.output_format_var.get(),
                parent=self.root
            )
            
            if filename:
                self.output_file_var.set(filename)
        finally:
            self.dialog_open = False
    
    def auto_output_file(self):
        """Auto-generate output file name"""
        input_file = self.input_file_var.get()
        if not input_file:
            return
            
        input_path = Path(input_file)
        suffix = self.config.get('output_suffix', '_translated')
        output_ext = self.output_format_var.get()
        
        output_name = f"{input_path.stem}{suffix}{output_ext}"
        output_path = input_path.parent / output_name
        
        self.output_file_var.set(str(output_path))
    
    def clear_input_file(self):
        """Clear input file selection"""
        self.input_file_var.set("")
        self.output_file_var.set("")
        self.input_format_var.set("Auto-detect")
        self.detection_result.config(text="")
        self.update_status("Ready")
        
        # Reset drop area
        self.drop_status.config(text="Ready for files", foreground='green')
        self.drop_label.config(text="📁 Drag subtitle files here (.srt, .ass, .vtt)\n💡 or click here to browse",
                              foreground='#666666')
    
    def detect_input_format(self):
        """Detect input file format"""
        input_file = self.input_file_var.get()
        if not input_file:
            return
            
        try:
            format_type = self.format_handler.detect_format(input_file)
            if format_type:
                self.input_format_var.set(format_type.upper())
            else:
                self.input_format_var.set("Unknown")
        except Exception as e:
            print(f"Error detecting format: {e}")
            self.input_format_var.set("Error")
    
    # Language Detection Methods
    def toggle_source_detection(self):
        """Toggle auto language detection"""
        if self.auto_detect_var.get():
            self.source_combo.config(state='disabled')
            self.source_lang_var.set('auto')
        else:
            self.source_combo.config(state='normal')
    
    def detect_language(self):
        """Detect language of input file"""
        input_file = self.input_file_var.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showwarning("Warning", "Please select a valid input file first")
            return
            
        try:
            # Read sample text from file
            subtitles = self.format_handler.read_subtitles(input_file)
            if not subtitles:
                self.detection_result.config(text="No text found", foreground='red')
                return
                
            # Get sample text (first few subtitles)
            sample_text = " ".join([sub.get('text', '') for sub in subtitles[:5]])
            
            # Detect language
            detected_lang = self.language_detector.detect_language(sample_text)
            
            if detected_lang and detected_lang != 'unknown':
                self.detection_result.config(text=f"Detected: {detected_lang}", foreground='green')
                if not self.auto_detect_var.get():
                    self.source_lang_var.set(detected_lang)
            else:
                self.detection_result.config(text="Could not detect", foreground='orange')
                
        except Exception as e:
            print(f"Language detection error: {e}")
            self.detection_result.config(text="Detection failed", foreground='red')
    
    # Translation Methods
    def start_translation(self):
        """Start single file translation"""
        print("🚀 Starting translation...")
        
        # Validate inputs
        if not self.validate_translation_inputs():
            print("❌ Validation failed")
            return
            
        print("✅ Validation passed")
        
        # Disable controls
        self.set_translation_controls(False)
        print(f"🔧 Controls disabled, is_translating: {self.is_translating}")
        
        # Start translation in separate thread
        self.translation_thread = threading.Thread(target=self.translate_file_worker)
        self.translation_thread.daemon = True
        self.translation_thread.start()
        print("🧵 Translation thread started")
    
    def validate_translation_inputs(self):
        """Validate translation inputs"""
        input_file = self.input_file_var.get().strip()
        output_file = self.output_file_var.get().strip()
        
        print(f"🔍 Validating inputs:")
        print(f"   Input file: '{input_file}'")
        print(f"   Output file: '{output_file}'")
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file using the Browse button or drag & drop")
            return False
            
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file does not exist:\n{input_file}")
            return False
            
        # Check if it's a supported subtitle file
        supported_extensions = ['.srt', '.ass', '.vtt']
        file_ext = os.path.splitext(input_file)[1].lower()
        if file_ext not in supported_extensions:
            messagebox.showerror("Error", f"Unsupported file format: {file_ext}\nSupported formats: {', '.join(supported_extensions)}")
            return False
            
        if not output_file:
            # Auto-generate output file if not specified
            print("📁 Auto-generating output file...")
            self.auto_output_file()
            output_file = self.output_file_var.get()
            print(f"   Generated output: '{output_file}'")
            
        if not output_file:
            messagebox.showerror("Error", "Could not determine output file path")
            return False
            
        # Check if source and target languages are the same
        source_lang = self.source_lang_var.get()
        target_lang = self.target_lang_var.get()
        
        print(f"🌍 Languages: {source_lang} → {target_lang}")
        
        if source_lang == target_lang and source_lang != 'auto':
            result = messagebox.askyesno("Warning", 
                f"Source and target languages are the same ({source_lang}).\nContinue anyway?")
            if not result:
                return False
        
        print("✅ All inputs valid")
        return True
    
    def translate_file_worker(self):
        """Worker thread for file translation"""
        print("📝 Translation worker started")
        print(f"🔍 is_translating: {self.is_translating}")
        
        try:
            input_file = self.input_file_var.get()
            output_file = self.output_file_var.get()
            source_lang = self.source_lang_var.get()
            target_lang = self.target_lang_var.get()
            
            print(f"📁 Input: {input_file}")
            print(f"📁 Output: {output_file}")
            print(f"🌍 Languages: {source_lang} → {target_lang}")
            
            # Update progress
            self.update_progress(0, "Initializing translation...")
            
            # Configure translator
            self.translator.config.set('translation_engine', self.engine_var.get())
            self.translator.config.set('cache_enabled', self.cache_var.get())
            self.translator.config.set('create_backup', self.backup_var.get())
            
            # Read subtitles
            self.update_progress(10, "Reading input file...")
            subtitles = self.format_handler.read_subtitles(input_file)
            
            if not subtitles:
                raise Exception("No subtitles found in input file")
            
            print(f"📖 Found {len(subtitles)} subtitles")
            total_subtitles = len(subtitles)
            
            # Auto-detect language if needed
            if source_lang == 'auto':
                self.update_progress(20, "Detecting language...")
                sample_text = " ".join([sub.get('text', '') for sub in subtitles[:5]])
                detected_lang = self.language_detector.detect_language(sample_text)
                source_lang = detected_lang if detected_lang != 'unknown' else 'en'
                
                # Update UI
                self.root.after(0, lambda: self.detection_result.config(
                    text=f"Auto-detected: {source_lang}", foreground='blue'))
            
            # Set source language in translator config
            self.translator.config.set('default_source_language', source_lang)
            print(f"🔧 Set source language to: {source_lang}")
            
            # Translate subtitles
            translated_subtitles = []
            for i, subtitle in enumerate(subtitles):
                if not self.is_translating:
                    print("⏹ Translation stopped by user")
                    break
                    
                progress = 20 + (i / total_subtitles) * 70
                self.update_progress(progress, f"Translating subtitle {i+1}/{total_subtitles}...")
                
                text = subtitle.get('text', '')
                if text.strip():
                    translated_text = self.translator.translate_text(text, target_lang)
                    subtitle['text'] = translated_text
                    print(f"✅ Translated: '{text[:50]}...' → '{translated_text[:50]}...'")
                
                translated_subtitles.append(subtitle)
            
            if self.is_translating:
                # Write output file
                self.update_progress(95, "Writing output file...")
                self.format_handler.write_subtitles(translated_subtitles, output_file, 
                                                  self.output_format_var.get())
                
                print(f"💾 Output file written: {output_file}")
                self.update_progress(100, "Translation completed successfully!")
                
                # Show success message
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success", f"Translation completed!\nOutput: {os.path.basename(output_file)}"))
            else:
                print("⏹ Translation was stopped")
                self.root.after(0, lambda: self.update_progress(0, "Translation stopped by user"))
                
        except Exception as e:
            error_msg = f"Translation failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, lambda: self.update_progress(0, "Translation failed"))
        finally:
            print("🔄 Re-enabling controls")
            # Re-enable controls
            self.root.after(0, lambda: self.set_translation_controls(True))
    
    def stop_translation(self):
        """Stop ongoing translation"""
        self.is_translating = False
        self.update_status("Stopping translation...")
    
    def set_translation_controls(self, enabled):
        """Enable/disable translation controls"""
        self.is_translating = not enabled  # Fix: is_translating should be opposite of enabled
        state = 'normal' if enabled else 'disabled'
        
        self.translate_button.config(state=state)
        self.stop_button.config(state='disabled' if enabled else 'normal')
        
        # Also disable input controls during translation
        controls = [self.input_entry, self.output_entry, self.source_combo, 
                   self.target_combo, self.engine_combo]
        for control in controls:
            try:
                control.config(state=state)
            except:
                pass
    
    def update_progress(self, value, text=""):
        """Update progress bar and label"""
        self.progress_var.set(value)
        if text:
            self.progress_label.config(text=text)
        self.root.update_idletasks()
    
    # Batch Processing Methods
    def add_batch_files(self):
        """Add files to batch processing"""
        filetypes = [
            ("All Subtitle Files", "*.srt;*.ass;*.vtt"),
            ("SRT Files", "*.srt"),
            ("ASS Files", "*.ass"),
            ("VTT Files", "*.vtt"),
            ("All Files", "*.*")
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Select Subtitle Files",
            filetypes=filetypes
        )
        
        for filename in filenames:
            self.add_file_to_batch(filename)
    
    def add_batch_folder(self):
        """Add all subtitle files from a folder"""
        folder = filedialog.askdirectory(title="Select Folder with Subtitle Files")
        if folder:
            self.add_directory_to_batch(folder)
    
    def add_file_to_batch(self, file_path):
        """Add a file to the batch list"""
        if not os.path.exists(file_path):
            return
            
        # Check if file already exists in list
        for item in self.file_tree.get_children():
            if self.file_tree.item(item, 'values')[0] == os.path.basename(file_path):
                return  # File already in list
        
        # Detect format
        format_type = self.format_handler.detect_format(file_path)
        if not format_type:
            return  # Unsupported format
        
        # Add to tree
        filename = os.path.basename(file_path)
        source_lang = self.default_source_var.get()
        target_lang = self.default_target_var.get()
        
        self.file_tree.insert('', 'end', values=(
            filename, format_type.upper(), source_lang, target_lang, 'Ready'
        ), tags=(file_path,))
        
        self.update_file_count()
    
    def add_directory_to_batch(self, directory):
        """Add all subtitle files from directory"""
        subtitle_extensions = ['.srt', '.ass', '.vtt']
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in subtitle_extensions):
                    file_path = os.path.join(root, file)
                    self.add_file_to_batch(file_path)
    
    def remove_selected_files(self):
        """Remove selected files from batch"""
        selection = self.file_tree.selection()
        for item in selection:
            self.file_tree.delete(item)
        self.update_file_count()
    
    def clear_all_files(self):
        """Clear all files from batch"""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.update_file_count()
    
    def start_batch_translation(self):
        """Start batch translation"""
        items = self.file_tree.get_children()
        if not items:
            messagebox.showwarning("Warning", "No files to translate")
            return
        
        # Start batch translation in separate thread
        self.batch_thread = threading.Thread(target=self.batch_translation_worker)
        self.batch_thread.daemon = True
        self.batch_thread.start()
    
    def batch_translation_worker(self):
        """Worker thread for batch translation"""
        items = self.file_tree.get_children()
        total_files = len(items)
        
        try:
            for i, item in enumerate(items):
                if not self.is_translating:
                    break
                
                # Get file info
                values = self.file_tree.item(item, 'values')
                filename = values[0]
                source_lang = values[2]
                target_lang = values[3]
                
                # Get full path from tags
                file_path = self.file_tree.item(item, 'tags')[0]
                
                # Update status
                self.root.after(0, lambda i=item: self.file_tree.item(
                    i, values=(*values[:4], 'Translating...')))
                
                progress = (i / total_files) * 100
                self.root.after(0, lambda p=progress: self.batch_progress_var.set(p))
                self.root.after(0, lambda f=filename: self.batch_progress_label.config(
                    text=f"Translating: {f}"))
                
                try:
                    # Generate output path
                    input_path = Path(file_path)
                    suffix = self.config.get('output_suffix', '_translated')
                    output_ext = self.output_format_var.get()
                    output_name = f"{input_path.stem}{suffix}{output_ext}"
                    output_path = input_path.parent / output_name
                    
                    # Translate file
                    subtitles = self.format_handler.read_subtitles(file_path)
                    
                    if source_lang == 'auto':
                        sample_text = " ".join([sub.get('text', '') for sub in subtitles[:5]])
                        detected_lang = self.language_detector.detect_language(sample_text)
                        source_lang = detected_lang if detected_lang != 'unknown' else 'en'
                    
                    for subtitle in subtitles:
                        text = subtitle.get('text', '')
                        if text.strip():
                            translated_text = self.translator.translate_text(text, source_lang, target_lang)
                            subtitle['text'] = translated_text
                    
                    # Write output
                    self.format_handler.write_subtitles(subtitles, str(output_path), output_ext)
                    
                    # Update status to completed
                    self.root.after(0, lambda i=item: self.file_tree.item(
                        i, values=(*values[:4], 'Completed')))
                    
                except Exception as e:
                    print(f"Error translating {filename}: {e}")
                    self.root.after(0, lambda i=item: self.file_tree.item(
                        i, values=(*values[:4], 'Failed')))
            
            if self.is_translating:
                self.root.after(0, lambda: self.batch_progress_var.set(100))
                self.root.after(0, lambda: self.batch_progress_label.config(text="Batch translation completed!"))
                self.root.after(0, lambda: messagebox.showinfo("Success", "Batch translation completed!"))
            
        except Exception as e:
            error_msg = f"Batch translation failed: {str(e)}"
            print(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        finally:
            self.is_translating = False
    
    def update_file_count(self):
        """Update file count in status bar"""
        count = len(self.file_tree.get_children())
        self.file_count_label.config(text=f"Files: {count}")
    
    # Preview and Utility Methods
    def preview_file(self):
        """Preview input file content"""
        input_file = self.input_file_var.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showwarning("Warning", "Please select a valid input file first")
            return
        
        try:
            subtitles = self.format_handler.read_subtitles(input_file)
            if not subtitles:
                messagebox.showinfo("Info", "No subtitles found in file")
                return
            
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"Preview: {os.path.basename(input_file)}")
            preview_window.geometry("600x400")
            
            # Preview text
            preview_text = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
            preview_text.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Show first 10 subtitles
            for i, sub in enumerate(subtitles[:10]):
                start_time = sub.get('start', 'Unknown')
                end_time = sub.get('end', 'Unknown')
                text = sub.get('text', '')
                
                preview_text.insert(tk.END, f"{i+1}. [{start_time} --> {end_time}]\n")
                preview_text.insert(tk.END, f"{text}\n\n")
            
            if len(subtitles) > 10:
                preview_text.insert(tk.END, f"... and {len(subtitles) - 10} more subtitles")
            
            preview_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview file: {e}")
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        output_file = self.output_file_var.get()
        if output_file:
            folder = os.path.dirname(output_file)
        else:
            input_file = self.input_file_var.get()
            if input_file:
                folder = os.path.dirname(input_file)
            else:
                folder = os.getcwd()
        
        if os.path.exists(folder):
            os.startfile(folder)  # Windows specific
    
    # Settings Methods
    def save_settings(self):
        """Save current settings to config"""
        try:
            # Check if language changed
            old_language = self.config.get('ui_language', 'en')
            new_language = self.ui_lang_var.get()
            
            # Update config with current values
            self.config.set('default_source_language', self.default_source_var.get())
            self.config.set('default_target_language', self.default_target_var.get())
            self.config.set('translation_engine', self.default_engine_var.get())
            self.config.set('delay_between_requests', self.delay_var.get())
            self.config.set('max_retries', self.retries_var.get())
            self.config.set('create_backup', self.backup_setting_var.get())
            self.config.set('cache_enabled', self.cache_setting_var.get())
            self.config.set('output_suffix', self.suffix_var.get())
            self.config.set('ui_language', new_language)
            
            # Save to file
            self.config.save_config()
            
            # If language changed, reload interface
            if old_language != new_language:
                self.change_language(new_language)
                messagebox.showinfo(self.localization.get('success'), 
                                  self.localization.get('settings_saved_restart') if 'settings_saved_restart' in self.localization.strings 
                                  else "Settings saved! Interface language updated.")
            else:
                messagebox.showinfo(self.localization.get('success'), 
                                  "Settings saved successfully!" if self.localization.language == 'en' 
                                  else "تم حفظ الإعدادات بنجاح!")
            
        except Exception as e:
            messagebox.showerror(self.localization.get('error'), f"Failed to save settings: {e}")
    
    def change_language(self, new_language):
        """Change interface language"""
        try:
            # Update localization
            self.localization.set_language(new_language)
            
            # Update window title
            self.root.title(self.localization.get('app_title'))
            
            # Show restart message
            restart_msg = ("Please restart the application to see all interface changes." 
                         if new_language == 'en' 
                         else "الرجاء إعادة تشغيل التطبيق لرؤية جميع تغييرات الواجهة.")
            
            messagebox.showinfo(
                "Language Changed" if new_language == 'en' else "تم تغيير اللغة",
                restart_msg
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change language: {e}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        result = messagebox.askyesno(self.localization.get('warning', 'Confirm'), 
                                   "Reset all settings to defaults?" if self.localization.language == 'en' 
                                   else "إعادة تعيين جميع الإعدادات للافتراضي؟")
        if result:
            try:
                # Reset config to defaults
                self.config.reset_to_defaults()
                
                # Update GUI with defaults
                self.load_settings_to_gui()
                
                messagebox.showinfo(self.localization.get('success'), 
                                  "Settings reset to defaults!" if self.localization.language == 'en'
                                  else "تم إعادة تعيين الإعدادات للافتراضي!")
                
            except Exception as e:
                messagebox.showerror(self.localization.get('error'), f"Failed to reset settings: {e}")
    
    def load_settings_to_gui(self):
        """Load settings from config to GUI"""
        self.default_source_var.set(self.config.get('default_source_language', 'en'))
        self.default_target_var.set(self.config.get('default_target_language', 'ar'))
        self.default_engine_var.set(self.config.get('translation_engine', 'google'))
        self.delay_var.set(self.config.get('delay_between_requests', 0.1))
        self.retries_var.set(self.config.get('max_retries', 3))
        self.backup_setting_var.set(self.config.get('create_backup', True))
        self.cache_setting_var.set(self.config.get('cache_enabled', True))
        self.suffix_var.set(self.config.get('output_suffix', '_translated'))
        self.ui_lang_var.set(self.config.get('ui_language', 'en'))
    
    def open_config_file(self):
        """Open config file in default editor"""
        config_file = self.config.config_file
        if os.path.exists(config_file):
            os.startfile(config_file)  # Windows specific
        else:
            messagebox.showwarning("Warning", "Config file not found")
    
    # Statistics Methods
    def refresh_stats(self):
        """Refresh statistics display"""
        try:
            # Session stats
            session_stats = f"""Session Statistics:
─────────────────────
Files Translated: 0
Total Characters: 0
Average Time per File: 0s
Session Duration: 0m
Last Translation: None

Translation Engines Used:
• Google Translate: 0 files
• Microsoft Translator: 0 files

Supported Formats:
• SRT: Yes
• ASS: Yes  
• VTT: Yes

Language Pairs:
• Auto-detect → Arabic
• English → Arabic
• French → Arabic
"""
            
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, session_stats)
            self.stats_text.config(state='disabled')
            
            # Cache stats
            cache_stats = f"""Cache Statistics:
─────────────────
Cache Status: {"Enabled" if self.config.get('cache_enabled', True) else "Disabled"}
Total Entries: 0
Cache Size: 0 KB
Hit Rate: 0%
Last Updated: Never

Cache Performance:
• Fast Lookups: 0ms avg
• Memory Usage: Low
• Storage: SQLite Database
"""
            
            self.cache_stats_text.config(state='normal')
            self.cache_stats_text.delete(1.0, tk.END)
            self.cache_stats_text.insert(1.0, cache_stats)
            self.cache_stats_text.config(state='disabled')
            
        except Exception as e:
            print(f"Error refreshing stats: {e}")
    
    def clear_cache(self):
        """Clear translation cache"""
        result = messagebox.askyesno("Confirm", "Clear all cached translations?")
        if result:
            try:
                self.translator.cache.clear_cache()
                messagebox.showinfo("Success", "Cache cleared successfully!")
                self.refresh_stats()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear cache: {e}")
    
    def export_stats(self):
        """Export statistics to file"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Export Statistics",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Subtitle Translator Statistics\n")
                    f.write("=" * 40 + "\n")
                    f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # Get current stats text
                    session_text = self.stats_text.get(1.0, tk.END)
                    cache_text = self.cache_stats_text.get(1.0, tk.END)
                    
                    f.write(session_text)
                    f.write("\n" + "=" * 40 + "\n")
                    f.write(cache_text)
                
                messagebox.showinfo("Success", f"Statistics exported to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export statistics: {e}")
    
    # Utility Methods
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
    
    def run(self):
        """Start the GUI application"""
        # Initialize display
        self.refresh_stats()
        self.load_settings_to_gui()
        
        # Set status message based on language
        ready_message = (f"{self.localization.get('ready')} - {self.localization.get('drag_files_here')}" 
                        if self.localization.language == 'ar' 
                        else f"{self.localization.get('ready')} - Drag files here or use Browse button")
        
        self.update_status(ready_message)
        
        # Start main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = SubtitleTranslatorGUI()
    app.run()
