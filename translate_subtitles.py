#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة ترجمة الترجمات
Subtitle Translation Tool
تترجم ملفات الترجمة SRT من الإنجليزية إلى العربية
Translates SRT subtitle files from English to Arabic
"""

import re
import os
import glob
from deep_translator import GoogleTranslator
import time
import argparse

class SubtitleTranslator:
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='ar')
    
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
    
    def translate_text(self, text, target_lang='ar'):
        """Translate text to target language with error handling"""
        try:
            # Skip empty lines or lines with only special characters
            if not text.strip() or text.strip() in ['', '-', '--', '...']:
                return text
            
            # Translate the text using deep-translator
            result = self.translator.translate(text)
            return result
            
        except Exception as e:
            print(f"Translation error for text '{text[:50]}...': {e}")
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
    
    def translate_srt_file(self, input_path, output_path=None, target_lang='ar'):
        """Main function to translate SRT file"""
        if not os.path.exists(input_path):
            print(f"Error: Input file '{input_path}' not found")
            return
        
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_arabic.srt"
        
        print(f"Reading subtitle file: {os.path.basename(input_path)}")
        subtitles = self.parse_srt_file(input_path)
        print(f"Found {len(subtitles)} subtitle entries")
        
        # Translate subtitles
        translated_subtitles = self.translate_subtitles(subtitles, target_lang)
        
        # Save translated file
        self.save_srt_file(translated_subtitles, output_path)
        
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
        """Interactive mode for file selection"""
        print("Movie Subtitle Arabic Translator")
        print("="*50)
        
        while True:
            print("\nChoose one of the following options:")
            print("1. Translate specific file")
            print("2. Translate all SRT files in current directory")
            print("3. Search in another directory")
            print("4. Exit")
            
            choice = input("\nEnter your choice [1-4]: ").strip()
            
            if choice == '1':
                file_path = input("Enter file path: ").strip().strip('"')
                if os.path.exists(file_path) and file_path.endswith('.srt'):
                    self.translate_srt_file(file_path)
                else:
                    print("File not found or not an SRT file")
            
            elif choice == '2':
                self.translate_all_srt_files(".")
            
            elif choice == '3':
                directory = input("Enter directory path: ").strip().strip('"')
                if os.path.exists(directory):
                    self.translate_all_srt_files(directory)
                else:
                    print("Directory not found")
            
            elif choice == '4':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice")

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
