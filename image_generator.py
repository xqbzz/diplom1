from model_loader import load_model
import torch
from PIL import Image

class ImageGenerator:
    def __init__(self, model=None):
        self.model = model or load_model()

    def generate_image(self, prompt, style, size):
        if not prompt:
            raise ValueError("Описание не может быть пустым.")
        
        # Добавление стиля в описание
        if style == "пиксель-арт":
            prompt += ", в стиле пиксель-арт"
        elif style == "реалистичный":
            prompt += ", очень детализированное и фотореалистичное"
        elif style == "акварель":
            prompt += ", в стиле акварели"
        elif style == "киберпанк":
            prompt += ", в стиле киберпанк"

        # Настройка размера изображения
        width, height = map(int, size.split('x'))

        # Генерация изображения
        try:
            image = self.model(prompt, height=height, width=width).images[0]
            return image
        except Exception as e:
            raise RuntimeError(f"Ошибка при генерации изображения: {e}")

    def save_image(self, image, path):
        image.save(path)
