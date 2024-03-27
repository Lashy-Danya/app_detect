import json

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel,
                             QMessageBox, QPushButton)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from collections import Counter

from .menu import MenuBar
from .settings_window import SettingsWindow
from .settings_manager import SettingsManager
from .start_up_window import StartUpWindow
from .inference_thread import DetectionThread


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.detection_thread = None
        self.imgPath = None

        self.settings = SettingsManager()

        self.setWindowTitle("Test")
        self.setMinimumSize(600, 400)

        # Set Menu Bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Set Settings Window
        self.settings_window = SettingsWindow(self.settings)

        self.__initUI()

        self._checkShowStartUpWindow()

    def __initUI(self):
        centra_widget = QWidget(self)
        self.setCentralWidget(centra_widget)
        layout = QVBoxLayout()

        # Display area for Image
        self.image_label = QLabel("No Image Load")
        self.image_label.setScaledContents(True)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Button run detect
        self.run_inference_button = QPushButton("Run Inference", self)
        self.run_inference_button.clicked.connect(self.start_detection)
        layout.addWidget(self.run_inference_button)

        centra_widget.setLayout(layout)

    def _loadImage(self, imgPath):
        self.imgPath = imgPath
        pixmap = QPixmap(imgPath)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(),
                                                 Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setText("")

    def _showSettings(self):
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def _checkShowStartUpWindow(self):
        if self.settings.get_setting("show_dialog_on_start"):
            self.pop_up_window = StartUpWindow(self.settings)
            self.pop_up_window.show()

    def start_detection(self):
        if self.imgPath is None:
            QMessageBox.warning(self, "Warning", "No image has been loaded.")
            return

        class_names = {
            0: 'Marlboro',
            1: 'Kent',
            2: 'Camel',
            3: 'Parliament',
            4: 'Pall Mall',
            5: 'Monte Carlo',
            6: 'Winston',
            7: 'Lucky Strike',
            8: '2001',
            9: 'Lark' 
        }
        # Disable the main window or its components
        self.setEnabled(False)
        QMessageBox.information(self, "Processing", "Detection is running, please wait...")

        # Start the thread for detection
        self.detection_thread = DetectionThread(self.imgPath, cutoff=0.5, class_name=class_names)
        self.detection_thread.finished_signal.connect(self.on_detection_finished)
        self.detection_thread.error_signal.connect(self.on_detection_error)
        self.detection_thread.start()

    def on_detection_finished(self, result):
        image, detections = result
        # Re-enable the main window or its components
        self.setEnabled(True)

        self.process_detections(detections)

        # Convert the image to QPixmap and display it in the label
        # Assume image is in the correct format (if not, convert it before setting)
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        
        QMessageBox.information(self, "Success", "Detection completed successfully.")

    def on_detection_error(self, error_message):
        # Re-enable the main window or its components
        self.setEnabled(True)
        QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

    def process_detections(self, detections):
        # Count the number of detections for each class
        class_counts = Counter([det[1] for det in detections])  # Assuming det[1] is the class name

        # Write the counts to a text file
        with open("detection_counts.txt", "w") as file:
            for class_name, count in class_counts.items():
                file.write(f"{class_name}: {count}\n")
        
        # Optionally, write the counts to a JSON file for easier processing by other programs
        with open("detection_counts.json", "w") as file:
            json.dump(class_counts, file, indent=4)

        QMessageBox.information(self, "Detection Complete", "The detection counts have been written to detection_counts.txt and detection_counts.json.")
