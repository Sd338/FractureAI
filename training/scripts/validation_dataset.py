import os
import cv2
import glob
import numpy as np
from torch.utils.data import Dataset

class ValidationDataset(Dataset):
    def __init__(self, image_folder, annotation_folder):
        self.image_folder = image_folder
        self.annotation_folder = annotation_folder
        self.image_files = glob.glob(os.path.join(image_folder, "*.jpg"))  # Adjust file type if necessary
        
        print(f"Found {len(self.image_files)} images in {self.image_folder}")  # Debugging line

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = self.image_files[idx]
        image = cv2.imread(image_path)
        
        # Load the corresponding annotation file
        annotation_file = os.path.join(self.annotation_folder, os.path.basename(image_path).replace('.jpg', '.txt'))  # Adjust if necessary
        with open(annotation_file, 'r') as f:
            annotations = f.readlines()
        
        # Process annotations
        boxes = []
        for line in annotations:
            parts = line.strip().split()
            class_id = int(parts[0])
            center_x = float(parts[1])
            center_y = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            boxes.append((class_id, center_x, center_y, width, height))

        print(f"Loaded image: {image_path} with {len(boxes)} boxes")  # Debugging line
        return image, np.array(boxes)

# If you want to test the dataset class directly
if __name__ == "__main__":
    val_image_folder = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\datasets\Bone Fracture Detection\bone fracture detection.v4-v4.yolov8\valid\images"
    val_annotation_folder = r"C:\Users\sd876\OneDrive\Desktop\FractureAI\training\datasets\Bone Fracture Detection\bone fracture detection.v4-v4.yolov8\valid\labels"
    dataset = ValidationDataset(val_image_folder, val_annotation_folder)

    # Test loading an item
    image, boxes = dataset[0]
    print(f"Image shape: {image.shape}, Boxes: {boxes}")
