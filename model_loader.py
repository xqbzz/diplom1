from diffusers import StableDiffusionPipeline, StableDiffusionXLPipeline
from transformers import CLIPTokenizer
import os
import torch
import json

def is_sdxl_model(model_path):
    index_path = os.path.join(model_path, "model_index.json")
    if not os.path.exists(index_path):
        return False
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return any(k in json.dumps(data) for k in ["text_encoder_2", "tokenizer_2"])
    except Exception:
        return False

def load_model(model_path):
    """Загрузка модели (SD или SDXL)"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель не найдена по пути: {model_path}")
    
    try:
        is_xl = is_sdxl_model(model_path)
        print(f"[DEBUG] Загружаем из: {model_path}")
        print(f"[DEBUG] SDXL? → {is_xl}")

        if is_xl:
            print("🔹 Загрузка модели SDXL")
            pipe = StableDiffusionXLPipeline.from_pretrained(
                model_path,
                torch_dtype=torch.float32
            )
        else:
            print("🔸 Загрузка обычной модели SD")
            pipe = StableDiffusionPipeline.from_pretrained(
                model_path,
                torch_dtype=torch.float32,
                safety_checker=None
            )

        # 🔥 Отключаем NSFW фильтр и постобработку
        if hasattr(pipe, "safety_checker"):
            pipe.safety_checker = None
            pipe.requires_safety_checker = False
            print("⚠️ Safety checker отключён.")

        if hasattr(pipe, "feature_extractor"):
            pipe.feature_extractor = None
            print("⚠️ Feature extractor отключён.")

        # Подгружаем tokenizer вручную при необходимости
        if not hasattr(pipe, "tokenizer") or pipe.tokenizer is None:
            try:
                print("⚠️ Tokenizer не обнаружен — загружаем вручную...")
                pipe.tokenizer = CLIPTokenizer.from_pretrained(os.path.join(model_path, "tokenizer"))
                print("✅ Tokenizer успешно загружен вручную.")
            except Exception as te:
                raise RuntimeError(f"❌ Ошибка загрузки tokenizer: {te}")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        pipe.set_progress_bar_config(disable=True)
        print(f"✅ Используется устройство: {device.upper()}")
        print(f"✅ Модель загружена: {model_path}")
        print(f"DEBUG: is_xl={is_xl}")
        if hasattr(pipe, "vae"):
            print("✅ VAE присутствует")
        return pipe

    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке модели: {e}")
