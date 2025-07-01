#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Script for Advanced Subtitle Translator
سكريبت إنشاء ملف تنفيذي لمترجم الترجمات المتقدم
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """تثبيت PyInstaller إذا لم يكن مثبتاً"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_spec_file():
    """إنشاء ملف spec مخصص لـ PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['start_translator.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('localization.py', '.'),
        ('progress_saver.py', '.'),
        ('*.py', '.'),
        ('docs', 'docs'),
        ('requirements.txt', '.'),
        ('LICENSE', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'googletrans',
        'langdetect',
        'chardet',
        'sqlite3',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'threading',
        'queue',
        'pathlib',
        'datetime',
        'json',
        'requests',
        'urllib3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Advanced_Subtitle_Translator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('translator.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Created translator.spec file")

def build_executable():
    """بناء الملف التنفيذي"""
    print("🔨 Building executable...")
    print("⏳ This may take a few minutes...")
    
    try:
        # تشغيل PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm", 
            "translator.spec"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            return True
        else:
            print("❌ Build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_simple_build():
    """إنشاء ملف تنفيذي بسيط"""
    print("🔨 Creating simple executable...")
    
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=AdvancedSubtitleTranslator",
            "--add-data=localization.py;.",
            "--add-data=config.json;.",
            "--hidden-import=googletrans",
            "--hidden-import=langdetect", 
            "--hidden-import=chardet",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "start_translator.py"
        ]
        
        if os.path.exists('icon.ico'):
            cmd.extend(["--icon=icon.ico"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Simple executable created successfully!")
            return True
        else:
            print("❌ Simple build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Simple build error: {e}")
        return False

def organize_output():
    """تنظيم ملفات الإخراج"""
    print("📁 Organizing output files...")
    
    # إنشاء مجلد التوزيع
    dist_dir = Path("AdvancedSubtitleTranslator_Distribution")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # نسخ الملف التنفيذي
    exe_files = list(Path("dist").glob("*.exe"))
    if exe_files:
        exe_file = exe_files[0]
        shutil.copy2(exe_file, dist_dir / "AdvancedSubtitleTranslator.exe")
        print(f"✅ Copied executable: {exe_file.name}")
    
    # نسخ الملفات المهمة
    important_files = [
        "README.md",
        "LICENSE", 
        "ARABIC_UI_GUIDE.md",
        "SOLUTION_SUMMARY.md",
        "config.json"
    ]
    
    for file in important_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"✅ Copied: {file}")
    
    # إنشاء ملف تعليمات
    instructions = """# Advanced Subtitle Translator - Portable Version

## 🚀 Quick Start
1. Double-click `AdvancedSubtitleTranslator.exe` to start
2. No installation required!
3. Supports Arabic and English interfaces

## 📁 Files Included
- AdvancedSubtitleTranslator.exe - Main application
- config.json - Configuration file
- README.md - Full documentation
- ARABIC_UI_GUIDE.md - Arabic interface guide

## 🌍 Language Support
- Change interface language from Settings tab
- Console messages always in English
- Full Arabic interface support

## 💡 System Requirements
- Windows 7/8/10/11
- No Python installation needed
- Internet connection for translation

## 🆘 Support
If you encounter any issues, please check the documentation files included.

Enjoy translating! 🎬✨
"""
    
    with open(dist_dir / "README_PORTABLE.txt", 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"✅ Distribution folder created: {dist_dir}")
    return dist_dir

def main():
    """الدالة الرئيسية"""
    print("🚀 Advanced Subtitle Translator - Build Script")
    print("=" * 50)
    
    # التحقق من المتطلبات
    if not install_pyinstaller():
        print("❌ Cannot proceed without PyInstaller")
        return
    
    # السؤال عن نوع البناء
    print("\n📋 Build Options:")
    print("1. Simple build (recommended) - Single .exe file")
    print("2. Advanced build with spec file")
    
    choice = input("\nChoose build type (1 or 2): ").strip()
    
    success = False
    
    if choice == "2":
        # بناء متقدم
        create_spec_file()
        success = build_executable()
    else:
        # بناء بسيط
        success = create_simple_build()
    
    if success:
        # تنظيم الإخراج
        dist_folder = organize_output()
        
        print("\n🎉 Build completed successfully!")
        print(f"📁 Executable location: {dist_folder}")
        print(f"💾 File size: ~{get_folder_size(dist_folder):.1f} MB")
        print("\n📋 Next steps:")
        print("1. Test the executable on your machine")
        print("2. Zip the distribution folder")
        print("3. Share with your friends!")
        print("\n🎯 Ready to distribute! 🚀")
        
    else:
        print("\n❌ Build failed. Please check the error messages above.")

def get_folder_size(folder):
    """حساب حجم المجلد بالميجابايت"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size / (1024 * 1024)  # Convert to MB
    except:
        return 0

if __name__ == "__main__":
    main()
