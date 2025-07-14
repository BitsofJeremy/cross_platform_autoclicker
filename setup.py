#!/usr/bin/env python3
"""
Setup script for Auto Clicker application.
Handles installation, dependency management, and build preparation.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 6):
        print("✗ Python 3.6 or higher is required")
        print(f"  Current version: {sys.version}")
        return False
    
    print(f"✓ Python version: {sys.version}")
    return True


def install_package(package_name, upgrade=False):
    """Install a Python package using pip."""
    cmd = [sys.executable, "-m", "pip", "install"]
    
    if upgrade:
        cmd.append("--upgrade")
    
    cmd.append(package_name)
    
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


def install_dependencies():
    """Install all required dependencies."""
    print("Installing dependencies...")
    
    # Upgrade pip first
    print("  Upgrading pip...")
    if not install_package("pip", upgrade=True):
        print("  ⚠ Failed to upgrade pip, continuing anyway...")
    
    # Required packages
    packages = [
        "pyautogui",
        "pyinstaller"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"  Installing {package}...")
        if install_package(package):
            print(f"  ✓ {package} installed successfully")
        else:
            print(f"  ✗ Failed to install {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n✗ Failed to install: {', '.join(failed_packages)}")
        print("Please try installing them manually:")
        for package in failed_packages:
            print(f"  pip install {package}")
        return False
    
    print("✓ All dependencies installed successfully")
    return True


def check_platform_requirements():
    """Check platform-specific requirements."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("macOS detected - you may need to:")
        print("  1. Grant accessibility permissions to Python/Terminal")
        print("  2. Install Xcode Command Line Tools if not already installed")
        
    elif system == "Linux":
        print("Linux detected - you may need to:")
        print("  1. Install python3-tk: sudo apt-get install python3-tk")
        print("  2. Install xdotool: sudo apt-get install xdotool")
        
    elif system == "Windows":
        print("Windows detected - should work out of the box")
        print("  Note: Windows Defender might flag the executable as suspicious")
        
    else:
        print(f"Unknown platform: {system}")
        print("  The application may still work, but hasn't been tested")


def create_virtual_environment():
    """Create a virtual environment for the project."""
    venv_path = Path.cwd() / "venv"
    
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✓ Virtual environment created")
        
        # Determine activation script path
        if platform.system() == "Windows":
            activate_script = venv_path / "Scripts" / "activate.bat"
        else:
            activate_script = venv_path / "bin" / "activate"
        
        print(f"To activate the virtual environment, run:")
        if platform.system() == "Windows":
            print(f"  {activate_script}")
        else:
            print(f"  source {activate_script}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create virtual environment: {e}")
        return False


def verify_installation():
    """Verify that the installation was successful."""
    print("Verifying installation...")
    
    # Check if pyautogui can be imported
    try:
        import pyautogui
        print("✓ pyautogui imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pyautogui: {e}")
        return False
    
    # Check if pyinstaller is available
    try:
        result = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ PyInstaller version: {result.stdout.strip()}")
        else:
            print("✗ PyInstaller not working correctly")
            return False
    except Exception as e:
        print(f"✗ PyInstaller check failed: {e}")
        return False
    
    # Check if main script exists
    main_script = Path.cwd() / "auto_clicker.py"
    if main_script.exists():
        print("✓ Main script found")
    else:
        print("✗ Main script (auto_clicker.py) not found")
        return False
    
    print("✓ Installation verification successful")
    return True


def create_desktop_shortcut():
    """Create a desktop shortcut (platform-specific)."""
    system = platform.system()
    
    if system == "Windows":
        # Windows shortcut creation would require pywin32
        print("To create a desktop shortcut on Windows:")
        print("  1. Right-click on auto_clicker.py")
        print("  2. Select 'Send to' > 'Desktop (create shortcut)'")
        
    elif system == "Darwin":  # macOS
        print("To create a desktop shortcut on macOS:")
        print("  1. Open Automator")
        print("  2. Create a new 'Application'")
        print("  3. Add 'Run Shell Script' action")
        print(f"  4. Enter: cd '{Path.cwd()}' && python3 auto_clicker.py")
        
    elif system == "Linux":
        desktop_file_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Auto Clicker
Comment=Python Auto Clicker Application
Exec=python3 {Path.cwd() / 'auto_clicker.py'}
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;
"""
        
        desktop_file = Path.home() / "Desktop" / "AutoClicker.desktop"
        try:
            with open(desktop_file, 'w') as f:
                f.write(desktop_file_content)
            os.chmod(desktop_file, 0o755)
            print(f"✓ Desktop shortcut created: {desktop_file}")
        except Exception as e:
            print(f"✗ Failed to create desktop shortcut: {e}")


def main():
    """Main setup function."""
    print("=" * 60)
    print("Auto Clicker - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check platform requirements
    check_platform_requirements()
    print()
    
    # Ask user what they want to do
    print("Setup options:")
    print("  1. Install dependencies only")
    print("  2. Create virtual environment and install dependencies")
    print("  3. Full setup (dependencies + verification + shortcuts)")
    print("  4. Just verify existing installation")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nSetup cancelled by user")
        sys.exit(0)
    
    if choice == "1":
        success = install_dependencies()
        
    elif choice == "2":
        success = create_virtual_environment()
        if success:
            print("\nNote: Activate the virtual environment before installing dependencies")
            print("Then run this script again to install dependencies")
        
    elif choice == "3":
        success = install_dependencies()
        if success:
            success = verify_installation()
        if success:
            create_desktop_shortcut()
            
    elif choice == "4":
        success = verify_installation()
        
    else:
        print("Invalid choice")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    if success:
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("  1. Run the application: python auto_clicker.py")
        print("  2. Build executable: python build_executable.py")
        print("  3. Read the README.md for detailed instructions")
    else:
        print("Setup encountered errors - please check the output above")
        sys.exit(1)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
