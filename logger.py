import logging

def setup_logger():
    logger = logging.getLogger("ImageGenerator")
    handler = logging.FileHandler('image_generator.log')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
