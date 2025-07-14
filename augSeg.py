import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import os

# Configuration
input_image_path = "1000.png"  # Path to grayscale image
output_dir = "augmented_images_no_spatial"
num_augmented_images = 10

# Augmentation pipeline (NO spatial transforms)
transform = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),  # brightness/contrast tweaks
    A.GaussNoise(var_limit=(10.0, 50.0), mean=0, p=0.3),  # noise
    A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=0.2),  # sensor noise
    A.MotionBlur(blur_limit=3, p=0.1),  # slight blur simulating motion
    A.MedianBlur(blur_limit=3, p=0.1),  # median blur
    A.ShiftScaleRotate(shift_limit=0, scale_limit=0, rotate_limit=0, p=0),  # explicitly no spatial changes
    A.Normalize(mean=(0.5,), std=(0.5,)),
    ToTensorV2()
])

# Load grayscale image
image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError(f"Image '{input_image_path}' not found.")

os.makedirs(output_dir, exist_ok=True)

# Generate augmented images
for i in range(num_augmented_images):
    augmented = transform(image=image)["image"]
    augmented_np = (augmented.squeeze().numpy() * 255).astype("uint8")
    output_path = os.path.join(output_dir, f"augmented_{i+1}.png")
    cv2.imwrite(output_path, augmented_np)
    print(f"Saved augmented image: {output_path}")

print("Data augmentation complete.")
