#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Subtitle Format Handler
معالج تنسيقات الترجمة المتقدم
Supports SRT, ASS, VTT formats
"""

import re
import os
from datetime import timedelta

class SubtitleFormatHandler:
    """Handler for multiple subtitle formats"""
    
    def __init__(self):
        self.supported_formats = ['.srt', '.ass', '.vtt']
    
    def detect_format(self, file_path):
        """Detect subtitle format from file extension and content"""
        _, ext = os.path.splitext(file_path.lower())
        
        if ext in self.supported_formats:
            return ext.lower()
        
        # Try to detect from content if extension is unknown
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(200)  # Read first 200 chars
                
            if 'WEBVTT' in content:
                return '.vtt'
            elif '[Script Info]' in content or 'Format:' in content:
                return '.ass'
            elif re.search(r'\d+\n\d{2}:\d{2}:\d{2}', content):
                return '.srt'
                
        except Exception:
            pass
            
        return None
    
    def parse_file(self, file_path):
        """Parse subtitle file based on its format"""
        format_type = self.detect_format(file_path)
        
        if format_type == '.srt':
            return self.parse_srt(file_path)
        elif format_type == '.ass':
            return self.parse_ass(file_path)
        elif format_type == '.vtt':
            return self.parse_vtt(file_path)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def parse_srt(self, file_path):
        """Parse SRT subtitle file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        blocks = re.split(r'\n\s*\n', content.strip())
        subtitles = []
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    number = int(lines[0])
                    timestamp = lines[1]
                    text = '\n'.join(lines[2:])
                    
                    subtitles.append({
                        'number': number,
                        'timestamp': timestamp,
                        'text': text,
                        'format': 'srt'
                    })
                except ValueError:
                    continue
        
        return subtitles
    
    def parse_ass(self, file_path):
        """Parse ASS/SSA subtitle file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        lines = content.split('\n')
        subtitles = []
        dialogue_started = False
        number = 1
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('[Events]'):
                dialogue_started = True
                continue
            
            if dialogue_started and line.startswith('Dialogue:'):
                # Parse ASS dialogue line
                # Format: Dialogue: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
                parts = line.split(',', 9)
                if len(parts) >= 10:
                    start_time = parts[1]
                    end_time = parts[2]
                    text = parts[9]
                    
                    # Convert ASS time format to SRT format
                    timestamp = f"{self.ass_time_to_srt(start_time)} --> {self.ass_time_to_srt(end_time)}"
                    
                    # Clean ASS formatting tags
                    text = self.clean_ass_tags(text)
                    
                    subtitles.append({
                        'number': number,
                        'timestamp': timestamp,
                        'text': text,
                        'format': 'ass'
                    })
                    number += 1
        
        return subtitles
    
    def parse_vtt(self, file_path):
        """Parse WebVTT subtitle file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove WEBVTT header
        content = re.sub(r'^WEBVTT\n\n?', '', content)
        
        blocks = re.split(r'\n\s*\n', content.strip())
        subtitles = []
        number = 1
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                # Skip cue identifiers if present
                start_idx = 0
                if '-->' not in lines[0]:
                    start_idx = 1
                
                if start_idx < len(lines) and '-->' in lines[start_idx]:
                    timestamp = lines[start_idx]
                    text = '\n'.join(lines[start_idx + 1:])
                    
                    # Convert VTT time format to SRT format
                    timestamp = self.vtt_time_to_srt(timestamp)
                    
                    # Clean VTT formatting tags
                    text = self.clean_vtt_tags(text)
                    
                    subtitles.append({
                        'number': number,
                        'timestamp': timestamp,
                        'text': text,
                        'format': 'vtt'
                    })
                    number += 1
        
        return subtitles
    
    def save_file(self, subtitles, output_path, format_type=None):
        """Save subtitles in specified format"""
        if format_type is None:
            _, ext = os.path.splitext(output_path.lower())
            format_type = ext
        
        if format_type == '.srt':
            self.save_srt(subtitles, output_path)
        elif format_type == '.ass':
            self.save_ass(subtitles, output_path)
        elif format_type == '.vtt':
            self.save_vtt(subtitles, output_path)
        else:
            raise ValueError(f"Unsupported output format: {format_type}")
    
    def save_srt(self, subtitles, output_path):
        """Save subtitles in SRT format"""
        with open(output_path, 'w', encoding='utf-8') as file:
            for subtitle in subtitles:
                file.write(f"{subtitle['number']}\n")
                file.write(f"{subtitle['timestamp']}\n")
                file.write(f"{subtitle['text']}\n\n")
    
    def save_ass(self, subtitles, output_path):
        """Save subtitles in ASS format"""
        ass_header = """[Script Info]
Title: Translated Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(ass_header)
            
            for subtitle in subtitles:
                # Convert SRT timestamp to ASS format
                start, end = subtitle['timestamp'].split(' --> ')
                start_ass = self.srt_time_to_ass(start)
                end_ass = self.srt_time_to_ass(end)
                
                file.write(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{subtitle['text']}\n")
    
    def save_vtt(self, subtitles, output_path):
        """Save subtitles in WebVTT format"""
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("WEBVTT\n\n")
            
            for subtitle in subtitles:
                # Convert SRT timestamp to VTT format
                timestamp = self.srt_time_to_vtt(subtitle['timestamp'])
                file.write(f"{timestamp}\n")
                file.write(f"{subtitle['text']}\n\n")
    
    # Helper methods for time format conversion
    def ass_time_to_srt(self, ass_time):
        """Convert ASS time format to SRT format"""
        # ASS: 0:00:00.00 -> SRT: 00:00:00,000
        parts = ass_time.split(':')
        if len(parts) == 3:
            h = parts[0].zfill(2)
            m = parts[1].zfill(2)
            s_ms = parts[2].split('.')
            s = s_ms[0].zfill(2)
            ms = (s_ms[1] + '0')[:3] if len(s_ms) > 1 else '000'
            return f"{h}:{m}:{s},{ms}"
        return ass_time
    
    def srt_time_to_ass(self, srt_time):
        """Convert SRT time format to ASS format"""
        # SRT: 00:00:00,000 -> ASS: 0:00:00.00
        return srt_time.replace(',', '.')[:-1]  # Remove last digit of milliseconds
    
    def vtt_time_to_srt(self, vtt_timestamp):
        """Convert VTT timestamp to SRT format"""
        # VTT uses same format but with dots instead of commas
        return vtt_timestamp.replace('.', ',')
    
    def srt_time_to_vtt(self, srt_timestamp):
        """Convert SRT timestamp to VTT format"""
        return srt_timestamp.replace(',', '.')
    
    def clean_ass_tags(self, text):
        """Remove ASS formatting tags"""
        # Remove ASS tags like {\an8}, {\c&Hffffff&}, etc.
        text = re.sub(r'\{[^}]*\}', '', text)
        return text.strip()
    
    def clean_vtt_tags(self, text):
        """Remove VTT formatting tags"""
        # Remove VTT tags like <c.classname>, <i>, etc.
        text = re.sub(r'<[^>]*>', '', text)
        return text.strip()
    
    def get_format_info(self, format_type):
        """Get information about a subtitle format"""
        format_info = {
            '.srt': {
                'name': 'SubRip',
                'extension': '.srt',
                'description': 'Simple text-based subtitle format',
                'supports_formatting': False
            },
            '.ass': {
                'name': 'Advanced SSA',
                'extension': '.ass',
                'description': 'Advanced formatting with styles and effects',
                'supports_formatting': True
            },
            '.vtt': {
                'name': 'WebVTT',
                'extension': '.vtt',
                'description': 'Web-based subtitle format for HTML5',
                'supports_formatting': True
            }
        }
        return format_info.get(format_type, {})
    
    def read_subtitles(self, file_path):
        """Read subtitles from file - alias for parse_file for compatibility"""
        return self.parse_file(file_path)
    
    def write_subtitles(self, subtitles, output_path, format_type=None):
        """Write subtitles to file - alias for save_file for compatibility"""
        return self.save_file(subtitles, output_path, format_type)
