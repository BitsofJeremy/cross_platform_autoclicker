# Auto Clicker GUI Application

A modern, cross-platform auto-clicker application with a graphical user interface built using Python's tkinter library.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Understanding the Code](#understanding-the-code)
- [Building Executable](#building-executable)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

- **Modern GUI**: Clean, intuitive interface using tkinter and ttk widgets
- **Configurable Click Speed**: Set clicks per second from 0.1 to 50.0
- **Click Count Options**: Choose between infinite clicks or a specific number
- **Mouse Button Selection**: Support for left, right, and middle mouse buttons
- **Click Types**: Single click or double click options
- **Keyboard Shortcuts**: F6 to toggle clicking, ESC to stop
- **Real-time Status**: Shows current status and total click count
- **Cross-platform**: Works on macOS, Linux, and Windows
- **Fail-safe Protection**: Built-in protection against runaway clicking

## Requirements

### Python Version
- Python 3.6 or higher

### Dependencies
- `tkinter` (usually included with Python)
- `pyautogui` (must be installed separately)

## Installation

### Step 1: Clone or Download
```bash
git clone https://github.com/BitsofJeremy/cross_platform_autoclicker.git
cd auto-clicker
```

### Step 2: Install Dependencies
```bash
pip install pyautogui
```

### Step 3: Run the Application
```bash
python auto_clicker.py
```

## Usage

### Basic Usage
1. Launch the application by running `python auto_clicker.py`
2. Configure your settings:
   - **Click Speed**: Set how many clicks per second (CPS)
   - **Click Count**: Choose infinite or set a specific number
   - **Mouse Button**: Select left, right, or middle mouse button
   - **Click Type**: Choose single or double click
3. Click "Start Clicking"
4. Position your mouse where you want to click
5. Press F6 to begin clicking
6. Press F6 again or ESC to stop

### Keyboard Shortcuts
- **F6**: Toggle clicking on/off
- **ESC**: Stop clicking

### Safety Features
- **Fail-safe**: Move mouse to any corner of the screen to stop clicking
- **Thread-safe**: Clicking runs in a separate thread to keep GUI responsive

## Code Structure

```
auto_clicker.py
├── AutoClickerGUI class
│   ├── __init__()              # Initialize the application
│   ├── setup_window()          # Configure main window
│   ├── setup_variables()       # Initialize tkinter variables
│   ├── setup_widgets()         # Create GUI components
│   ├── setup_bindings()        # Set up keyboard shortcuts
│   ├── start_clicking()        # Start the clicking process
│   ├── stop_clicking()         # Stop the clicking process
│   ├── click_worker()          # Worker thread for clicking
│   └── run()                   # Start the application
└── main()                      # Entry point
```

## Understanding the Code

### For Junior Python Developers

#### 1. Object-Oriented Programming (OOP)
The application uses a class-based structure:
```python
class AutoClickerGUI:
    def __init__(self):
        # Initialize the application
        self.root = tk.Tk()
        self.setup_window()
        # ... more initialization
```

#### 2. GUI with tkinter
The GUI is built using tkinter, Python's standard GUI library:
```python
# Creating widgets
self.start_button = ttk.Button(
    button_frame,
    text="Start Clicking",
    command=self.start_clicking
)
```

#### 3. Threading
Clicking happens in a separate thread to prevent GUI freezing:
```python
self.click_thread = threading.Thread(target=self.click_worker, daemon=True)
self.click_thread.start()
```

#### 4. Event Handling
The application responds to user actions:
```python
def setup_bindings(self):
    self.root.bind('<F6>', lambda e: self.toggle_clicking())
    self.root.bind('<Escape>', lambda e: self.stop_clicking())
```

#### 5. Variables and State Management
tkinter variables automatically update the GUI:
```python
self.status_var = tk.StringVar(value="Ready")
self.total_clicks_var = tk.IntVar(value=0)
```

### Key Programming Concepts

#### Error Handling
```python
try:
    # Code that might fail
    pyautogui.click(button=self.mouse_button_var.get())
except pyautogui.FailSafeException:
    # Handle specific errors
    self.show_failsafe_message()
```

#### Threading Safety
```python
# Update GUI from worker thread
self.root.after(0, self.stop_clicking)
```

#### Input Validation
```python
def validate_settings(self):
    if self.cps_var.get() <= 0:
        messagebox.showerror("Error", "Clicks per second must be greater than 0")
        return False
    return True
```

## Building Executable

See the `build_executable.py` script for creating standalone executables for different platforms.

## Troubleshooting

### Common Issues

#### 1. "pyautogui not found"
**Solution**: Install pyautogui
```bash
pip install pyautogui
```

#### 2. "Permission denied" on macOS
**Solution**: Grant accessibility permissions:
1. System Preferences → Security & Privacy → Privacy → Accessibility
2. Add Python or your terminal application

#### 3. Clicking stops unexpectedly
**Cause**: Fail-safe triggered (mouse moved to corner)
**Solution**: This is intentional for safety. Keep mouse away from screen corners.

#### 4. GUI not responding
**Cause**: Blocking operation in main thread
**Solution**: Already handled by using separate thread for clicking

### Platform-Specific Notes

#### macOS
- May require accessibility permissions
- Use `python3` instead of `python` if needed

#### Linux
- May need to install `python3-tk` package
- Some distributions require `xdotool` for automation

#### Windows
- Usually works out of the box
- Windows Defender might flag the executable (false positive)

## Contributing

### Code Style
This project follows PEP 8 guidelines:
- Use 4 spaces for indentation
- Keep lines under 79 characters when possible
- Use descriptive variable names
- Include docstrings for all functions and classes

### Adding Features
1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guidelines
4. Add appropriate error handling
5. Test on multiple platforms
6. Submit a pull request

### Reporting Issues
Please include:
- Python version
- Operating system
- Steps to reproduce
- Error messages (if any)

## License

This project is for educational purposes. Use responsibly and in accordance with your local laws and the terms of service of any applications you interact with.

## Disclaimer

This tool is designed for legitimate automation tasks. Users are responsible for ensuring they comply with the terms of service of any applications they use this tool with. The authors are not responsible for any misuse of this software.
