import os
import torch
from torchvision import transforms
from PIL import Image
import time 

# Define the paths
MODEL_PATH = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\outputs\model checkpoints\last.pt"
OUTPUT_IMAGES_DIR = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"

# Ensure the output directory exists
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)

def load_model(model_name: str):
    """Load the specified model."""
    if model_name == "fracture_model":
        # Load the model
        model = torch.load(MODEL_PATH)
        model.eval()  # Set the model to evaluation mode
        return model
    else:
        raise ValueError(f"Model {model_name} is not recognized.")

def process_image(image: Image.Image):
    """Process the image for inference."""
    # Define your transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize to your model's input size
        transforms.ToTensor(),
    ])
    return transform(image).unsqueeze(0)  # Add batch dimension

def save_image(image: Image.Image, filename: str):
    """Save the processed image."""
    save_path = os.path.join(OUTPUT_IMAGES_DIR, filename)
    image.save(save_path)
    return save_path

async def handle_image_upload(file):
    """Handle image upload and processing."""
    # Read the uploaded file
    image = Image.open(file.file)
    
    # Process the image for model inference
    processed_image = process_image(image)
    
    # Load the model
    model = load_model("fracture_model")
    
    # Perform inference (add your inference logic here)
    with torch.no_grad():
        # Replace this with your model inference code
        predictions = model(processed_image)
        
    # Save the original image to the output directory
    original_filename = f"uploaded_image_{int(time.time())}.png"
    save_image(image, original_filename)
    
    # Return predictions (or any relevant information)
    return predictions.tolist()  # Convert predictions to list for JSON serialization
