from model_loader import load_model
import torch
from PIL import Image


class ImageGenerator:
    def __init__(self, model_path=None,device='cuda'):
        """Инициализация генератора"""
        if not model_path:
            raise ValueError("Не указан путь к модели.")
        self.model = load_model(model_path)  # Загрузка модели с указанным путём

    def generate_image(self, prompt, style, size, num_inference_steps=50):
        """Генерация изображения на основе текста, стиля и размера"""
        if not prompt:
            raise ValueError("Описание не может быть пустым.")
        
        # Добавление стиля в описание
        if style == "пиксель-арт":
            prompt += ", pixelart style"
        elif style == "реалистичный":
            prompt += ", realistic"
        elif style == "акварель":
            prompt += ", watercolour style"
        elif style == "киберпанк":
            prompt += ", cyberpunk style"

        # Настройка размера изображения
        try:
            width, height = map(int, size.split('x'))
        except Exception:
            width, height = 1024, 1024


        # Генерация изображения
        try:
            image = self.model(
                prompt=prompt, 
                height=height, 
                width=width,
                num_inference_steps=num_inference_steps  # Количество итераций
            ).images[0]
            return image
        except Exception as e:
            raise RuntimeError(f"Ошибка при генерации изображения: {e}")

    def save_image(self, image, path):
        """Сохранение изображения в файл"""
        try:
            image.save(path)
        except Exception as e:
            raise RuntimeError(f"Ошибка при сохранении изображения: {e}")
