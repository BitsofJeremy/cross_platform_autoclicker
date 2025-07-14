#!/usr/bin/env python3
"""
Build script for creating executable versions of the Auto Clicker application.
Supports macOS, Linux, and Windows using PyInstaller.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


class ExecutableBuilder:
    """Class to handle building executables for different platforms."""
    
    def __init__(self):
        """Initialize the builder."""
        self.current_platform = platform.system()
        self.script_dir = Path(__file__).parent
        self.source_file = self.script_dir / "auto_clicker.py"
        self.build_dir = self.script_dir / "build"
        self.dist_dir = self.script_dir / "dist"
        
        # Platform-specific settings
        self.platform_configs = {
            "Darwin": {  # macOS
                "name": "AutoClicker",
                "extension": ".app",
                "icon": "icon.icns",
                "additional_args": ["--windowed", "--onefile"]
            },
            "Linux": {
                "name": "AutoClicker",
                "extension": "",
                "icon": "icon.png",
                "additional_args": ["--onefile"]
            },
            "Windows": {
                "name": "AutoClicker",
                "extension": ".exe",
                "icon": "icon.ico",
                "additional_args": ["--windowed", "--onefile"]
            }
        }
    
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        required_packages = ["pyinstaller", "pyautogui"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✓ {package} is installed")
            except ImportError:
                missing_packages.append(package)
                print(f"✗ {package} is missing")
        
        if missing_packages:
            print(f"\nMissing packages: {', '.join(missing_packages)}")
            print("Install them using:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        
        return True
    
    def check_source_file(self):
        """Check if the source file exists."""
        if not self.source_file.exists():
            print(f"✗ Source file not found: {self.source_file}")
            return False
        
        print(f"✓ Source file found: {self.source_file}")
        return True
    
    def clean_build_directories(self):
        """Clean previous build directories."""
        for directory in [self.build_dir, self.dist_dir]:
            if directory.exists():
                print(f"Cleaning {directory}")
                shutil.rmtree(directory)
    
    def create_spec_file(self):
        """Create a PyInstaller spec file with custom configuration."""
        config = self.platform_configs.get(self.current_platform, self.platform_configs["Linux"])
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.source_file}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
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
    name='{config["name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
        
        # Add app bundle for macOS
        if self.current_platform == "Darwin":
            spec_content += f'''
app = BUNDLE(
    exe,
    name='{config["name"]}.app',
    icon=None,
    bundle_identifier='com.autoclicker.app',
    info_plist={{
        'NSHighResolutionCapable': 'True',
        'NSAppleEventsUsageDescription': 'This app needs to send mouse clicks.',
        'NSAccessibilityUsageDescription': 'This app needs accessibility permission to click.',
    }},
)
'''
        
        spec_file = self.script_dir / f"{config['name']}.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        return spec_file
    
    def build_executable(self):
        """Build the executable using PyInstaller."""
        config = self.platform_configs.get(self.current_platform, self.platform_configs["Linux"])
        
        # Create spec file
        spec_file = self.create_spec_file()
        
        # Build command
        cmd = [
            "pyinstaller",
            str(spec_file),
            "--clean",
            "--noconfirm"
        ]
        
        print(f"Building executable for {self.current_platform}...")
        print(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, cwd=self.script_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Build successful!")
                return True
            else:
                print("✗ Build failed!")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False
                
        except FileNotFoundError:
            print("✗ PyInstaller not found. Please install it using: pip install pyinstaller")
            return False
        except Exception as e:
            print(f"✗ Build error: {e}")
            return False
    
    def post_build_actions(self):
        """Perform post-build actions."""
        config = self.platform_configs[self.current_platform]
        expected_output = self.dist_dir / f"{config['name']}{config['extension']}"
        
        if expected_output.exists():
            print(f"✓ Executable created: {expected_output}")
            
            # Get file size
            if expected_output.is_file():
                size = expected_output.stat().st_size
                size_mb = size / (1024 * 1024)
                print(f"  Size: {size_mb:.2f} MB")
            
            # Platform-specific instructions
            if self.current_platform == "Darwin":
                print("\nmacOS Instructions:")
                print("1. The .app bundle is ready to use")
                print("2. You may need to grant accessibility permissions:")
                print("   System Preferences → Security & Privacy → Privacy → Accessibility")
                print("3. Add the AutoClicker app to the allowed applications")
                
            elif self.current_platform == "Linux":
                print("\nLinux Instructions:")
                print("1. Make the file executable: chmod +x AutoClicker")
                print("2. Run with: ./AutoClicker")
                print("3. You may need to install python3-tk if not already installed")
                
            elif self.current_platform == "Windows":
                print("\nWindows Instructions:")
                print("1. The .exe file is ready to use")
                print("2. Windows Defender might flag it as potentially unwanted")
                print("3. This is a false positive - you can add it to exclusions")
            
            return True
        else:
            print(f"✗ Expected output not found: {expected_output}")
            return False
    
    def create_requirements_file(self):
        """Create a requirements.txt file for dependencies."""
        requirements = [
            "pyautogui>=0.9.50",
            "pyinstaller>=5.0.0"
        ]
        
        requirements_file = self.script_dir / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write('\n'.join(requirements))
        
        print(f"✓ Created requirements.txt")
    
    def build(self):
        """Main build process."""
        print("=" * 50)
        print("Auto Clicker - Executable Builder")
        print("=" * 50)
        print(f"Platform: {self.current_platform}")
        print(f"Python: {sys.version}")
        print()
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Check source file
        if not self.check_source_file():
            return False
        
        # Clean previous builds
        self.clean_build_directories()
        
        # Create requirements file
        self.create_requirements_file()
        
        # Build executable
        if not self.build_executable():
            return False
        
        # Post-build actions
        if not self.post_build_actions():
            return False
        
        print("\n" + "=" * 50)
        print("Build completed successfully!")
        print("=" * 50)
        return True


def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "pyautogui"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def create_build_scripts():
    """Create platform-specific build scripts."""
    script_dir = Path(__file__).parent
    
    # Create batch file for Windows
    windows_script = script_dir / "build_windows.bat"
    with open(windows_script, 'w') as f:
        f.write("""@echo off
echo Building Auto Clicker for Windows...
python build_executable.py
pause
""")
    
    # Create shell script for Unix-like systems
    unix_script = script_dir / "build_unix.sh"
    with open(unix_script, 'w') as f:
        f.write("""#!/bin/bash
echo "Building Auto Clicker for Unix/Linux/macOS..."
python3 build_executable.py
read -p "Press Enter to continue..."
""")
    
    # Make shell script executable
    try:
        os.chmod(unix_script, 0o755)
    except:
        pass
    
    print("✓ Created platform-specific build scripts")
    print(f"  Windows: {windows_script}")
    print(f"  Unix/Linux/macOS: {unix_script}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Auto Clicker executable")
    parser.add_argument("--install-deps", action="store_true", 
                       help="Install required dependencies")
    parser.add_argument("--create-scripts", action="store_true",
                       help="Create platform-specific build scripts")
    parser.add_argument("--clean", action="store_true",
                       help="Clean build directories only")
    
    args = parser.parse_args()
    
    if args.install_deps:
        install_dependencies()
        return
    
    if args.create_scripts:
        create_build_scripts()
        return
    
    builder = ExecutableBuilder()
    
    if args.clean:
        builder.clean_build_directories()
        print("✓ Build directories cleaned")
        return
    
    # Run the build process
    success = builder.build()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()