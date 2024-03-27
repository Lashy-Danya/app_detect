from PyQt5.QtCore import QThread, pyqtSignal

from model.model_tflite import TFLiteModel

class DetectionThread(QThread):
    # Signals to indicate completion and pass the resulting image or an error message
    finished_signal = pyqtSignal(tuple)
    error_signal = pyqtSignal(str)

    def __init__(self, image_path, cutoff, class_name, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.cutoff = cutoff
        self.class_name = class_name
        self.model = TFLiteModel("C:\projects\coursework_detect\detect_mobilenet_320.tflite")

    def run(self):
        try:
            # Assume that do_sliding_window_inference is a method of TFLiteModel
            image, detections = self.model.do_sliding_window_inference(self.image_path, self.cutoff, self.class_name)
            self.finished_signal.emit((image, detections))  # If successful, emit the finished signal with the image
        except Exception as e:
            self.error_signal.emit(str(e))  # If there is an error, emit the error signal

