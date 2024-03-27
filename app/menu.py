from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog


class MenuBar(QMenuBar):
    def __init__(self, parent=None) -> None:
        super(MenuBar, self).__init__(parent)
        self.parent = parent

        # File menu
        self.file_menu = self.addMenu('File')

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.openFile)
        self.file_menu.addAction(open_action)

        # Settings Menu
        self.settings_menu = self.addMenu("Settings")

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.openSettings)
        self.settings_menu.addAction(settings_action)

    def openFile(self):
        options = QFileDialog.Options()
        imgPath, _ = QFileDialog.getOpenFileName(self.parent, "Open Image", "",
                                                 "Image Files (*.png *.jpg *.jpeg *.JPG)",
                                                 options=options)
        if imgPath:
            self.parent._loadImage(imgPath)

    def openSettings(self):
        self.parent._showSettings()
