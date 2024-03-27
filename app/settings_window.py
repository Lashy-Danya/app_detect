from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QPushButton,
                             QToolTip, QApplication)
from PyQt5.QtCore import QTimer, QPoint


class PopupHint(QWidget):
    def __init__(self, parent=None, text="Popup", duration=2000, background_color="green", text_color="white", border_color="darkgreen"):
        super().__init__(parent)
        self.text = text
        self.duration = duration
        self.background_color = background_color
        self.text_color = text_color
        self.border_color = border_color

        self.initUI()

    def initUI(self):
        # Set tooltip style
        style = f"background-color: {self.background_color}; color: {self.text_color}; border: 1px solid {self.border_color};"
        QApplication.instance().setStyleSheet(f"QToolTip {{ {style} }}")

    def showBelowWidget(self, widget):
        # Calculate global position of the widget
        global_pos = widget.mapToGlobal(QPoint(0, widget.height()))
        # Adjust position to show the tooltip below the widget
        QToolTip.showText(global_pos, self.text)
        # Set a timer to hide the tooltip after the specified duration
        QTimer.singleShot(self.duration, QToolTip.hideText)


class SettingsWindow(QWidget):
    def __init__(self, settings) -> None:
        super(SettingsWindow, self).__init__()
        self.settings = settings
        self.settings_controls = {}

        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout(self)

        self.chk_show_dialog = QCheckBox("Show dialog on start")
        self.chk_show_dialog.setChecked(self.settings.get_setting("show_dialog_on_start"))
        self.layout.addWidget(self.chk_show_dialog)

        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.__save_settings)
        self.layout.addWidget(self.button_save)

        self.settings_controls = {
            'show_dialog_on_start': (self.chk_show_dialog, lambda x: x.isChecked())
        }

    def __save_settings(self):
        new_settings = {key: getter(widget) for key, (widget, getter) in self.settings_controls.items()}
        self.settings.update_settings(new_settings)
        
        popup = PopupHint(text="Settings saved", background_color="green", text_color="white",
                          border_color="darkgreen")
        popup.showBelowWidget(self.button_save)