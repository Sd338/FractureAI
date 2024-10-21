import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.yolo import FractureDetector
from app.models.llama import generate_response_based_on_yolo

def main():
    # Define paths
    model_path = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\outputs\model checkpoints\last.pt"
    image_path = r"C:\Users\sd876\Downloads\Facebook\441276484_478017954788273_3491614684915675436_n.jpg"
    output_folder = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"

    # Initialize FractureDetector
    detector = FractureDetector(model_path, output_folder)

    try:
        # Detect fractures
        yolo_results = detector.detect_fractures(image_path, conf_threshold=0.25)

        if yolo_results:
            print("\nFracture(s) Detected.")
            print("\nYOLO Detection Results:")
            for idx, detection in enumerate(yolo_results, 1):
                print(f"\nDetection {idx}:")
                print(f"Type: {detection['name']}")
                print(f"Confidence: {detection['confidence']:.4f}")
                print(f"Location: ({detection['coordinates'][0]:.2f}, {detection['coordinates'][1]:.2f})")

            # Generate detailed response using LLaMA model
            llama_response = generate_response_based_on_yolo(yolo_results)
            print("\nDetailed Analysis from Fracture AI:")
            print(llama_response)
        else:
            print("\nNo fractures detected.")

        print(f"\nDebug image saved in: {output_folder}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()