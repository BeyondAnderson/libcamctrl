import tkinter as tk
import subprocess

class VideoRecorderUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Resolution label
        self.resolution_label = tk.Label(self, text="Resolution:")
        self.resolution_label.grid(row=0, column=0)

        # Resolution entry
        self.resolution_entry = tk.Entry(self)
        self.resolution_entry.grid(row=0, column=1)

        # Frame rate label
        self.fps_label = tk.Label(self, text="Frame rate:")
        self.fps_label.grid(row=1, column=0)

        # Frame rate entry
        self.fps_entry = tk.Entry(self)
        self.fps_entry.grid(row=1, column=1)

        # Output format label
        self.format_label = tk.Label(self, text="Output format:")
        self.format_label.grid(row=2, column=0)

        # Output format entry
        self.format_entry = tk.Entry(self)
        self.format_entry.grid(row=2, column=1)

        # File name label
        self.filename_label = tk.Label(self, text="File name:")
        self.filename_label.grid(row=3, column=0)

        # File name entry
        self.filename_entry = tk.Entry(self)
        self.filename_entry.grid(row=3, column=1)

        # Save folder label
        self.folder_label = tk.Label(self, text="Save folder:")
        self.folder_label.grid(row=4, column=0)

        # Save folder entry
        self.folder_entry = tk.Entry(self)
        self.folder_entry.grid(row=4, column=1)

        # Start button
        self.start_button = tk.Button(self, text="Start", command=self.start_recording)
        self.start_button.grid(row=5, column=0)

        # Stop button
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=5, column=1)

    def start_recording(self):
        resolution = self.resolution_entry.get()
        fps = self.fps_entry.get()
        format = self.format_entry.get()
        filename = self.filename_entry.get()
        folder = self.folder_entry.get()

        # Build the command string
        cmd = f"libcamera-vid -r {resolution} -f {fps} -o {folder}/{filename}.{format}"

        # Start the recording process
        self.recording_process = subprocess.Popen(cmd, shell=True)

        # Disable the start button and enable the stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        # Send SIGINT to the recording process to stop it
        self.recording_process.send_signal(subprocess.signal.SIGINT)

        # Enable the start button and disable the stop button
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

root = tk.Tk()
app = VideoRecorderUI(master=root)
app.mainloop()