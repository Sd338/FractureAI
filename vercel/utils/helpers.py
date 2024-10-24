import os
import base64
from PIL import Image
import io
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_image(image_data: str) -> Dict[str, Any]:
    """
    Process the uploaded image data.
    
    :param image_data: Base64 encoded string or file path
    :return: A dictionary with processing results
    """
    try:
        if image_data.startswith('data:image/'):
            image = _process_base64_image(image_data)
        else:
            image = _load_image(image_data)

        processed_image = _perform_image_processing(image)

        result = {
            "format": processed_image.format,
            "size": processed_image.size,
            "mode": processed_image.mode,
            "message": "Image processed successfully"
        }

        logging.info("Image processed successfully")
        return result

    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise

def _process_base64_image(base64_data: str) -> Image.Image:
    """Convert base64 image data to a PIL image."""
    header, encoded = base64_data.split(',', 1)
    image_data = io.BytesIO(base64.b64decode(encoded))
    image = Image.open(image_data)

    logging.info("Base64 image processed successfully")
    return image

def _load_image(image_path: str) -> Image.Image:
    """Load an image from the file system."""
    if not os.path.exists(image_path):
        logging.error(f"Image file not found: {image_path}")
        raise FileNotFoundError(f"No such file: '{image_path}'")

    image = Image.open(image_path)
    logging.info(f"Image loaded from {image_path}")
    return image

def _perform_image_processing(image: Image.Image) -> Image.Image:
    """Perform any image processing required."""
    new_size = (800, 800)  # Resize to 800x800 pixels
    processed_image = image.resize(new_size)

    logging.info("Image resized to 800x800 pixels")
    return processed_image

def generate_filename(prefix="image", ext=".jpg") -> str:
    """Generates a unique filename with a specific prefix and extension."""
    import uuid
    return f"{prefix}_{uuid.uuid4().hex}{ext}"
