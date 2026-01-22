import subprocess
import time
import pyautogui
import os

# Path to the GUI script
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "gui_main.py"))

def run_test():
    print(f"Starting QWDownloader: {script_path}")
    # Launch the application
    process = subprocess.Popen(["python", script_path])
    
    # Wait for the window to initialize
    time.sleep(3)
    
    # Use shortcut to start download
    print("Pressing Ctrl+D to start download...")
    pyautogui.hotkey('ctrl', 'd')
    
    print("Waiting 10 seconds...")
    time.sleep(10)
    
    # Terminate the process
    print("Terminating application...")
    process.terminate()
    print("Test completed.")

if __name__ == "__main__":
    run_test()
