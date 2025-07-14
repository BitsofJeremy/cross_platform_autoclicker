# Gemini Guidelines for cross_platform_autoclicker

This document provides instructions for Gemini on how to interact with this repository.

## Project Overview

This is a cross-platform auto-clicker GUI application built with Python's `tkinter` library. It allows users to configure and automate mouse clicks.

## Key Files

- `auto_clicker.py`: The main application script containing the GUI and core logic.
- `requirements.txt`: Lists the Python dependencies, primarily `pyautogui`.
- `build_executable.py`: A script used to create standalone executables.
- `README.md`: The primary source of project information.

## Development Workflow

- **To Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- **To Run the Application:**
  ```bash
  python auto_clicker.py
  ```
- **To Build an Executable:**
  ```bash
  python build_executable.py
  ```

## Gemini-Specific Instructions

1.  **Do Not Run the Application:** This is a GUI application that requires a desktop environment to run. Do not attempt to run `python auto_clicker.py` yourself. The user has indicated this is to be run on a remote server with a GPU. If you need to run the app, ask the user to run it and provide the logs.
2.  **Code Modifications:** When editing code, strictly adhere to the PEP 8 style guide as mentioned in the `README.md`.
3.  **Threading:** The application uses a separate thread for the clicking logic to keep the GUI responsive. When making changes, be mindful of thread safety. GUI updates from the worker thread should be done using `root.after()`.
4.  **Platform Differences:** Be aware of the platform-specific considerations mentioned in the `README.md` (e.g., macOS accessibility permissions, Linux dependencies).
5.  **Responsible Use:** This is an automation tool. When interacting with the user about its functionality, maintain a neutral and responsible tone.
