import os
from dotenv import load_dotenv
from groq import Groq
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
API_KEYS = [
    os.getenv("GORQ_API_KEY_1"),
    os.getenv("GORQ_API_KEY_2"),
    os.getenv("GORQ_API_KEY_3"),
    os.getenv("GORQ_API_KEY_4")
]

class GorQClient:
    def __init__(self):
        self.current_api_index = 0
        self.client = Groq(api_key=self.get_api_key())
        logging.info("GorQClient initialized with API key: %s", self.get_api_key())

    def switch_api_key(self):
        """Switch to the next available API key."""
        self.current_api_index = (self.current_api_index + 1) % len(API_KEYS)
        logging.info("Switched to API key index: %d", self.current_api_index)
        self.client = Groq(api_key=self.get_api_key())

    def get_api_key(self):
        """Get the current API key."""
        return API_KEYS[self.current_api_index]

    def call_llama_model(self, user_message):
        """Call the LLaMA model and return the response."""
        max_retries = len(API_KEYS)
        retries = 0
        
        while retries < max_retries:
            try:
                prompt = f"""You are a medical AI assistant specializing in fracture analysis. 
                Provide a detailed, empathetic response including:
                1. A formal report header with current date and time
                2. Detailed analysis of detected fractures
                3. Confidence assessment
                4. Immediate recommendations with explanations (Why and How)
                5. Pain management guidelines
                6. Follow-up care instructions
                7. Important precautions and warnings

                Analyze the following fracture detection data and provide recommendations:
                {user_message}
                """

                logging.info("Calling LLaMA model with user message.")
                completion = self.client.chat.completions.create(
                    model="llama-3.2-11b-text-preview",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=3290,
                    top_p=1,
                    stream=True,
                    stop=None
                )

                response = ""
                for chunk in completion:
                    response += chunk.choices[0].delta.content or ""

                # Clean up the response to remove formatting artifacts
                response = self.clean_response(response)

                logging.info("Response received from LLaMA model.")
                return response

            except Exception as e:
                logging.error(f"API error: {e}")
                self.switch_api_key()
                retries += 1
                logging.info("Retrying with new API key.")
        
        return "All API keys have been exhausted. Please try again later."

    def clean_response(self, response):
        """Remove any unwanted characters or formatting artifacts."""
        # Replace unwanted characters (e.g., stars) with empty strings
        response = response.replace("*", "")  # Remove stars
        response = response.replace("•", "")  # Remove bullet points
        response = response.replace("#", "")  # Remove hash symbols
        response = response.replace("`", "")  # Remove backticks
        response = response.strip()  # Trim any leading or trailing whitespace
        return response

def format_confidence_level(confidence):
    """Convert numerical confidence to descriptive text."""
    if confidence > 0.85:
        return "High"
    elif confidence > 0.65:
        return "Moderate"
    else:
        return "Low"

def generate_response_based_on_yolo(yolo_output):
    """Generate a detailed, personalized response based on YOLO model output."""
    gorq_client = GorQClient()

    if not yolo_output:
        return "Fracture Analysis Report: No fractures detected in the provided image. However, if you're experiencing pain or discomfort, please consult a healthcare professional for a thorough evaluation."

    # Process YOLO output to create detailed analysis
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details = []
    
    for detection in yolo_output:
        x1, y1, x2, y2 = detection['coordinates']
        cls = detection['class']
        conf = detection['confidence']
        name = detection.get('name', 'unspecified fracture')
        
        details.append({
            "fracture_type": name,
            "location": cls,
            "confidence_level": format_confidence_level(conf),
            "numerical_confidence": f"{conf:.4f}",
            "position": {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2
            },
            "severity_indicators": {
                "displacement": "Requires professional assessment",
                "surrounding_tissue": "Potential soft tissue involvement"
            }
        })

    # Construct detailed message for LLM
    user_message = json.dumps({
        "timestamp": current_time,
        "analysis_type": "Fracture Detection and Analysis",
        "detected_fractures": details,
        "request": "Provide a comprehensive analysis including immediate care recommendations, pain management strategies, and follow-up care instructions. Include specific details about each detected fracture and potential complications to watch for."
    }, indent=2)

    # Get detailed response from LLM
    response = gorq_client.call_llama_model(user_message)
    
    return response

# Test the functionality (This part should be executed in a separate test file or interactive environment)
if __name__ == "__main__":
    # Example YOLO output for testing
    example_yolo_output = [
        {
            "coordinates": [100, 150, 200, 300],
            "class": "fracture",
            "confidence": 0.87,
            "name": "radius fracture"
        }
    ]

    # Generate a response based on the example YOLO output
    response = generate_response_based_on_yolo(example_yolo_output)
    print(response)
