#!/usr/bin/env python3
"""
Build Windows executable for V-USB Driver Installer
Requires: pyinstaller
"""

import subprocess
import sys
from pathlib import Path


def build_exe():
    """Build executable using PyInstaller"""
    
    project_root = Path(__file__).parent
    script = project_root / "windows_driver_installer.py"
    
    if not script.exists():
        print(f"Error: {script} not found")
        return False
    
    print("Building Windows executable...")
    print(f"Script: {script}")
    
    try:
        # Build with PyInstaller
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=V-USB Driver Installer",
            "--icon=NONE",
            "--add-data=.:.",
            "--hidden-import=tkinter",
            "--collect-all=tkinter",
            str(script)
        ]
        
        print(f"\nCommand: {' '.join(cmd)}\n")
        
        result = subprocess.run(cmd, cwd=project_root)
        
        if result.returncode == 0:
            exe_path = project_root / "dist" / "V-USB Driver Installer.exe"
            if exe_path.exists():
                print(f"\n✓ Build successful!")
                print(f"Executable: {exe_path}")
                print(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
                return True
        
        print("\n✗ Build failed")
        return False
        
    except FileNotFoundError:
        print("Error: PyInstaller not found")
        print("Install with: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Main entry point"""
    if sys.platform != "win32":
        print("Warning: This script is designed to run on Windows")
        print("You can still run it on Linux/macOS, but the executable will be for Windows")
    
    if not build_exe():
        sys.exit(1)


if __name__ == "__main__":
    main()
