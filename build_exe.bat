@echo off
title Build Advanced Subtitle Translator Executable
echo 🚀 Advanced Subtitle Translator - Build Script
echo ===============================================
echo.

echo 📦 Installing PyInstaller...
pip install pyinstaller

echo.
echo 🔨 Building executable...
echo ⏳ This may take a few minutes...
echo.

REM Create simple executable
pyinstaller --onefile --windowed ^
    --name="AdvancedSubtitleTranslator" ^
    --add-data="localization.py;." ^
    --add-data="config.json;." ^
    --hidden-import="googletrans" ^
    --hidden-import="langdetect" ^
    --hidden-import="chardet" ^
    --hidden-import="tkinter" ^
    --hidden-import="tkinter.ttk" ^
    --hidden-import="tkinter.filedialog" ^
    --hidden-import="tkinter.messagebox" ^
    --hidden-import="tkinter.scrolledtext" ^
    start_translator.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ Build completed successfully!
    echo 📁 Executable created in: dist\AdvancedSubtitleTranslator.exe
    echo.
    echo 📋 Creating distribution folder...
    
    REM Create distribution folder
    if exist "AdvancedSubtitleTranslator_Portable" rmdir /s /q "AdvancedSubtitleTranslator_Portable"
    mkdir "AdvancedSubtitleTranslator_Portable"
    
    REM Copy executable
    copy "dist\AdvancedSubtitleTranslator.exe" "AdvancedSubtitleTranslator_Portable\"
    
    REM Copy important files
    copy "README.md" "AdvancedSubtitleTranslator_Portable\" 2>nul
    copy "LICENSE" "AdvancedSubtitleTranslator_Portable\" 2>nul
    copy "ARABIC_UI_GUIDE.md" "AdvancedSubtitleTranslator_Portable\" 2>nul
    copy "config.json" "AdvancedSubtitleTranslator_Portable\" 2>nul
    
    REM Create instructions file
    echo # Advanced Subtitle Translator - Portable Version > "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo. >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo ## Quick Start: >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo 1. Double-click AdvancedSubtitleTranslator.exe >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo 2. No installation required! >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo 3. Supports Arabic and English interfaces >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo. >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo ## System Requirements: >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo - Windows 7/8/10/11 >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo - Internet connection for translation >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    echo - No Python installation needed >> "AdvancedSubtitleTranslator_Portable\README_PORTABLE.txt"
    
    echo.
    echo 🎉 Distribution package ready!
    echo 📁 Location: AdvancedSubtitleTranslator_Portable\
    echo 💾 Ready to zip and share with friends!
    echo.
    echo 📋 Next steps:
    echo 1. Test AdvancedSubtitleTranslator.exe
    echo 2. Zip the AdvancedSubtitleTranslator_Portable folder
    echo 3. Share with your friends!
    echo.
    
) else (
    echo.
    echo ❌ Build failed!
    echo 💡 Make sure all dependencies are installed:
    echo    pip install -r requirements.txt
    echo.
)

pause
