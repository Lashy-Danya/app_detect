from PyQt5.QtCore import QThread, pyqtSignal

from model.model_tflite import TFLiteModel

class DetectionThread(QThread):
    # Signals to indicate completion and pass the resulting image or an error message
    finished_signal = pyqtSignal(tuple)
    error_signal = pyqtSignal(str)

    def __init__(self, model_path, image_path, cutoff, class_name, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.cutoff = cutoff
        self.class_name = class_name
        self.model = TFLiteModel(model_path)

    def run(self):
        try:
            image, detections = self.model.do_sliding_window_inference(self.image_path, self.cutoff, self.class_name)
            self.finished_signal.emit((image, detections))
        except Exception as e:
            self.error_signal.emit(str(e))
            print("Error in detection thread: ", e)
