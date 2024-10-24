import os
import json
import logging
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEYS = [
    os.getenv("GORQ_API_KEY_1"),
    os.getenv("GORQ_API_KEY_2"),
    os.getenv("GORQ_API_KEY_3"),
    os.getenv("GORQ_API_KEY_4")
]

# Configure logging
logging.basicConfig(level=logging.INFO)

class GroqLlamaClient:
    def __init__(self):
        """Initialize the client with API keys and Groq API."""
        self.api_index = 0
        api_key = self.get_current_api_key()
        
        if api_key is None:
            logging.error("API key not found! Ensure GORQ_API_KEY_1 and GORQ_API_KEY_2 are set in the environment.")
            return

        self.client = Groq(api_key=api_key)
        logging.info(f"GroqLlamaClient initialized with API key index {self.api_index + 1}")

    def get_current_api_key(self):
        """Fetch the active API key."""
        return API_KEYS[self.api_index]

    def switch_api_key(self):
        """Switch to the next API key if the current one fails."""
        self.api_index = (self.api_index + 1) % len(API_KEYS)
        logging.info(f"Switching to API Key {self.api_index + 1}")
        self.client = Groq(api_key=self.get_current_api_key())

    def call_llama_model(self, yolo_data):
        """Call the LLaMA model with YOLO output data to generate a detailed response."""
        while True:
            try:
                logging.info("Preparing prompt for LLaMA model...")

                # Prepare the LLaMA model prompt based on YOLO data
                prompt = self.create_prompt(yolo_data)
                logging.info("Prompt prepared. Sending request to LLaMA model...")

                # Call Groq's LLaMA model
                completion = self.client.chat.completions.create(
                    model="llama-3.2-11b-text-preview",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=3000,
                    top_p=1,
                    stream=True,
                    stop=None
                )

                # Collect and format the response
                response = "".join([chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content])
                logging.info("Received response from LLaMA model.")
                return self.clean_response(response)

            except Exception as e:
                logging.error(f"Error with API: {e}")
                self.switch_api_key()

    def create_prompt(self, yolo_data):
        """Create a prompt to send to the LLaMA model based on YOLO output."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = f"""
        You are an expert medical AI specializing in analyzing fracture images.
        Current analysis is based on YOLO detection model's output. The report should include:
        1. Report header with current date and time ({current_time})
        2. Detailed analysis of detected fractures, including location and severity.
        3. Confidence in each diagnosis.
        4. Immediate recommendations (Why and How).
        5. Pain management suggestions.
        6. Follow-up care instructions.
        7. Precautions and warnings for the patient.

        YOLO data for analysis:
        {json.dumps(yolo_data, indent=2)}
        """
        logging.info("Prompt created successfully.")
        return prompt

    def clean_response(self, response):
        """Clean unwanted characters from the LLaMA model response."""
        return response.replace("*", "").replace("•", "").replace("#", "").replace("`", "").strip()

def format_confidence(confidence_score):
    """Format confidence score into descriptive text."""
    if confidence_score >= 0.85:
        return "High"
    elif confidence_score >= 0.65:
        return "Moderate"
    else:
        return "Low"

def generate_fracture_report(yolo_output):
    """Generate a fracture report based on YOLO output data."""
    llama_client = GroqLlamaClient()

    if not yolo_output:
        logging.warning("YOLO output is empty, no fractures detected.")
        return "Fracture Analysis Report: No fractures detected. If you're experiencing pain, consult a healthcare provider."

    # Construct detailed information from YOLO model output
    report_details = []
    for detection in yolo_output:
        logging.info(f"Processing detection: {detection}")
        report_details.append({
            "Fracture Type": detection.get('name', 'Unspecified fracture'),
            "Location": detection['class'],
            "Confidence": format_confidence(detection['confidence']),
            "Coordinates": detection['coordinates'],
            "Severity Notes": {
                "Displacement": "May require specialist assessment",
                "Soft Tissue Involvement": "Potential soft tissue damage"
            }
        })

    # Prepare data to send to LLaMA model
    yolo_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analysis_type": "Fracture Detection Report",
        "fractures_detected": report_details
    }

    # Call LLaMA model to generate detailed report
    report = llama_client.call_llama_model(yolo_data)
    
    logging.info("Fracture report generated successfully.")
    return report


# Testing with mock YOLO output (for debugging purposes)
if __name__ == "__main__":
    logging.info("Starting LLaMA model interaction...")

    # Mock YOLO output for testing
    mock_yolo_output = [
        {
            "name": "Fracture of the left radius",
            "class": "left arm",
            "confidence": 0.92,
            "coordinates": [100, 200, 150, 250]
        },
        {
            "name": "Fracture of the right tibia",
            "class": "right leg",
            "confidence": 0.87,
            "coordinates": [300, 400, 350, 450]
        }
    ]

    # Generate a report based on the mock output
    report = generate_fracture_report(mock_yolo_output)
    print(report)
