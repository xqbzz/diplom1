from diffusers import StableDiffusionXLPipeline
import os
import torch

def load_model(model_path):
    """Загрузка модели из указанного пути"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель не найдена по указанному пути: {model_path}")
    
    try:
        # Загрузка модели из локального пути
        pipe = StableDiffusionXLPipeline.from_pretrained(model_path)
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        print(f"Модель загружена: {model_path}")
        return pipe
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке модели: {e}")
