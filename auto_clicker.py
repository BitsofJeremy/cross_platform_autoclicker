#!/usr/bin/env python3
"""
Auto Clicker GUI Application
A modern GUI auto-clicker with customizable settings for macOS, Linux, and Windows.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import platform

try:
    import pyautogui
except ImportError:
    pyautogui = None


class AutoClickerGUI:
    """Main GUI class for the auto-clicker application."""
    
    def __init__(self):
        """Initialize the auto-clicker GUI."""
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_widgets()
        self.setup_bindings()
        
        # Clicking state
        self.is_clicking = False
        self.click_thread = None
        
        # Check if pyautogui is available
        if pyautogui is None:
            self.show_dependency_error()
    
    def setup_window(self):
        """Configure the main window properties."""
        self.root.title("Auto Clicker")
        self.root.geometry("400x700")
        self.root.resizable(False, False)
        
        # Set window icon and styling based on platform
        if platform.system() == "Darwin":  # macOS
            self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_variables(self):
        """Initialize tkinter variables."""
        self.cps_var = tk.DoubleVar(value=1.0)
        self.click_count_var = tk.IntVar(value=0)
        self.infinite_var = tk.BooleanVar(value=True)
        self.mouse_button_var = tk.StringVar(value="left")
        self.click_type_var = tk.StringVar(value="single")
        self.status_var = tk.StringVar(value="Ready")
        self.total_clicks_var = tk.IntVar(value=0)
    
    def setup_widgets(self):
        """Create and configure all GUI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Auto Clicker", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # CPS (Clicks Per Second) section
        cps_frame = ttk.LabelFrame(main_frame, text="Click Speed", padding="10")
        cps_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(cps_frame, text="Clicks per second:").grid(row=0, column=0, sticky=tk.W)
        
        cps_spinbox = ttk.Spinbox(
            cps_frame, 
            from_=0.1, 
            to=50.0, 
            increment=0.1,
            textvariable=self.cps_var,
            width=10,
            format="%.1f"
        )
        cps_spinbox.grid(row=0, column=1, sticky=tk.E)
        
        # Click count section
        count_frame = ttk.LabelFrame(main_frame, text="Click Count", padding="10")
        count_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(
            count_frame, 
            text="Infinite clicks", 
            variable=self.infinite_var, 
            value=True,
            command=self.toggle_click_count
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Radiobutton(
            count_frame, 
            text="Limited clicks:", 
            variable=self.infinite_var, 
            value=False,
            command=self.toggle_click_count
        ).grid(row=1, column=0, sticky=tk.W)
        
        self.count_spinbox = ttk.Spinbox(
            count_frame, 
            from_=1, 
            to=999999, 
            textvariable=self.click_count_var,
            width=10,
            state="disabled"
        )
        self.count_spinbox.grid(row=1, column=1, sticky=tk.E)
        
        # Mouse button section
        button_frame = ttk.LabelFrame(main_frame, text="Mouse Button", padding="10")
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(
            button_frame, 
            text="Left", 
            variable=self.mouse_button_var, 
            value="left"
        ).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(
            button_frame, 
            text="Right", 
            variable=self.mouse_button_var, 
            value="right"
        ).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Radiobutton(
            button_frame, 
            text="Middle", 
            variable=self.mouse_button_var, 
            value="middle"
        ).grid(row=0, column=2, sticky=tk.W)
        
        # Click type section
        type_frame = ttk.LabelFrame(main_frame, text="Click Type", padding="10")
        type_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(
            type_frame, 
            text="Single Click", 
            variable=self.click_type_var, 
            value="single"
        ).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(
            type_frame, 
            text="Double Click", 
            variable=self.click_type_var, 
            value="double"
        ).grid(row=0, column=1, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10))
        
        self.start_button = ttk.Button(
            button_frame, 
            text="Start Clicking", 
            command=self.start_clicking,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            button_frame, 
            text="Stop Clicking", 
            command=self.stop_clicking,
            state="disabled"
        )
        self.stop_button.pack(side=tk.LEFT)
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(status_frame, text="Total clicks:").grid(row=1, column=0, sticky=tk.W)
        clicks_label = ttk.Label(status_frame, textvariable=self.total_clicks_var)
        clicks_label.grid(row=1, column=1, sticky=tk.E)
        
        # Instructions
        instructions = ttk.Label(
            main_frame, 
            text="Instructions:\n1. Set your desired click speed and options\n2. Click 'Start Clicking'\n3. Position your mouse where you want to click\n4. Press F6 to start/stop clicking\n5. Press ESC to stop clicking",
            justify=tk.LEFT,
            font=("Arial", 9)
        )
        instructions.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_bindings(self):
        """Set up keyboard bindings."""
        self.root.bind('<F6>', lambda e: self.toggle_clicking())
        self.root.bind('<Escape>', lambda e: self.stop_clicking())
        self.root.focus_set()  # Allow window to receive key events
    
    def toggle_click_count(self):
        """Toggle the click count spinbox state."""
        if self.infinite_var.get():
            self.count_spinbox.configure(state="disabled")
        else:
            self.count_spinbox.configure(state="normal")
    
    def show_dependency_error(self):
        """Show error message if pyautogui is not installed."""
        messagebox.showerror(
            "Missing Dependency",
            "pyautogui is required for this application to work.\n\n"
            "Please install it using:\npip install pyautogui"
        )
    
    def validate_settings(self):
        """Validate user settings before starting."""
        if pyautogui is None:
            messagebox.showerror(
                "Error", 
                "pyautogui is not installed. Please install it first."
            )
            return False
        
        if self.cps_var.get() <= 0:
            messagebox.showerror("Error", "Clicks per second must be greater than 0")
            return False
        
        if not self.infinite_var.get() and self.click_count_var.get() <= 0:
            messagebox.showerror("Error", "Click count must be greater than 0")
            return False
        
        return True
    
    def start_clicking(self):
        """Start the auto-clicking process."""
        if not self.validate_settings():
            return
        
        if self.is_clicking:
            return
        
        self.is_clicking = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_var.set("Clicking...")
        self.total_clicks_var.set(0)
        
        # Start clicking in a separate thread
        self.click_thread = threading.Thread(target=self.click_worker, daemon=True)
        self.click_thread.start()
    
    def stop_clicking(self):
        """Stop the auto-clicking process."""
        if not self.is_clicking:
            return
        
        self.is_clicking = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_var.set("Stopped")
    
    def toggle_clicking(self):
        """Toggle between start and stop clicking."""
        if self.is_clicking:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def click_worker(self):
        """Worker thread for performing clicks."""
        if pyautogui is None:
            return
        
        # Set pyautogui settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0
        
        delay = 1.0 / self.cps_var.get()
        click_count = 0
        max_clicks = self.click_count_var.get() if not self.infinite_var.get() else float('inf')
        
        try:
            while self.is_clicking and click_count < max_clicks:
                # Perform the click
                if self.click_type_var.get() == "single":
                    pyautogui.click(button=self.mouse_button_var.get())
                else:  # double click
                    pyautogui.doubleClick(button=self.mouse_button_var.get())
                
                click_count += 1
                self.total_clicks_var.set(click_count)
                
                # Wait for the specified delay
                time.sleep(delay)
                
        except pyautogui.FailSafeException:
            self.root.after(0, lambda: messagebox.showinfo(
                "Fail-safe Triggered", 
                "Auto-clicking stopped due to mouse moved to corner (fail-safe)."
            ))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", 
                f"An error occurred during clicking: {str(e)}"
            ))
        finally:
            # Update UI in main thread
            self.root.after(0, self.stop_clicking)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main function to run the application."""
    try:
        app = AutoClickerGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
