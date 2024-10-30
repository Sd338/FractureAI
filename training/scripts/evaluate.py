import os
import sys
import cv2
import numpy as np

# Get the absolute path of the script
script_path = os.path.abspath(__file__)

# Calculate the path to the project root (assuming the script is in training/scripts)
project_root = os.path.abspath(os.path.join(os.path.dirname(script_path), '..', '..'))

# Add the project root to the Python path
sys.path.insert(0, project_root)

# Now try to import the FractureDetector
try:
    from backend.app.models.yolo import FractureDetector
except ImportError as e:
    print(f"Error importing FractureDetector: {e}")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

def load_model(model_path, output_folder):
    # Load the FractureDetector model
    return FractureDetector(model_path, output_folder)

def evaluate_model(detector, validation_dataset_path, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over images in the validation dataset
    image_folder = os.path.join(validation_dataset_path, 'images')
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

    for image_file in image_files:
        # Load each image
        image_path = os.path.join(image_folder, image_file)

        try:
            # Perform inference
            detections = detector.detect_fractures(image_path, save_visualization=False)

            # Load the image for visualization
            image = cv2.imread(image_path)

            if image is None:
                print(f"Could not read image: {image_path}")
                continue

            # Draw bounding boxes on the image
            for detection in detections:
                x1, y1, x2, y2 = map(int, detection['coordinates'])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{detection['name']} ({detection['confidence']:.2f})"
                cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Save the result image with detections
            result_image_path = os.path.join(output_folder, f"detected_{image_file}")
            cv2.imwrite(result_image_path, image)
            print(f"Processed {image_file}, results saved to {result_image_path}")

        except Exception as e:
            print(f"Error processing {image_file}: {e}")

if __name__ == "__main__":
    model_path = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\outputs\model checkpoints\last.pt"
    output_folder = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"
    validation_dataset_path = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\datasets\Bone Fracture Detection\bone fracture detection.v4-v4.yolov8\valid"

    detector = load_model(model_path, output_folder)
    evaluate_model(detector, validation_dataset_path, output_folder)
