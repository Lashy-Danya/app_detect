from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QPushButton,
                             QToolTip, QApplication, QLabel, QDoubleSpinBox,
                             QLineEdit, QHBoxLayout, QFileDialog, QSlider)
from PyQt5.QtCore import QTimer, QPoint, Qt


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
        layout = QVBoxLayout(self)

        # Show dialog on start checkbox
        self.chk_show_dialog = QCheckBox("Show dialog on start")
        self.chk_show_dialog.setChecked(self.settings.get_setting("show_dialog_on_start"))
        layout.addWidget(self.chk_show_dialog)

        # Cutoff value input
        layout.addWidget(QLabel("Cutoff value:"))
        self.cutoff_slider = QSlider(Qt.Horizontal)
        self.cutoff_slider.setMinimum(0)
        self.cutoff_slider.setMaximum(100)
        self.cutoff_slider.setValue(int(self.settings.get_setting("cutoff") * 100))
        self.cutoff_slider.setTickPosition(QSlider.TicksBelow)
        self.cutoff_slider.setTickInterval(1)

        self.cutoff_label = QLabel(str(self.cutoff_slider.value() / 100))
        self.cutoff_slider.valueChanged.connect(
            lambda value: self.cutoff_label.setText(str(value / 100))
        )

        cutoff_layout = QHBoxLayout()
        cutoff_layout.addWidget(self.cutoff_slider)
        cutoff_layout.addWidget(self.cutoff_label)
        layout.addLayout(cutoff_layout)

        # Class name file selection
        layout.addWidget(QLabel("Class names file:"))
        self.class_names_file = QLineEdit()
        self.class_names_file.setText(self.settings.get_setting("class_names_file"))
        self.class_names_file.setReadOnly(True)
        class_file_button = QPushButton("Choose File")
        class_file_button.clicked.connect(self.__chooseClassNamesFile)

        class_file_layout = QHBoxLayout()
        class_file_layout.addWidget(self.class_names_file)
        class_file_layout.addWidget(class_file_button)
        layout.addLayout(class_file_layout)

        # Model file selection
        layout.addWidget(QLabel("TFLite Model file:"))
        self.model_file = QLineEdit()
        self.model_file.setText(self.settings.get_setting("model_file"))
        self.model_file.setReadOnly(True)
        model_file_button = QPushButton("Choose File")
        model_file_button.clicked.connect(self.__chooseModelFile)

        model_file_layout = QHBoxLayout()
        model_file_layout.addWidget(self.model_file)
        model_file_layout.addWidget(model_file_button)
        layout.addLayout(model_file_layout)

        # Save button
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.__save_settings)
        layout.addWidget(self.button_save)

        self.settings_controls = {
            'show_dialog_on_start': (self.chk_show_dialog, lambda x: x.isChecked()),
            'cutoff': (self.cutoff_slider, lambda x: x.value() / 100),
            "class_names_file": (self.class_names_file, lambda x: x.text()),
            "model_file": (self.model_file, lambda x: x.text())
        }

    def __chooseClassNamesFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Class Names File", "", "JSON Files (*.json)")
        if file_name:
            self.class_names_file.setText(file_name)

    def __chooseModelFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select TFLite Model File", "", "TFLite Files (*.tflite)")
        if file_name:
            self.model_file.setText(file_name)

    def __save_settings(self):
        new_settings = {key: getter(widget) for key, (widget, getter) in self.settings_controls.items()}
        self.settings.update_settings(new_settings)
        
        popup = PopupHint(text="Settings saved", background_color="green", text_color="white",
                          border_color="darkgreen")
        popup.showBelowWidget(self.button_save)
