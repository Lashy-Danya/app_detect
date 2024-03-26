import sys

from PyQt5.QtWidgets import QApplication

from app.window import MainWindow


def __center_window(app, window):
    screen = app.primaryScreen().geometry()
    window_size = window.geometry()
    window.move(
        (screen.width() - window_size.width()) // 2,
        (screen.height() - window_size.height()) // 2
    )

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    __center_window(app, window)

    window.show()
    app.exec_()

if __name__ == "__main__":
    main()