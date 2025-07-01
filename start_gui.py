#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Subtitle Translator - GUI Launcher
مشغل الواجهة الرسومية لمترجم الترجمات المتقدم
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import threading
import time

def check_dependencies():
    """Check if all required dependencies are available"""
    print("Checking dependencies...")
    
    required_modules = [
        'tkinter',
        'googletrans', 
        'langdetect',
        'chardet'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'googletrans':
                import googletrans
                print(f"✓ {module} - version {googletrans.__version__}")
            elif module == 'langdetect':
                import langdetect
                print(f"✓ {module} - available")
            elif module == 'chardet':
                import chardet
                print(f"✓ {module} - version {chardet.__version__}")
            elif module == 'tkinter':
                import tkinter
                print(f"✓ {module} - available")
        except ImportError:
            missing_modules.append(module)
            print(f"✗ {module} - missing")
    
    return missing_modules

def install_missing_dependencies(missing_modules):
    """Install missing dependencies"""
    if not missing_modules:
        return True
    
    print(f"\nMissing modules: {', '.join(missing_modules)}")
    print("Installing missing dependencies...")
    
    import subprocess
    
    try:
        for module in missing_modules:
            if module == 'tkinter':
                print("⚠️  tkinter is part of Python standard library")
                print("   Please reinstall Python with tkinter support")
                return False
            else:
                print(f"Installing {module}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
                print(f"✓ {module} installed successfully")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    print("\nChecking required files...")
    
    required_files = [
        'gui_translator.py',
        'translate_subtitles.py',
        'config.py',
        'subtitle_formats.py',
        'language_detector.py',
        'cache.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            missing_files.append(file)
            print(f"✗ {file} - missing")
    
    return missing_files

def show_startup_splash():
    """Show startup splash screen"""
    splash = tk.Tk()
    splash.title("Starting...")
    splash.geometry("400x200")
    splash.resizable(False, False)
    
    # Center the window
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (400 // 2)
    y = (splash.winfo_screenheight() // 2) - (200 // 2)
    splash.geometry(f"400x200+{x}+{y}")
    
    # Remove window decorations
    splash.overrideredirect(True)
    
    # Create content
    frame = tk.Frame(splash, bg='#2c3e50', relief='raised', borderwidth=2)
    frame.pack(fill='both', expand=True)
    
    # Title
    title_label = tk.Label(frame, text="Advanced Subtitle Translator", 
                          bg='#2c3e50', fg='white', font=('Arial', 16, 'bold'))
    title_label.pack(pady=20)
    
    # Version
    version_label = tk.Label(frame, text="Version 2.2.2", 
                            bg='#2c3e50', fg='#ecf0f1', font=('Arial', 10))
    version_label.pack()
    
    # Status
    status_label = tk.Label(frame, text="Loading components...", 
                           bg='#2c3e50', fg='#bdc3c7', font=('Arial', 9))
    status_label.pack(pady=10)
    
    # Progress bar simulation
    progress_frame = tk.Frame(frame, bg='#2c3e50')
    progress_frame.pack(pady=10)
    
    progress_bar = tk.Frame(progress_frame, bg='#3498db', height=4)
    progress_bar.pack(side='left')
    
    # Animate progress bar
    def animate_progress():
        for i in range(101):
            width = int(300 * i / 100)
            progress_bar.config(width=width)
            
            if i < 30:
                status_label.config(text="Checking dependencies...")
            elif i < 60:
                status_label.config(text="Loading modules...")
            elif i < 90:
                status_label.config(text="Initializing GUI...")
            else:
                status_label.config(text="Ready!")
            
            splash.update()
            time.sleep(0.02)
    
    # Start animation in thread
    def run_animation():
        time.sleep(0.5)  # Brief pause
        animate_progress()
        time.sleep(0.5)  # Show "Ready!" for a moment
        splash.destroy()
    
    animation_thread = threading.Thread(target=run_animation)
    animation_thread.daemon = True
    animation_thread.start()
    
    splash.mainloop()

def main():
    """Main function to start the GUI application"""
    print("Advanced Subtitle Translator v2.2.2")
    print("=" * 40)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    # Check dependencies
    missing_modules = check_dependencies()
    if missing_modules:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_modules)}")
        install_choice = input("Install missing dependencies? (y/n): ").strip().lower()
        
        if install_choice == 'y':
            if not install_missing_dependencies(missing_modules):
                print("❌ Failed to install dependencies. Exiting.")
                return False
        else:
            print("❌ Cannot continue without dependencies. Exiting.")
            return False
    
    # Check required files
    missing_files = check_files()
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all files are in the same directory.")
        return False
    
    print("\n✅ All dependencies and files are available!")
    
    # Check for command line file argument
    startup_file = None
    if len(sys.argv) > 1:
        file_arg = sys.argv[1]
        if os.path.exists(file_arg):
            startup_file = file_arg
            print(f"📄 File passed via command line: {file_arg}")
    
    try:
        # Show splash screen
        print("\n🚀 Starting GUI...")
        show_startup_splash()
        
        # Import and start GUI
        print("Loading GUI components...")
        from gui_translator import SubtitleTranslatorGUI
        
        print("Creating application...")
        app = SubtitleTranslatorGUI()
        
        # Load startup file if provided
        if startup_file:
            app.input_file_var.set(startup_file)
            app.auto_output_file()
            app.detect_input_format()
            app.update_status(f"Loaded: {os.path.basename(startup_file)}")
        
        print("✅ GUI started successfully!")
        print("\n💡 Tips:")
        print("   • Drag and drop subtitle files into the application")
        print("   • Use the Settings tab to customize your preferences")
        print("   • Check the Statistics tab for usage information")
        print("   • Supported formats: .srt, .ass, .vtt")
        
        # Start the application
        app.run()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to start GUI: {e}")
        import traceback
        traceback.print_exc()
        
        # Show error dialog if tkinter is available
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Startup Error", 
                               f"Failed to start the application:\n\n{str(e)}\n\n"
                               "Please check the console for more details.")
        except:
            pass
        
        return False

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Advanced Subtitle Translator.lnk")
        target = os.path.abspath(__file__)
        wDir = os.path.dirname(target)
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print(f"✅ Desktop shortcut created: {path}")
        return True
    except:
        print("⚠️  Could not create desktop shortcut (optional)")
        return False

if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            print("\n🎉 Application finished successfully!")
        else:
            print("\n💔 Application failed to start properly.")
            input("Press Enter to exit...")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Application interrupted by user.")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
