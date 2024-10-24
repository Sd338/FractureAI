import os
import sys
from datetime import datetime
from typing import Dict, Any
from PIL import Image

# Add the current and parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.extend([current_dir, parent_dir])

# Import your model classes from the models directory
from models.yolo import FractureDetector
from models.llama import generate_response_based_on_yolo

# Constants
MODEL_PATH = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\outputs\model checkpoints\last.pt"
OUTPUT_FOLDER = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"
TEMP_DIR = "temp"

class FractureAnalysisSystem:
    def __init__(self, yolo_model_path: str, output_folder: str):
        self.fracture_detector = FractureDetector(model_path=yolo_model_path, output_folder=output_folder)

    def process_image(self, image: Image.Image, patient_id: str = None) -> Dict[str, Any]:
        try:
            temp_image_path = self._save_temp_image(image)
            detection_results = self.fracture_detector.detect_fractures(temp_image_path)

            # Generate report based on detection results
            report = self._generate_report(detection_results, patient_id)

            self._cleanup_temp_image(temp_image_path)

            return {
                "detection_results": detection_results,
                "report": report
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _save_temp_image(image: Image.Image) -> str:
        os.makedirs(TEMP_DIR, exist_ok=True)
        temp_image_path = os.path.join(TEMP_DIR, "uploaded_image.jpg")
        image.save(temp_image_path)
        return temp_image_path

    @staticmethod
    def _cleanup_temp_image(temp_image_path: str) -> None:
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

    def _generate_report(self, detection_results: Dict[str, Any], patient_id: str = None) -> str:
        prompt = f"""You are a medical AI assistant specializing in fracture analysis. Your role is to provide a detailed, empathetic response to fracture detection data. Your analysis should be thorough, compassionate, and easy for patients to understand.

Please structure your response as follows:

1. Formal Report Header:
   - Include the current date and time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
   - Patient ID: {patient_id if patient_id else "Not provided"}
   - Examining AI: Medical Fracture Analysis Assistant

2. Detailed Fracture Analysis:
   - Describe each detected fracture in detail
   - Specify the location, type, and severity of each fracture
   - Use clear, non-technical language when possible

3. Confidence Assessment:
   - Provide a confidence level for each detection
   - Explain what factors contribute to the confidence level
   - Mention any limitations or potential for false positives/negatives

4. Immediate Recommendations:
   - Suggest necessary immediate actions
   - Explain WHY each action is important
   - Describe HOW to perform each recommended action

5. Pain Management Guidelines:
   - Suggest appropriate pain management techniques
   - Include both medicinal and non-medicinal options
   - Emphasize the importance of following dosage instructions

6. Follow-up Care Instructions:
   - Recommend follow-up appointments and their timing
   - Suggest any additional tests or examinations needed
   - Explain the importance of adhering to the follow-up schedule

7. Important Precautions and Warnings:
   - List crucial precautions to take
   - Highlight any warning signs to watch for
   - Provide clear instructions on when to seek immediate medical attention

8. Emotional Support and Reassurance:
   - Offer words of encouragement and support
   - Acknowledge the patient's potential concerns or anxieties
   - Emphasize the importance of a positive outlook in recovery

9. Lifestyle Adjustments:
   - Suggest temporary lifestyle changes to aid recovery
   - Provide tips for adapting daily activities
   - Recommend exercises or physical therapy, if appropriate

10. Resources and Support:
    - Mention available support groups or educational resources
    - Suggest ways for family members to assist in the recovery process

Please analyze the following fracture detection data and provide recommendations based on this structure:

{detection_results}

Remember to maintain a compassionate and reassuring tone throughout your response, while providing accurate and helpful medical information."""

        # Call the LLaMA model's response generation function
        return generate_response_based_on_yolo(detection_results)

def main():
    system = FractureAnalysisSystem(MODEL_PATH, OUTPUT_FOLDER)
    image_path = r"C:\Users\sd876\Downloads\Facebook\fracture_detection_debug.jpg"
    
    with Image.open(image_path) as img:
        results = system.process_image(img, patient_id="P12345")
        
        # Debugging: Print the entire results to understand the output
        print("Results: ", results)

        # Check for detection results and report
        if 'error' in results:
            print("Error processing image:", results['error'])
        else:
            print("Detection Results:", results.get('detection_results', 'No detection results found'))
            print("\nGenerated Report:")
            print(results.get('report', 'No report generated'))

if __name__ == "__main__":
    main()
