import cv2
import numpy as np
from fastapi import UploadFile

def preprocess_image(file: UploadFile):
    # Read the uploaded image
    img = cv2.imdecode(np.frombuffer(file.file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Resize the image to your model's input size
    img = cv2.resize(img, (224, 224))  # Adjust the size as needed
    img = img / 255.0  # Normalize to [0, 1]
    
    return img

def process_image(image: np.ndarray):
    # Simulated fracture detection logic
    mean_pixel_value = np.mean(image)
    has_fracture = mean_pixel_value < 0.5  # Dummy logic for demonstration

    return {
        "message": "Image processed successfully!",
        "status": "success",
        "fracture_detected": has_fracture
    }
