import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API keys for accessing external services
    GORQ_API_KEY_1 = os.getenv("GORQ_API_KEY_1")
    GORQ_API_KEY_2 = os.getenv("GORQ_API_KEY_2")
<<<<<<< HEAD
    GORQ_API_KEY_3 = os.getenv("GORQ_API_KEY_3")
    GORQ_API_KEY_4 = os.getenv("GORQ_API_KEY_4")
=======
>>>>>>> 1f693feac21ffb672e81a6a763c82a8b795f5d34

    # Rate limits for the model
    RATE_LIMIT_REQUESTS_PER_MINUTE = 30  # For llama-3.2-11b-text-preview
    RATE_LIMIT_REQUESTS_PER_DAY = 7000
    RATE_LIMIT_TOKENS_PER_MINUTE = 7000
    RATE_LIMIT_TOKENS_PER_DAY = 500000

    # Base URL for your API (adjust as needed)
    BASE_API_URL = "https://api.example.com"

    # Output and model paths
    OUTPUT_FOLDER = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"  # Adjust the path as needed
    MODEL_PATH = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\outputs\model checkpoints\last.pt"  # Adjust the path as needed

    # Other configuration settings can be added here
    DEBUG = True  # Set to False in production
    SECRET_KEY = os.getenv("SECRET_KEY")  # Use a secret key for security (if applicable)

# Example of accessing the configuration
if __name__ == "__main__":
    config = Config()
    print("GORQ API Key 1:", config.GORQ_API_KEY_1)
    print("Rate Limit (Requests per Minute):", config.RATE_LIMIT_REQUESTS_PER_MINUTE)
    print("Output Folder:", config.OUTPUT_FOLDER)
    print("Model Path:", config.MODEL_PATH)
