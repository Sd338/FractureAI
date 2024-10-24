import cv2
import torch
import numpy as np
from ultralytics import YOLO
import logging
from datetime import datetime
from pathlib import Path
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='fracture_detection.log'
)

class FractureDetector:
    def __init__(self, model_path: str, output_folder: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.output_folder = output_folder
        
        # Ensure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
        
        try:
            self.model = YOLO(model_path)
            self.model.to(self.device)
            logging.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise

    def preprocess_image(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at path: {image_path}")
        
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_clahe = clahe.apply(img_gray)
        
        # Slight Gaussian blur to reduce noise
        img_blurred = cv2.GaussianBlur(img_clahe, (3, 3), 0)
        
        return cv2.merge([img_blurred, img_blurred, img_blurred]), img

    def detect_fractures(self, image_path: str, conf_threshold: float = 0.25, save_visualization: bool = True):
        try:
            processed_image, original_image = self.preprocess_image(image_path)
            
            results = self.model(processed_image, device=self.device, conf=conf_threshold)
            detections = []
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    class_name = self.model.names[cls]
                    
                    detection = {
                        'coordinates': [float(x1), float(y1), float(x2), float(y2)],
                        'class': class_name,
                        'confidence': conf,
                        'name': f"{class_name} fracture"
                    }
                    detections.append(detection)

            if save_visualization and detections:
                self._save_visualization(original_image, detections)

            return detections

        except Exception as e:
            logging.error(f"Error in fracture detection: {e}")
            raise

    def _save_visualization(self, image, detections):
        img_viz = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = map(int, det['coordinates'])
            cv2.rectangle(img_viz, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det['name']} ({det['confidence']:.2f})"
            cv2.putText(img_viz, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = os.path.join(self.output_folder, f"detection_result_{timestamp}.jpg")
        cv2.imwrite(save_path, img_viz)
        logging.info(f"Visualization saved to {save_path}")

if __name__ == "__main__":
    model_path = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\outputs\model checkpoints\last.pt"
    image_path = r"C:\Users\sd876\Downloads\Facebook\441276484_478017954788273_3491614684915675436_n.jpg"
    output_folder = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"
    
    detector = FractureDetector(model_path, output_folder)
    
    try:
        results = detector.detect_fractures(image_path, conf_threshold=0.25)
        
        if results:
            print("\nFracture(s) Detected.")
            print("\nDetection Results:")
            for idx, detection in enumerate(results, 1):
                print(f"\nDetection {idx}:")
                print(f"Type: {detection['name']}")
                print(f"Confidence: {detection['confidence']:.4f}")
                print(f"Location: ({detection['coordinates'][0]:.2f}, {detection['coordinates'][1]:.2f})")
        else:
            print("\nNo fractures detected.")

        print(f"\nDebug image saved in: {output_folder}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error in main execution: {e}") 