import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube, Playlist
import threading

class YoutubeDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text="YouTube URL:").grid(row=0, column=0, sticky="w", pady=5)
        self.url_entry = ttk.Entry(self.master, width=40)
        self.url_entry.grid(row=0, column=1, columnspan=2, pady=5)

        ttk.Label(self.master, text="Output Path:").grid(row=1, column=0, sticky="w", pady=5)
        self.output_entry = ttk.Entry(self.master, width=30)
        self.output_entry.grid(row=1, column=1, pady=5)
        ttk.Button(self.master, text="Browse", command=self.browse_output_path).grid(row=1, column=2, pady=5)

        self.audio_only_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.master, text="Audio Only", variable=self.audio_only_var).grid(row=2, column=0, columnspan=3, pady=5)

        ttk.Label(self.master, text="Resolution:").grid(row=3, column=0, sticky="w", pady=5)
        self.resolution_var = tk.StringVar(value='360p')
        ttk.Combobox(self.master, textvariable=self.resolution_var, values=['360p', '720p', '1080p']).grid(row=3, column=1, columnspan=2, pady=5)

        ttk.Button(self.master, text="Download", command=self.start_download_thread).grid(row=4, column=0, columnspan=3, pady=10)

        self.status_label = ttk.Label(self.master, text="Status:")
        self.status_label.grid(row=5, column=0, sticky="w", pady=5)
        self.status_value_label = ttk.Label(self.master, text="")
        self.status_value_label.grid(row=5, column=1, columnspan=2, pady=5)

        self.file_count_label = ttk.Label(self.master, text="File Progress:")
        self.file_count_label.grid(row=6, column=0, sticky="w", pady=5)
        self.file_count_value_label = ttk.Label(self.master, text="")
        self.file_count_value_label.grid(row=6, column=1, columnspan=2, pady=5)

        self.file_index = 0
        self.total_files = 0

    def start_download_thread(self):
        # Start a new thread for the download process
        download_thread = threading.Thread(target=self.download_video)
        download_thread.start()

    def download_video(self):
        url = self.url_entry.get()
        output_path = self.output_entry.get()
        audio_only = self.audio_only_var.get()
        resolution = self.resolution_var.get()

        try:
            if 'playlist' in url.lower():
                playlist = Playlist(url)
                self.total_files = len(playlist.video_urls)
                for video_url in playlist.video_urls:
                    self.file_index += 1
                    self.download_single_video(video_url, output_path, audio_only, resolution)
            else:
                self.total_files = 1
                self.download_single_video(url, output_path, audio_only, resolution)
        except Exception as e:
            self.update_status_label(f"An error occurred: {e}")

    def download_single_video(self, url, output_path, audio_only, resolution):
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress_callback)

            if audio_only:
                video_stream = yt.streams.filter(only_audio=True).first()
            else:
                video_stream = yt.streams.filter(res=resolution).first()

            output_path = output_path or '.'

            self.update_status_label(f"Downloading {'audio' if audio_only else 'video'} {self.file_index}/{self.total_files}: {yt.title}")
            self.update_file_count_label(f"File Progress: {self.file_index}/{self.total_files}")

            video_stream.download(output_path)

            self.update_status_label(f"{'Audio' if audio_only else 'Video'} '{yt.title}' has been downloaded successfully.")
        except Exception as e:
            self.update_status_label(f"An error occurred: {e}")

    def on_progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        # Progress bar removed, not needed without it

    def update_status_label(self, status):
        self.status_value_label.config(text=status)

    def update_file_count_label(self, file_count):
        self.file_count_value_label.config(text=file_count)

    def browse_output_path(self):
        output_path = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, output_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderGUI(root)
    root.mainloop()
