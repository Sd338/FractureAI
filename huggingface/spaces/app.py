import gradio as gr
from PIL import Image, ImageDraw
import sys
import os
import time
import threading

# Add the backend app to the system path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import models after updating the path
from backend.app.models.yolo import FractureDetector
from backend.app.models.llama import generate_response_based_on_yolo

# Initialize the fracture detector
MODEL_PATH = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\outputs\model checkpoints\last.pt"
OUTPUT_FOLDER = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"
detector = FractureDetector(MODEL_PATH, OUTPUT_FOLDER)

def delete_file_after_delay(file_path, delay):
    def delete_file():
        time.sleep(delay)
        try:
            os.remove(file_path)
            print(f"Temporary file {file_path} has been deleted.")
        except Exception as e:
            print(f"Error deleting temporary file: {e}")

    thread = threading.Thread(target=delete_file)
    thread.start()

def mark_fracture_area(image, detections):
    draw = ImageDraw.Draw(image)
    for detection in detections:
        x, y, w, h = detection['coordinates']
        draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
    return image

def analyze_image(input_image):
    # Save the uploaded image to a temporary location
    temp_image_path = os.path.join(OUTPUT_FOLDER, 'temp_uploaded_image.jpg')
    input_image.save(temp_image_path)

    try:
        # Perform fracture detection
        detections = detector.detect_fractures(temp_image_path, conf_threshold=0.25)

        # Mark the fracture areas on the image
        marked_image = mark_fracture_area(input_image.copy(), detections)

        # Generate analysis report
        analysis_report = generate_response_based_on_yolo(detections)

        # Schedule deletion of temporary file
        delete_file_after_delay(temp_image_path, 120)  # 120 seconds = 2 minutes

        return marked_image, analysis_report

    except Exception as e:
        return input_image, f"An error occurred during analysis: {str(e)}"

# Define the Gradio interface
iface = gr.Interface(
    fn=analyze_image,
    inputs=gr.Image(type="pil", label="Upload X-ray Image"),
    outputs=[
        gr.Image(type="pil", label="Output Image with Marked Fractures"),
        gr.Textbox(label="Fracture Analysis Report")
    ],
    title="Fracture Detection and Analysis System",
    description="Upload an X-ray image to detect fractures, view marked areas, and receive a detailed analysis report."
)

# Launch the Gradio interface
if __name__ == "__main__":
    iface.launch()
