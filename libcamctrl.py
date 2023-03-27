import os
import tkinter as tk
from tkinter import ttk


class CamController:
    def __init__(self, master):
        # Create UI elements
        name_label = tk.Label(master, text="File name:")
        name_label.grid(row=8, column=0, sticky="e")

        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=8, column=1)
        self.name_entry.insert(0, "")

        folder_label = tk.Label(master, text="Save folder:")
        folder_label.grid(row=9, column=0, sticky="e")

        self.folder_var = tk.StringVar(master)
        self.folder_menu = tk.OptionMenu(master, self.folder_var, os.path.expanduser("~"))
        self.folder_menu.grid(row=9, column=1, sticky="w")
        self.folder_var.trace("w", self.update_folder)

    def update_folder(self, *args):
        folder = self.folder_var.get()
        self.folder_menu['menu'].delete(0, 'end')

        for item in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, item)):
                self.folder_menu['menu'].add_command(label=item, command=tk._setit(self.folder_var, item))


class CameraUI:
    def __init__(self, master):
        # Create an instance of the CamController class
        self.controller = CamController(master)
        self.master = master
        master.title("Camera UI")

        # Create UI elements
        resolution_label = tk.Label(master, text="Resolution:")
        resolution_label.grid(row=5, column=0, sticky="e")

        self.resolution_var = tk.StringVar()
        self.resolution_var.set("1920x1080")
        resolution_options = ["640x480", "1280x720", "1920x1080"]
        resolution_dropdown = tk.OptionMenu(master, self.resolution_var, *resolution_options)
        resolution_dropdown.grid(row=5, column=1)

        framerate_label = tk.Label(master, text="Framerate:")
        framerate_label.grid(row=6, column=0, sticky="w")

        self.framerate_var = tk.StringVar()
        self.framerate_var.set("30")
        framerate_options = ["10", "20", "30", "60", "120"]
        framerate_dropdown = tk.OptionMenu(master, self.framerate_var, *framerate_options)
        framerate_dropdown.grid(row=6, column=1)

        format_label = tk.Label(master, text="Output Format:")
        format_label.grid(row=7, column=0, sticky="e")

        self.format_var = tk.StringVar(master)
        self.format_var.set(".mp4")
        format_menu = tk.OptionMenu(master, self.format_var, ".mp4", ".h264")
        format_menu.grid(row=7, column=1, sticky="w")

        name_label = tk.Label(master, text="File name:")
        name_label.grid(row=8, column=0, sticky="e")

        self.controller.name_entry.grid(row=8, column=1)

        folder_label = tk.Label(master, text="Save folder:")
        folder_label.grid(row=9, column=0, sticky="e")

        self.controller.folder_menu = tk.OptionMenu(master, self.controller.folder_var, os.path.expanduser("~"))
        self.controller.folder_menu.grid(row=9, column=1, sticky="w")
        self.controller.folder_var.trace("w", self.controller.update_folder)

        start_button = tk.Button(master, text="Start", command=self.start_recording)
        start_button.grid(row=10, column=0)

        stop_button = tk.Button(master, text="Stop", command=self.stop_recording, state="disabled")
        stop_button.grid(row=10, column=1)

        self.status_label = tk.Label(master, text="Camera UI by LAVETT")
        self.status_label.grid(row=11, column=0, columnspan=2)

    def start_recording(self):
        # Get the selected options and file name
        width, height = self.resolution_var.get().split("x")
        framerate = self.framerate_var.get()
        folder = self.folder_entry.get()
        name = self.name_entry.get()

        # Get the selected folder
        self.folder = self.folder_var.get()

        # Create the command to start recording
        command = f"sudo libcamera-vid --width {width} --height {height} --framerate {framerate} -t 0 -o {os.path.join(self.folder, name+'.h264')} &"

        # Start recording
        os.system(command)

        # Disable start button and enable stop button
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_recording(self):
        # Stop recording
        os.system("sudo pkill -SIGINT libcamera-vid")

        # Wait for recording to stop
        time.sleep(1)

        # Convert H.264 file to MP4 format
        convert_command = f"sudo ffmpeg -i {os.path.join(self.folder, self.name_entry.get()+'.h264')} -c:v copy -c:a copy {os.path.join(self.folder, self.name_entry.get()+'.mp4')}"
        os.system(f"{convert_command} && rm {os.path.join(self.folder, self.name_entry.get()+'.h264')}")

        # Disable stop button and enable start button
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraUI(root)
    root.mainloop()
