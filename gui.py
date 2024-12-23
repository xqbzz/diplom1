import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from image_generator import ImageGenerator
from config import AVAILABLE_STYLES, AVAILABLE_SIZES
from logger import setup_logger

logger = setup_logger()

class ImageGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.generator = ImageGenerator()

    def initUI(self):
        self.setWindowTitle("Генератор Изображений ИИ")
        self.setGeometry(100, 100, 900, 700)

        # Поле для ввода текста
        self.prompt_label = QtWidgets.QLabel("Введите описание:", self)
        self.prompt_label.setGeometry(50, 50, 200, 30)
        self.prompt_input = QtWidgets.QLineEdit(self)
        self.prompt_input.setGeometry(50, 80, 700, 30)

        # Выпадающий список для выбора стиля
        self.style_label = QtWidgets.QLabel("Выберите стиль:", self)
        self.style_label.setGeometry(50, 130, 200, 30)
        self.style_dropdown = QtWidgets.QComboBox(self)
        self.style_dropdown.setGeometry(50, 160, 200, 30)
        self.style_dropdown.addItems(AVAILABLE_STYLES)

        # Выпадающий список для выбора размера изображения
        self.size_label = QtWidgets.QLabel("Выберите размер:", self)
        self.size_label.setGeometry(50, 200, 200, 30)
        self.size_dropdown = QtWidgets.QComboBox(self)
        self.size_dropdown.setGeometry(50, 230, 200, 30)
        self.size_dropdown.addItems(AVAILABLE_SIZES)

        # Кнопка для генерации изображения
        self.generate_button = QtWidgets.QPushButton("Создать изображение", self)
        self.generate_button.setGeometry(50, 280, 200, 40)
        self.generate_button.clicked.connect(self.generate_image)

        # Область для отображения изображения
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setGeometry(300, 50, 550, 550)
        self.image_label.setFrameShape(QtWidgets.QFrame.Box)

        # Статус-метка
        self.status_label = QtWidgets.QLabel("Статус: Ожидание ввода...", self)
        self.status_label.setGeometry(50, 600, 700, 30)

    def generate_image(self):
        prompt = self.prompt_input.text()
        style = self.style_dropdown.currentText()
        size = self.size_dropdown.currentText()

        if not prompt:
            self.status_label.setText("Статус: Пожалуйста, введите описание.")
            return

        self.status_label.setText("Статус: Генерация изображения...")
        QtWidgets.QApplication.processEvents()

        try:
            # Генерация изображения
            image = self.generator.generate_image(prompt, style, size)

            # Сохранение и отображение изображения
            image_path = f"generated_image_{style}_{size}.png"
            self.generator.save_image(image, image_path)
            self.display_image(image_path)

            self.status_label.setText("Статус: Изображение успешно создано.")
            logger.info(f"Image successfully generated: {image_path}")
        except Exception as e:
            self.status_label.setText(f"Статус: Ошибка - {e}")
            logger.error(f"Error generating image: {e}")

    def display_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio))
