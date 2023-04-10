import sys
import subprocess
import cv2
import numpy as np
import threading
from time import sleep
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow, QPushButton, QLabel, QComboBox, QLineEdit, QFileDialog
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("libcam UI v0.0.0.1")
        self.setGeometry(0, 70, 1024, 500)
        
        # Create dropdown menu for selecting resolution
        self.resolution_label = QLabel('Select resolution', self)
        self.resolution_label.move(10, 10)
        self.resolution_label.resize(120, 30)
        self.resolution_dropdown = QComboBox(self)
        self.resolution_dropdown.addItem("1920x1080")
        self.resolution_dropdown.addItem("1280x720")
        self.resolution_dropdown.addItem("640x480")
        self.resolution_dropdown.move(140, 10)
        self.resolution_dropdown.resize(110,30)
        
        # Create dropdown menu for selecting framerate
        self.framerate_label = QLabel('Select framerate', self)
        self.framerate_label.move(10, 50)
        self.framerate_label.resize(120, 30)
        self.framerate_dropdown = QComboBox(self)
        self.framerate_dropdown.addItem("30")
        self.framerate_dropdown.addItem("20")
        self.framerate_dropdown.addItem("10")
        self.framerate_dropdown.move(140, 50)
        self.framerate_dropdown.resize(110, 30)
        
        # Create output format selector button
        self.file_format_label = QLabel('Select file format', self)
        self.file_format_label.move(10, 90)
        self.file_format_label.resize(120, 30)
        self.file_format_dropdown = QComboBox(self)
        self.file_format_dropdown.addItem("mp4")
        self.file_format_dropdown.addItem("avi")
        self.file_format_dropdown.addItem("mkv")
        self.file_format_dropdown.addItem("h264")
        self.file_format_dropdown.move(140, 90)
        self.file_format_dropdown.resize(110, 30)
        
        # Create input field for filename
        self.filename_label = QLabel('Choose filename', self)
        self.filename_label.move(10, 130)
        self.filename_label.resize(140, 30)
        self.filename_input = QLineEdit(self)
        self.filename_input.move(140, 130)
        self.filename_input.resize(170, 30)
        
        self.filename_input_button = QPushButton('Enter', self)
        self.filename_input_button.move(310, 130)
        self.filename_input_button.resize(50, 30)
        self.filename_input_button.clicked.connect(self.choose_filename)
        
        self.filename_label = QLabel('Your chosen filename:', self)
        self.filename_label.move(10, 170)
        self.filename_label.resize(160, 30)
        self.filename_chosen_label = QLabel('No filename chosen.', self)
        self.filename_chosen_label.move(170, 170)
        self.filename_chosen_label.resize(200, 30)
        
        # Create save-folder button
        self.save_folder_button = QPushButton('Select save folder', self)
        self.save_folder_button.move(10, 210)
        self.save_folder_button.resize(140, 30)
        self.save_folder_button.clicked.connect(self.select_save_folder)
        
        self.save_folder_label = QLabel('No save folder selected.', self)
        self.save_folder_label.move(170, 210)
        self.save_folder_label.resize(200, 30)
        
        # Create preview button
        self.preview_button = QPushButton('Open preview', self)
        self.preview_button_checked = False
        self.preview_button.setCheckable(True)
        self.preview_button.move(10, 250)
        self.preview_button.resize(140, 30)
        
        self.preview_button.clicked.connect(self.preview_button_clicked)
        self.preview_button.setChecked(self.preview_button_checked)
        
        # Create a QLabel widget for the camera preview
        self.camera_preview_label = QLabel('Preview', self)
        self.camera_preview_label.move(370, 10)
        self.camera_preview_label.resize(480,360)
        self.camera_preview_label.hide() # Hide the label initially
                
        # Create Start/Stop button
        self.start_stop_button = QPushButton(self)
        self.start_stop_button_checked = False
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.setText("Start Recording")
        self.start_stop_button.setStyleSheet("background-color: green;font-weight: bold")
        self.start_stop_button.move(170, 250)
        self.start_stop_button.resize(140, 30)
        
        self.start_stop_button.clicked.connect(self.start_stop_button_clicked)
        self.start_stop_button.setChecked(self.start_stop_button_checked)
        
    def select_save_folder(self):
        save_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.save_folder_path = save_folder
        self.save_folder_label.setText(save_folder)
        
    def choose_filename(self):
        if self.filename_input.text() != "":
            filename_chosen = self.filename_input.text()
            self.filename_chosen_label.setText(filename_chosen + "." + self.file_format_dropdown.currentText())
        else:
            self.filename_chosen_label.setText("Filename can't be empty.")

    def start_stop_button_clicked(self, checked):
        if checked == True:
            self.start_stop_button.setText("Stop Recording")
            self.start_stop_button.setStyleSheet("background-color: red;font-weight: bold")
        elif checked == False:
            self.start_stop_button.setText("Start Recording")
            self.start_stop_button.setStyleSheet("background-color: green;font-weight: bold")
            
    def preview_button_clicked(self, checked):
        if checked == True:
            self.camera_preview_label.show()
            self.preview_button.setText("Close preview")
        elif checked == False:
            self.camera_preview_label.hide()
            self.preview_button.setText("Open preview")
            
    def start_camera(self):
        # Start the camera thread
        self.camera_thread = VideoThread()
        self.camera_thread.change_pixmap_signal.connect(self.show_frame)
        self.camera_thread.start()
        
    def show_frame(self, cv_img):
        # Convert the cv_img to a QPixmap and set it on the camera preview label
        qt_img = self.convert_cv_qt(cv_img)
        self.camera_preview_label.setPixmap(qt_img)
            
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window
window = MainWindow()
window.show() # IMPORTANT!! Windows are hidden by default.

# Start the event loop.
app.exec()

