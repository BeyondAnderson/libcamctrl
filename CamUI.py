# Import the CameraUI class from CameraUI.py
import sys
from PyQt5.QtWidgets import QApplication
from CameraUI import RecordUI

def main():
    # Create a QApplication instance
    app = QApplication(sys.argv)
    # Create an instance of the CameraUI class
    cam_ui = RecordUI()
    # Start the UI
    cam_ui.show()
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
