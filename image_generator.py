from model_loader import load_model
from transformers import CLIPTokenizer
from PIL import Image
import torch
import os

class ImageGenerator:
    def __init__(self, model_path=None, device='cuda'):
        if not model_path:
            raise ValueError("Не указан путь к модели.")
        self.model_path = model_path
        self.model = load_model(model_path)

        # 💡 Страховка на случай, если tokenizer не подгрузился
        if not hasattr(self.model, "tokenizer") or self.model.tokenizer is None:
            try:
                tokenizer_path = os.path.join(self.model_path, "tokenizer")
                print(f"📥 Подгружаем tokenizer вручную из: {tokenizer_path}")
                self.model.tokenizer = CLIPTokenizer.from_pretrained(tokenizer_path)
                print("✅ Tokenizer подгружен вручную.")
            except Exception as e:
                raise RuntimeError(f"❌ Ошибка загрузки tokenizer: {e}")

    def generate_image(self, prompt, style, size, num_inference_steps=50):
        """Генерация изображения на основе текста, стиля и размера"""
        if not prompt:
            raise ValueError("Описание не может быть пустым.")
        
        # Добавление стиля в prompt
        if style and style != "не выбран":
            style_map = {
                "пиксель-арт": "pixelart style",
                "реалистичный": "realistic",
                "акварель": "watercolour style",
                "киберпанк": "cyberpunk style",
                "фэнтези": "fantasy style",
                "мультфильм": "cartoon style"
            }
            prompt += ", " + style_map.get(style, style)

        # Размер изображения
        try:
            width, height = map(int, size.split('x'))
        except Exception:
            width, height = 512, 512  # fallback по умолчанию

        # Генерация изображения
        try:
            result = self.model(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
                guidance_scale=7.5  # стандартная настройка качества
            )
            return result.images[0]
        except Exception as e:
            raise RuntimeError(f"Ошибка при генерации изображения: {e}")

    def save_image(self, image, path):
        """Сохранение изображения в файл"""
        try:
            image.save(path)
        except Exception as e:
            raise RuntimeError(f"Ошибка при сохранении изображения: {e}")
