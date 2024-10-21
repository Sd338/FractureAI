import sys
import os
import numpy as np
from PIL import Image

# Add the parent directory of 'backend' to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.helpers import save_uploaded_file, load_image, preprocess_image, clear_output_folder

# Define constants for testing
TEST_IMAGE_PATH = r"C:\Users\sd876\Downloads\Facebook\441276484_478017954788273_3491614684915675436_n.jpg"
OUTPUT_FOLDER = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\output_images"

# Test the save_uploaded_file function
def test_save_uploaded_file():
    # Ensure the test file is copied to the output folder
    save_uploaded_file(TEST_IMAGE_PATH, OUTPUT_FOLDER)
    print(f"File saved to: {OUTPUT_FOLDER}")

# Test the load_image function
def test_load_image():
    # Load the image and check its type
    image = load_image(TEST_IMAGE_PATH)
    assert isinstance(image, Image.Image), "Loaded object is not an instance of PIL.Image.Image"
    print("Image loaded successfully.")

# Test the preprocess_image function
def test_preprocess_image():
    # Preprocess the image and check the result's shape
    image = load_image(TEST_IMAGE_PATH)
    preprocessed_image = preprocess_image(image)
    assert isinstance(preprocessed_image, np.ndarray), "Preprocessed image is not a numpy array"
    print(f"Preprocessed image shape: {preprocessed_image.shape}")

# Test the clear_output_folder function
def test_clear_output_folder():
    # Clear the output folder and confirm it's empty
    clear_output_folder(OUTPUT_FOLDER)
    print(f"Output folder {OUTPUT_FOLDER} cleared.")

if __name__ == "__main__":
    test_save_uploaded_file()
    test_load_image()
    test_preprocess_image()
    test_clear_output_folder()
