from diffusers import StableDiffusionPipeline
import torch

def load_model(model_id="CompVis/stable-diffusion-v1-4"):
    # Загрузка модели
    try:
        pipe = StableDiffusionPipeline.from_pretrained(model_id)
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        return pipe
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке модели: {e}")
