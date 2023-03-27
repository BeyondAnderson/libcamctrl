import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QFileDialog

class RecordUI(QWidget):
    def __init__(self):
        super().__init__()

        # set up UI
        self.setWindowTitle("Record Video")
        self.setGeometry(100, 100, 400, 200)

        # create resolution drop-down menu
        self.resolution_label = QLabel(self)
        self.resolution_label.setText("Select Resolution:")
        self.resolution_label.move(10, 10)
        self.resolution_dropdown = QComboBox(self)
        self.resolution_dropdown.addItem("1920x1080")
        self.resolution_dropdown.addItem("1280x720")
        self.resolution_dropdown.addItem("640x480")
        self.resolution_dropdown.move(130, 10)

        # create framerate drop-down menu
        self.framerate_label = QLabel(self)
        self.framerate_label.setText("Select Framerate:")
        self.framerate_label.move(10, 50)
        self.framerate_dropdown = QComboBox(self)
        self.framerate_dropdown.addItem("30")
        self.framerate_dropdown.addItem("60")
        self.framerate_dropdown.addItem("120")
        self.framerate_dropdown.move(130, 50)

        # create filename input field
        self.filename_label = QLabel(self)
        self.filename_label.setText("Filename:")
        self.filename_label.move(10, 90)
        self.filename_input = QLabel(self)
        self.filename_input.move(130, 90)

        # create save folder button
        self.save_folder_button = QPushButton(self)
        self.save_folder_button.setText("Save Folder")
        self.save_folder_button.move(10, 130)
        self.save_folder_button.clicked.connect(self.select_save_folder)

        # create start button
        self.start_button = QPushButton(self)
        self.start_button.setText("Start Recording")
        self.start_button.move(130, 130)
        self.start_button.clicked.connect(self.start_recording)

        # create stop button
        self.stop_button = QPushButton(self)
        self.stop_button.setText("Stop Recording")
        self.stop_button.move(250, 130)
        self.stop_button.clicked.connect(self.stop_recording)

        # create preview button
        self.preview_button = QPushButton(self)
        self.preview_button.setText("Preview Recording")
        self.preview_button.move(10, 170)
        self.preview_button.clicked.connect(self.preview_recording)

    def select_save_folder(self):
        save_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.save_folder_path = save_folder

    def start_recording(self):
        # get resolution and framerate values
        resolution = self.resolution_dropdown.currentText()
        framerate = self.framerate_dropdown.currentText()

        # set up filename and path
        filename = self.filename_input.text()
        if filename == "":
            filename = "video"
        filepath = os.path.join(self.save_folder_path, filename + ".h264")

        # start recording
        cmd = "libcamera-vid -t 0 --width {0} --height {1} --framerate {2} --output {3}".format(
            resolution.split("x")[0], resolution.split("x")[1], framerate, filepath
        )
        self.process = subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def stop_recording(self):
        self.process.terminate()

        # convert to mp4
        input_file = os.path.join(self.save_folder_path, self.filename_input.text() + ".h264")
        output_file = os.path.join(self.save_folder_path, self.filename_input.text() + ".mp4")
        cmd = "MP4Box -add {0} {1}".format(input_file, output_file)
        subprocess.call(cmd.split())

    def preview_recording(self):
        # get resolution and framerate values
        resolution = self.resolution_dropdown.currentText()
        framerate = self.framerate_dropdown.currentText()

        # set up filename and path
        filename = self.filename_input.text()
        if filename == "":
            filename = "video"
        filepath = os.path.join(self.save_folder_path, filename + ".h264")

        # start preview
        cmd = "omxplayer -o local --fps {0} --win '0 0 800 600' {1}".format(
            framerate, filepath
        )
        subprocess.call(cmd.split())

    def closeEvent(self, event):
        # terminate process if still running
        if hasattr(self, "process"):
            self.process.terminate()

    def keyPressEvent(self, event):
        # stop recording on escape key press
        if event.key() == 16777216 and hasattr(self, "process"):
            self.process.terminate()

        if name == "main":
            app = QApplication(sys.argv)
            ui = RecordUI()
            ui.show()
            sys.exit(app.exec_())
