import logging
import numpy as np
from PIL import Image

def load_image(image_path):
    """Load an image from the specified path."""
    try:
        image = Image.open(image_path)
        logging.info(f"Image loaded successfully from {image_path}.")
        return image
    except Exception as e:
        logging.error(f"Failed to load image from {image_path}: {e}")
        return None

def preprocess_image(image, target_size=(640, 640)):
    """Preprocess the image for YOLO model."""
    try:
        # Resize and convert to RGB
        image = image.resize(target_size)
        image = image.convert("RGB")
        logging.info(f"Image preprocessed to size {target_size}.")
        return np.array(image) / 255.0  # Normalize to [0, 1]
    except Exception as e:
        logging.error(f"Error in preprocessing image: {e}")
        return None

def draw_bounding_boxes(image, detections):
    """Draw bounding boxes on the image based on YOLO detections."""
    import cv2  # Make sure you have OpenCV installed
    try:
        image = np.array(image)
        for detection in detections:
            x1, y1, x2, y2 = detection['coordinates']
            label = detection['name']
            color = (255, 0, 0)  # Red color for bounding boxes

            # Draw rectangle
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # Draw label
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        logging.info("Bounding boxes drawn on the image.")
        return Image.fromarray(image)
    except Exception as e:
        logging.error(f"Error in drawing bounding boxes: {e}")
        return image

def format_detection_output(detections):
    """Format the YOLO detection output for reporting."""
    formatted_detections = []
    for detection in detections:
        formatted_detection = {
            "name": detection.get("name", "Unknown"),
            "class": detection.get("class", "Unknown"),
            "confidence": round(detection.get("confidence", 0.0), 2),
            "coordinates": detection.get("coordinates", [])
        }
        formatted_detections.append(formatted_detection)

    logging.info("Detection output formatted successfully.")
    return formatted_detections
