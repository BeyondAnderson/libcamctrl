import tkinter as tk
import os

class CameraUI:
    def __init__(self, master):
        self.master = master
        master.title("Camera UI")

        # Create labels and dropdown menus for resolution, framerate, and output format
        resolution_label = tk.Label(master, text="Resolution:")
        resolution_label.grid(row=0, column=0, sticky="w")

        self.resolution_var = tk.StringVar()
        self.resolution_var.set("1920x1080")
        resolution_options = ["640x480", "1280x720", "1920x1080"]
        resolution_dropdown = tk.OptionMenu(master, self.resolution_var, *resolution_options)
        resolution_dropdown.grid(row=0, column=1)

        framerate_label = tk.Label(master, text="Framerate:")
        framerate_label.grid(row=1, column=0, sticky="w")

        self.framerate_var = tk.StringVar()
        self.framerate_var.set("30")
        framerate_options = ["30", "60", "120"]
        framerate_dropdown = tk.OptionMenu(master, self.framerate_var, *framerate_options)
        framerate_dropdown.grid(row=1, column=1)

        format_label = tk.Label(master, text="Output Format:")
        format_label.grid(row=2, column=0, sticky="w")

        self.format_var = tk.StringVar()
        self.format_var.set(".mp4")
        format_options = [".mp4", ".avi", ".mkv"]
        format_dropdown = tk.OptionMenu(master, self.format_var, *format_options)
        format_dropdown.grid(row=2, column=1)

        # Create labels and entry boxes for save folder and file name
        folder_label = tk.Label(master, text="Save Folder:")
        folder_label.grid(row=3, column=0, sticky="w")

        self.folder_entry = tk.Entry(master)
        self.folder_entry.grid(row=3, column=1)

        name_label = tk.Label(master, text="File Name:")
        name_label.grid(row=4, column=0, sticky="w")

        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=4, column=1)

        # Create start and stop buttons
        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.grid(row=5, column=0)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop, state="disabled")
        self.stop_button.grid(row=5, column=1)

    def start(self):
        # Get the selected options and file name
        resolution = self.resolution_var.get()
        framerate = self.framerate_var.get()
        format = self.format_var.get()
        folder = self.folder_entry.get()
        name = self.name_entry.get()

        # Create the command to start recording
        command = f"sudo libcamera-vid -r {resolution} -f {framerate} -o {os.path.join(folder, name+format)} &"

        # Start recording
        os.system(command)

        # Disable start button and enable stop button
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop(self):
        # Create the command to stop recording
        command = "sudo pkill libcamera-vid"

        # Stop recording
        os.system(command)

        # Enable start button and disable stop button
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraUI(root)
    root.mainloop()
