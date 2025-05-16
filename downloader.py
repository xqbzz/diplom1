from PyQt5.QtCore import QThread, pyqtSignal
from diffusers import StableDiffusionXLPipeline

class ModelDownloader(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    complete = pyqtSignal()

    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path

    def run(self):
        try:
            self.status.emit("Загрузка модели из локальной папки...")
            pipe = StableDiffusionXLPipeline.from_pretrained(self.model_path)
            self.status.emit("Модель успешно загружена из локальной папки.")
            self.complete.emit()
        except Exception as e:
            self.status.emit(f"Ошибка загрузки модели: {e}")
