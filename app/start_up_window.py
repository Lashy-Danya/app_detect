from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton


class StartUpWindow(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("Welcome!")
        layout = QVBoxLayout(self)

        message_label = QLabel("Welcome to the application!")
        layout.addWidget(message_label)

        self.chk_dont_show_again = QCheckBox("Don`t show this message again")
        layout.addWidget(self.chk_dont_show_again)

        button = QPushButton("Ok")
        button.clicked.connect(self.close_window)
        layout.addWidget(button)

    def close_window(self):
        if self.chk_dont_show_again.isChecked():
            self.settings.set_setting("show_dialog_on_start", False)
        self.close()