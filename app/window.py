import sys

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QApplication, QToolTip)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

from .menu import MenuBar
from .settings_window import SettingsWindow
from .settings_manager import SettingsManager


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        self.settings = SettingsManager()

        self.setWindowTitle("Test")
        self.setMinimumSize(600, 400)

        # Set Menu Bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Set Settings Window
        self.settings_window = SettingsWindow(self.settings)

        self.__initUI()

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

        centra_widget.setLayout(layout)

    def _loadImage(self, imgPath):
        pixmap = QPixmap(imgPath)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(),
                                                 Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setText("")

    def _showSettings(self):
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    # def showEvent(self, event):
    #     screen = QApplication.primaryScreen().geometry()
    #     window_size = self.geometry()
    #     self.move(
    #         (screen.width() - window_size.width()) // 2,
    #         (screen.height() - window_size.height()) // 2
    #     )
    #     super(MainWindow, self).showEvent(event)
        