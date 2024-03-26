from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QPushButton


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
        self.chk_show_dialog.setCheckable(self.settings.get_setting("show_dialog_on_start"))
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
