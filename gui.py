import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from image_generator import ImageGenerator
from config import AVAILABLE_STYLES, AVAILABLE_SIZES
from logger import setup_logger
from time import time
from downloader import ModelDownloader  # Импортируем класс для загрузки модели

logger = setup_logger()

from PyQt5.QtCore import QThread, pyqtSignal

class GenerationThread(QThread):
    finished = pyqtSignal(object, float)  # передаём PIL.Image
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    time_update = pyqtSignal(str)

    def __init__(self, generator, prompt, style, size, steps):
        super().__init__()
        self.generator = generator
        self.prompt = prompt
        self.style = style
        self.size = size
        self.steps = steps

    def run(self):
        try:
            start_time = time()
            img = self.generator.generate_image(self.prompt, self.style, self.size, self.steps)
            end_time = time()
            elapsed = end_time - start_time
            self.finished.emit(img, elapsed)
        except Exception as e:
            self.error.emit(str(e))

class ImageGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.generator = None  # Генератор инициализируется после загрузки модели
        self.downloader_thread = None  # Поток для загрузки модели
        self.model_path = os.path.join(os.getcwd(), "models")  # Папка для хранения моделей
        self.refresh_model_list()  # Обновляем список доступных моделей

    def initUI(self):
        # Настройка главного окна
        self.setWindowTitle("Генератор Изображений ИИ")
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f4f4;
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QStatusBar {
                font-size: 12px;
                font-family: Arial, sans-serif;
            }
        """)

        # Главный макет
        central_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Выбор папки для загрузки моделей
        self.folder_button = QtWidgets.QPushButton("Выбрать папку для моделей", self)
        self.folder_button.clicked.connect(self.select_folder)
        main_layout.addWidget(self.folder_button)

        # Кнопка загрузки модели
        self.download_button = QtWidgets.QPushButton("Загрузить модель", self)
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)

        # Прогресс-бар
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)

        # Статус загрузки
        self.status_label = QtWidgets.QLabel("Статус: Ожидание ввода...", self)
        self.status_label.setStyleSheet("color: #555;")
        main_layout.addWidget(self.status_label)

        # Поле для ввода описания
        form_layout = QtWidgets.QFormLayout()
        self.prompt_input = QtWidgets.QLineEdit(self)
        self.prompt_input.setPlaceholderText("Введите описание изображения...")
        form_layout.addRow("Описание:", self.prompt_input)

        # Выпадающий список для выбора модели
        self.model_dropdown = QtWidgets.QComboBox(self)
        form_layout.addRow("Модель:", self.model_dropdown)

        # Выпадающий список для выбора стиля
        self.style_dropdown = QtWidgets.QComboBox(self)
        self.style_dropdown.addItems(AVAILABLE_STYLES)
        form_layout.addRow("Стиль:", self.style_dropdown)

        # Выпадающий список для выбора размера
        self.size_dropdown = QtWidgets.QComboBox(self)
        self.size_dropdown.addItems(AVAILABLE_SIZES)
        form_layout.addRow("Размер:", self.size_dropdown)

        # Выпадающий список для выбора количества итераций
        self.iterations_dropdown = QtWidgets.QComboBox(self)
        self.iterations_dropdown.addItems(["25", "50", "100", "150"])  # Значения итераций
        form_layout.addRow("Количество итераций:", self.iterations_dropdown)

        main_layout.addLayout(form_layout)

        # Кнопка генерации изображения
        self.generate_button = QtWidgets.QPushButton("Создать изображение", self)
        self.generate_button.setFixedHeight(40)
        self.generate_button.clicked.connect(self.generate_image)
        main_layout.addWidget(self.generate_button)

        # Область для отображения изображения
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setFixedSize(600, 600)
        self.image_label.setStyleSheet("border: 2px solid #ccc; border-radius: 10px; background-color: white;")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)

        # Устанавливаем центральный виджет
        self.setCentralWidget(central_widget)

    def refresh_model_list(self):
        """Обновление списка доступных моделей"""
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

        self.model_dropdown.clear()  # Очищаем список моделей
        models = [name for name in os.listdir(self.model_path) if os.path.isdir(os.path.join(self.model_path, name))]
        if models:
            self.model_dropdown.addItems(models)
            self.status_label.setText("Доступные модели обновлены.")
        else:
            self.status_label.setText("Модели не найдены. Скачайте или добавьте модель.")

    def select_folder(self):
        """Открыть диалоговое окно для выбора папки"""
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку для моделей")
        if folder:
            self.model_path = folder
            self.refresh_model_list()  # Обновляем список моделей после смены папки
            self.status_label.setText(f"Выбрана папка: {folder}")
        else:
            self.status_label.setText("Папка не выбрана.")

    def start_download(self):
        """Начало загрузки выбранной модели"""
        if not self.model_path:
            self.status_label.setText("Пожалуйста, выберите папку для моделей.")
            return

        selected_model = self.model_dropdown.currentText()
        model_full_path = os.path.join(self.model_path, selected_model)

        self.downloader_thread = ModelDownloader(model_path=model_full_path)


        # Связываем сигналы с методами
        self.downloader_thread.progress.connect(self.progress_bar.setValue)
        self.downloader_thread.status.connect(self.update_status)
        self.downloader_thread.complete.connect(self.on_download_complete)

        # Запуск потока
        self.downloader_thread.start()

    def update_status(self, message):
        """Обновление статуса загрузки"""
        self.status_label.setText(f"Статус: {message}")

    def on_download_complete(self):
        """Действия при завершении загрузки"""
        self.status_label.setText("Статус: Загрузка завершена. Модель готова к использованию.")
        self.progress_bar.setValue(100)
        self.refresh_model_list()  # Обновляем список моделей после загрузки

    def generate_image(self):
        if not self.generator:
            selected_model = self.model_dropdown.currentText()
            self.status_label.setText("Загрузка модели...")
            QtWidgets.QApplication.processEvents()
            try:
                self.generator = ImageGenerator(model_path=os.path.join(self.model_path, selected_model))
            except Exception as e:
                self.status_label.setText(f"Ошибка загрузки модели: {e}")
                return

        prompt = self.prompt_input.text()
        style = self.style_dropdown.currentText()
        size = self.size_dropdown.currentText()
        iterations = int(self.iterations_dropdown.currentText())

        if not prompt:
            self.status_label.setText("Статус: Пожалуйста, введите описание.")
            return

        self.status_label.setText(f"Статус: Генерация изображения ({iterations} итераций)...")
    
        self.gen_thread = GenerationThread(self.generator, prompt, style, size, iterations)
        self.gen_thread.finished.connect(self.on_generation_finished)
        self.gen_thread.error.connect(self.on_generation_error)
        self.gen_thread.progress.connect(self.update_progress)  # новый слот для прогресса
        self.gen_thread.time_update.connect(self.update_time)  # новый слот для времени
        self.gen_thread.start()

    def on_generation_finished(self, image, elapsed):
        image_path = f"generated_image_{self.style_dropdown.currentText()}_{self.size_dropdown.currentText()}_{self.iterations_dropdown.currentText()}.png"
        self.generator.save_image(image, image_path)
        self.display_image(image_path)
        self.status_label.setText(f"Статус: Изображение успешно создано. Время: {elapsed:.1f} сек")
        self.progress_bar.setValue(100)


    def on_generation_error(self, message):
        self.status_label.setText(f"Статус: Ошибка генерации - {message}")
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_time(self, time_str):
        # Обновляем статус с прогрессом и временем
        current_text = self.status_label.text()
        # Можно просто показывать время отдельно или вместе со статусом
        self.status_label.setText(f"Статус: Генерация... {time_str}")

    def display_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
