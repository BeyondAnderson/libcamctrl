import tkinter as tk
import os

class CameraUI:
    def __init__(self, master):
        self.master = master
        master.title("Camera UI")
        self.controller = CamController(master)
        self.folder = None

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
        format_options = [".mp4"]
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

        # Add folder selection menu
        folder_label = tk.Label(self.frame, text="Save folder:")
        folder_label.grid(row=3, column=0, sticky="e")

        self.folder_var = tk.StringVar(self.frame)
        self.folder_var.set(os.path.expanduser("~"))
        folder_menu = tk.OptionMenu(self.frame, self.folder_var, os.path.expanduser("~"), command=self.controller.update_folder)
        folder_menu.grid(row=3, column=1, sticky="w")

    def start(self):
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

    def stop(self):
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
