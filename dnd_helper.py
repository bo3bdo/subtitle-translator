#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Drag and Drop Helper for GUI
مساعد السحب والإفلات للواجهة الرسومية
"""

import tkinter as tk
from tkinter import messagebox
import os

class DragDropMixin:
    """Mixin class to add drag and drop functionality to tkinter widgets"""
    
    def __init__(self):
        self.dnd_accept = ['text/uri-list']
        
    def setup_dnd(self, widget, callback=None):
        """Setup drag and drop for a widget"""
        self.dnd_callback = callback
        
        # Bind drag and drop events
        widget.bind('<Button-1>', self.dnd_start, '+')
        widget.bind('<B1-Motion>', self.dnd_motion, '+')
        widget.bind('<ButtonRelease-1>', self.dnd_end, '+')
        
        # For file associations (Windows specific)
        try:
            widget.drop_target_register('DND_Files')
            widget.dnd_bind('<<Drop>>', self.dnd_drop)
        except:
            # If tkdnd is not available, use alternative method
            self.setup_alternative_dnd(widget)
    
    def setup_alternative_dnd(self, widget):
        """Alternative drag and drop setup when tkdnd is not available"""
        # Set up visual feedback for drag operations
        widget.bind('<Enter>', self.on_drag_enter)
        widget.bind('<Leave>', self.on_drag_leave)
        
        # Add support for file associations via command line args
        import sys
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if os.path.exists(file_path) and self.is_subtitle_file(file_path):
                if self.dnd_callback:
                    self.dnd_callback([file_path])
    
    def on_drag_enter(self, event):
        """Visual feedback when entering drag area"""
        widget = event.widget
        try:
            original_relief = getattr(widget, '_original_relief', widget.cget('relief'))
            widget._original_relief = original_relief
            widget.config(relief='solid', highlightbackground='blue', highlightthickness=2)
        except:
            pass
    
    def on_drag_leave(self, event):
        """Restore visual state when leaving drag area"""
        widget = event.widget
        try:
            original_relief = getattr(widget, '_original_relief', 'flat')
            widget.config(relief=original_relief, highlightthickness=0)
        except:
            pass
    
    def dnd_start(self, event):
        """Start drag operation"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def dnd_motion(self, event):
        """Handle drag motion"""
        # Calculate drag distance
        dx = event.x - getattr(self, 'drag_start_x', event.x)
        dy = event.y - getattr(self, 'drag_start_y', event.y)
        
        # If significant movement, treat as drag
        if abs(dx) > 5 or abs(dy) > 5:
            self.is_dragging = True
    
    def dnd_end(self, event):
        """End drag operation"""
        if not getattr(self, 'is_dragging', False):
            # If not dragging, treat as click
            if hasattr(self, 'on_click'):
                self.on_click(event)
        
        self.is_dragging = False
    
    def dnd_drop(self, event):
        """Handle file drop"""
        try:
            # Get dropped files
            files = self.tk.splitlist(event.data)
            if self.dnd_callback:
                self.dnd_callback(files)
        except Exception as e:
            print(f"Drop error: {e}")
    
    def is_subtitle_file(self, file_path):
        """Check if file is a supported subtitle file"""
        subtitle_extensions = ['.srt', '.ass', '.vtt']
        return any(file_path.lower().endswith(ext) for ext in subtitle_extensions)

class FileDropHelper:
    """Helper class for file drop operations"""
    
    @staticmethod
    def handle_file_drop(files, target_widget=None, callback=None):
        """Handle dropped files"""
        if not files:
            return
        
        subtitle_files = []
        other_files = []
        
        for file_path in files:
            if os.path.isfile(file_path):
                if FileDropHelper.is_subtitle_file(file_path):
                    subtitle_files.append(file_path)
                else:
                    other_files.append(file_path)
            elif os.path.isdir(file_path):
                # Find subtitle files in directory
                found_files = FileDropHelper.find_subtitle_files(file_path)
                subtitle_files.extend(found_files)
        
        if subtitle_files and callback:
            callback(subtitle_files)
        
        if other_files:
            messagebox.showwarning(
                "Unsupported Files",
                f"Some files were ignored (unsupported format):\n" + 
                "\n".join([os.path.basename(f) for f in other_files[:5]]) +
                (f"\n... and {len(other_files) - 5} more" if len(other_files) > 5 else "")
            )
    
    @staticmethod
    def is_subtitle_file(file_path):
        """Check if file is a supported subtitle file"""
        subtitle_extensions = ['.srt', '.ass', '.vtt']
        return any(file_path.lower().endswith(ext) for ext in subtitle_extensions)
    
    @staticmethod
    def find_subtitle_files(directory):
        """Find all subtitle files in directory"""
        subtitle_files = []
        subtitle_extensions = ['.srt', '.ass', '.vtt']
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in subtitle_extensions):
                        subtitle_files.append(os.path.join(root, file))
        except Exception as e:
            print(f"Error scanning directory: {e}")
        
        return subtitle_files

def setup_file_association():
    """Setup file association for drag and drop from file explorer"""
    import sys
    import tkinter as tk
    
    # Check if file was passed as command line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            return file_path
    
    return None

def enable_dnd_for_widget(widget, callback):
    """Enable drag and drop for a specific widget"""
    try:
        # Try using tkdnd if available
        widget.drop_target_register('DND_Files')
        widget.dnd_bind('<<Drop>>', lambda event: callback(widget.tk.splitlist(event.data)))
        return True
    except:
        # Fallback to basic file association
        return False

def create_visual_drop_zone(parent, callback, text="Drop files here"):
    """Create a visual drop zone widget"""
    frame = tk.Frame(parent, relief='solid', borderwidth=2, bg='#f0f0f0')
    
    label = tk.Label(frame, text=text, bg='#f0f0f0', fg='#666666',
                    font=('Arial', 10), wraplength=200)
    label.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Setup drag and drop
    enable_dnd_for_widget(frame, callback)
    enable_dnd_for_widget(label, callback)
    
    # Visual feedback
    def on_enter(event):
        frame.config(bg='#e6f3ff', relief='solid')
        label.config(bg='#e6f3ff', fg='#0066cc')
    
    def on_leave(event):
        frame.config(bg='#f0f0f0', relief='solid')
        label.config(bg='#f0f0f0', fg='#666666')
    
    frame.bind('<Enter>', on_enter)
    label.bind('<Enter>', on_enter)
    frame.bind('<Leave>', on_leave)
    label.bind('<Leave>', on_leave)
    
    return frame

if __name__ == "__main__":
    # Test drag and drop functionality
    root = tk.Tk()
    root.title("Drag and Drop Test")
    root.geometry("400x300")
    
    def test_callback(files):
        print(f"Dropped files: {files}")
        for file in files:
            if FileDropHelper.is_subtitle_file(file):
                print(f"  Subtitle file: {file}")
            else:
                print(f"  Other file: {file}")
    
    drop_zone = create_visual_drop_zone(root, test_callback, "Drop subtitle files here\n(.srt, .ass, .vtt)")
    drop_zone.pack(expand=True, fill='both', padx=20, pady=20)
    
    root.mainloop()
