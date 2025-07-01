#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic Language Detection for Subtitles
كاشف اللغة التلقائي للترجمات
"""

import re
from deep_translator import GoogleTranslator
from collections import Counter

class LanguageDetector:
    """Automatic language detection for subtitle text"""
    
    def __init__(self):
        # Common words in different languages
        self.language_patterns = {
            'en': {
                'words': ['the', 'and', 'you', 'that', 'was', 'for', 'are', 'with', 'his', 'they'],
                'chars': set('abcdefghijklmnopqrstuvwxyz'),
                'name': 'English'
            },
            'ar': {
                'words': ['في', 'من', 'إلى', 'على', 'هذا', 'هذه', 'التي', 'الذي', 'كان', 'كانت'],
                'chars': set('ابتثجحخدذرزسشصضطظعغفقكلمنهوي'),
                'name': 'Arabic'
            },
            'fr': {
                'words': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir'],
                'chars': set('abcdefghijklmnopqrstuvwxyzàâäéèêëïîôöùûüÿç'),
                'name': 'French'
            },
            'es': {
                'words': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se'],
                'chars': set('abcdefghijklmnopqrstuvwxyzáéíóúüñ'),
                'name': 'Spanish'
            },
            'de': {
                'words': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich'],
                'chars': set('abcdefghijklmnopqrstuvwxyzäöüß'),
                'name': 'German'
            },
            'it': {
                'words': ['il', 'di', 'che', 'e', 'la', 'per', 'una', 'in', 'del', 'è'],
                'chars': set('abcdefghijklmnopqrstuvwxyzàèéìíîòóù'),
                'name': 'Italian'
            },
            'ru': {
                'words': ['в', 'и', 'не', 'на', 'я', 'быть', 'тот', 'он', 'оно', 'они'],
                'chars': set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя'),
                'name': 'Russian'
            },
            'ja': {
                'words': ['の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'と', 'し'],
                'chars': set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'),
                'name': 'Japanese'
            },
            'ko': {
                'words': ['이', '은', '는', '을', '를', '에', '의', '가', '와', '과'],
                'chars': set('가나다라마바사아자차카타파하'),
                'name': 'Korean'
            },
            'zh': {
                'words': ['的', '一', '是', '在', '不', '了', '有', '和', '人', '这'],
                'chars': set('一二三四五六七八九十'),
                'name': 'Chinese'
            }
        }
    
    def detect_language_simple(self, text):
        """Simple pattern-based language detection"""
        if not text or not text.strip():
            return 'unknown'
        
        # Clean text
        clean_text = self.clean_text(text)
        words = clean_text.lower().split()
        
        if len(words) == 0:
            return 'unknown'
        
        # Character-based detection
        char_scores = {}
        for lang_code, lang_data in self.language_patterns.items():
            score = 0
            total_chars = 0
            
            for char in clean_text.lower():
                if char.isalpha():
                    total_chars += 1
                    if char in lang_data['chars']:
                        score += 1
            
            if total_chars > 0:
                char_scores[lang_code] = score / total_chars
        
        # Word-based detection
        word_scores = {}
        for lang_code, lang_data in self.language_patterns.items():
            matches = sum(1 for word in words if word in lang_data['words'])
            word_scores[lang_code] = matches / max(len(words), 1)
        
        # Combine scores
        combined_scores = {}
        for lang_code in self.language_patterns.keys():
            char_score = char_scores.get(lang_code, 0)
            word_score = word_scores.get(lang_code, 0)
            # Weight word matches more heavily
            combined_scores[lang_code] = (char_score * 0.3) + (word_score * 0.7)
        
        # Return language with highest score
        if combined_scores:
            best_lang = max(combined_scores, key=combined_scores.get)
            confidence = combined_scores[best_lang]
            
            # Require minimum confidence
            if confidence > 0.05:  # Lower threshold for better detection
                return best_lang
        
        return 'unknown'
    
    def detect_language_online(self, text):
        """Online language detection using Google Translate"""
        try:
            # Use Google Translate's detect method
            detector = GoogleTranslator(source='auto', target='en')
            # Get a sample of text for detection
            sample_text = self.get_text_sample(text)
            
            if not sample_text:
                return 'unknown'
            
            # Try to translate to get source language
            result = detector.translate(sample_text)
            
            # Unfortunately, deep-translator doesn't expose detected language
            # So we'll use the simple detection as fallback
            return self.detect_language_simple(text)
            
        except Exception:
            # Fallback to simple detection
            return self.detect_language_simple(text)
    
    def detect_from_subtitles(self, subtitles, method='simple'):
        """Detect language from a list of subtitle entries"""
        if not subtitles:
            return 'unknown'
        
        # Combine text from multiple subtitles for better accuracy
        combined_text = ' '.join([sub.get('text', '') for sub in subtitles[:20]])  # Use first 20 subtitles
        
        if method == 'online':
            return self.detect_language_online(combined_text)
        else:
            return self.detect_language_simple(combined_text)
    
    def clean_text(self, text):
        """Clean text for language detection"""
        # Remove subtitle formatting
        text = re.sub(r'<[^>]*>', '', text)  # HTML tags
        text = re.sub(r'\{[^}]*\}', '', text)  # ASS tags
        text = re.sub(r'&[^;]+;', '', text)  # HTML entities
        
        # Remove numbers and special characters for word detection
        text = re.sub(r'[0-9\(\)\[\]\{\}<>\"\'`]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def get_text_sample(self, text, max_length=500):
        """Get a representative sample of text for detection"""
        clean_text = self.clean_text(text)
        
        if len(clean_text) <= max_length:
            return clean_text
        
        # Take words from the middle to avoid titles/credits
        words = clean_text.split()
        if len(words) > 20:
            start_idx = len(words) // 4
            end_idx = start_idx + (len(words) // 2)
            words = words[start_idx:end_idx]
        
        sample = ' '.join(words)
        return sample[:max_length]
    
    def get_language_name(self, lang_code):
        """Get human-readable language name"""
        return self.language_patterns.get(lang_code, {}).get('name', lang_code.upper())
    
    def get_supported_languages(self):
        """Get list of supported languages for detection"""
        return {code: data['name'] for code, data in self.language_patterns.items()}
    
    def detect_with_confidence(self, text, method='simple'):
        """Detect language with confidence score"""
        detected_lang = self.detect_language_simple(text) if method == 'simple' else self.detect_language_online(text)
        
        # Calculate confidence based on detection method
        if detected_lang == 'unknown':
            return detected_lang, 0.0
        
        # Simple confidence calculation
        clean_text = self.clean_text(text)
        words = clean_text.lower().split()
        
        if detected_lang in self.language_patterns:
            lang_data = self.language_patterns[detected_lang]
            matches = sum(1 for word in words if word in lang_data['words'])
            confidence = min(matches / max(len(words), 1) * 2, 1.0)  # Cap at 1.0
        else:
            confidence = 0.5  # Default confidence for online detection
        
        return detected_lang, confidence
    
    def detect_language(self, text, method='simple'):
        """Detect language from text - main interface method"""
        if method == 'simple':
            return self.detect_language_simple(text)
        elif method == 'online':
            return self.detect_language_online(text)
        else:
            # Default to simple method
            return self.detect_language_simple(text)
