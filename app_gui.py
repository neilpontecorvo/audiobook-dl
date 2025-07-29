import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import subprocess
import sys

class AudiobookDownloaderApp:
    def __init__(self, root):
        self.root = root
        root.title("Audiobook Downloader")
        root.geometry("600x450")

        # --- UI Elements ---
        self.url_label = tk.Label(root, text="Audiobook URL:")
        self.url_label.pack(pady=(10, 2))
        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.pack(pady=(0, 10), padx=20)

        self.path_label = tk.Label(root, text="Save Location:")
        self.path_label.pack(pady=(5, 2))
        self.path_frame = tk.Frame(root)
        self.path_frame.pack(pady=(0, 10))
        self.path_entry = tk.Entry(self.path_frame, width=45)
        self.path_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.browse_button = tk.Button(self.path_frame, text="Browse...", command=self.browse_folder)
        self.browse_button.pack(side=tk.LEFT)

        self.download_button = tk.Button(root, text="Download Audiobook", command=self.start_download_thread, font=("Helvetica", 12, "bold"))
        self.download_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status Log:")
        self.status_label.pack(pady=(5,2))
        self.status_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70, bg="black", fg="white")
        self.status_text.pack(pady=10, padx=20, expand=True, fill='both')
        self.status_text.config(state='disabled')
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def log_status(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')

    def start_download_thread(self):
        url = self.url_entry.get()
        output_path = self.path_entry.get()

        if not url or not output_path:
            self.log_status("Error: Please provide both a URL and a save location.\n")
            return

        self.download_button.config(state="disabled")
        
        download_thread = threading.Thread(
            target=self.run_script, 
            args=(url, output_path)
        )
        download_thread.start()

    def run_script(self, url, output_path):
        # CORRECTED COMMAND: Runs the 'audiobookdl' module
        command = [
            sys.executable,
            "-u",
            "-m",
            "audiobookdl",
            "download", # Specify the 'download' subcommand
            "--output-dir",
            output_path,
            url
        ]
        
        try:
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                encoding='utf-8'
            )
            
            for line in iter(process.stdout.readline, ''):
                self.log_status(line)
            
            process.stdout.close()
            process.wait()
            
            if process.returncode == 0:
                self.log_status("\nDownload finished successfully! 🎉\n")
            else:
                self.log_status(f"\nScript finished with an error (code: {process.returncode}).\n")
                
        except Exception as e:
            self.log_status(f"An unexpected error occurred: {e}\n")
        finally:
            self.download_button.config(state="normal")


if __name__ == "__main__":
    main_window = tk.Tk()
    app = AudiobookDownloaderApp(main_window)
    main_window.mainloop()