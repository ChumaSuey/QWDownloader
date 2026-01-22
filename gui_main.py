import tkinter as tk
from tkinter import ttk, scrolledtext
import sv_ttk
import requests
import os
import time
import threading
from bs4 import BeautifulSoup

# Constants from main2.0.py
URL = "https://maps.quakeworld.nu/all/"
DEST_FOLDER = "./qwmaps"

class QWDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QWDownloader")
        self.root.geometry("600x450")
        
        self.is_downloading = False
        self.setup_ui()
        
        # Set Sun Valley Dark Theme
        sv_ttk.set_theme("dark")

    def setup_ui(self):
        # Main container with padding
        container = ttk.Frame(self.root, padding="20")
        container.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(container, text="QuakeWorld Map Downloader", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = ttk.Label(container, text="Downloads .bsp files from maps.quakeworld.nu", font=("Segoe UI", 10))
        desc_label.pack(pady=(0, 20))

        # Buttons frame
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.download_btn = ttk.Button(btn_frame, text="Start Download", style="Accent.TButton", command=self.start_download_thread)
        self.download_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_download)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn.configure(state="disabled")

        # Shortcuts
        self.root.bind("<Control-d>", lambda e: self.start_download_thread())
        self.root.bind("<Control-s>", lambda e: self.stop_download())

        # Log panel
        log_label = ttk.Label(container, text="Status Log:", font=("Segoe UI", 10, "bold"))
        log_label.pack(anchor=tk.W, pady=(10, 5))

        self.log_widget = scrolledtext.ScrolledText(container, height=15, font=("Consolas", 9), state='disabled', bg="#1e1e1e", fg="#ffffff", borderwidth=0)
        self.log_widget.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        """Thread-safe logging to the text panel."""
        self.root.after(0, self._log, message)

    def _log(self, message):
        self.log_widget.configure(state='normal')
        self.log_widget.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_widget.see(tk.END)
        self.log_widget.configure(state='disabled')

    def start_download_thread(self):
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.download_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        self.thread = threading.Thread(target=self.run_downloader, daemon=True)
        self.thread.start()

    def stop_download(self):
        self.is_downloading = False
        self.log("Stopping download...")
        self.stop_btn.configure(state="disabled")

    def verify_destination_folder(self):
        if not os.path.exists(DEST_FOLDER):
            os.makedirs(DEST_FOLDER)
            self.log(f"Created folder: {DEST_FOLDER}")

    def download_file(self, download_url, file_name):
        if not self.is_downloading:
            return False

        # Validator: Check if file already exists
        file_path = os.path.join(DEST_FOLDER, file_name)
        if os.path.exists(file_path):
            self.log(f"Skipping: {file_name} (Already exists)")
            return True

        try:
            self.log(f"Downloading: {file_name}...")
            response = requests.get(download_url)
            response.raise_for_status()
            with open(file_path, "wb") as file:
                file.write(response.content)
            self.log(f"Successfully downloaded: {file_name}")
            return True
        except Exception as e:
            self.log(f"Error downloading {file_name}: {e}")
            return False

    def run_downloader(self):
        try:
            self.verify_destination_folder()
            self.log("Accessing website...")
            response = requests.get(URL)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.find_all("tr")
            
            for row in rows:
                if not self.is_downloading:
                    break
                
                elements = row.find_all("td")
                if len(elements) == 3:
                    file_name = elements[0].text.strip()
                    if file_name.endswith(".bsp"):
                        download_link = elements[0].find("a")["href"]
                        download_url = URL + download_link
                        
                        if self.download_file(download_url, file_name):
                            time.sleep(1) # Reduced sleep for better UX, but still keeping a small break
            
            if self.is_downloading:
                self.log("Process complete!")
            else:
                self.log("Process stopped.")
                
        except Exception as e:
            self.log(f"Fatal Error: {e}")
        finally:
            self.is_downloading = False
            self.root.after(0, lambda: self.download_btn.configure(state="normal"))
            self.root.after(0, lambda: self.stop_btn.configure(state="disabled"))

if __name__ == "__main__":
    root = tk.Tk()
    app = QWDownloaderGUI(root)
    root.mainloop()
