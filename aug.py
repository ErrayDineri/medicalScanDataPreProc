import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import os

# ✅ Configuration
input_image_path = "1000.png"  # Path to preprocessed image
output_dir = "augmented_images"  # Output folder
num_augmented_images = 10  # How many augmented versions to generate

# ✅ Augmentation pipeline (safe for medical images)
transform = A.Compose([
    A.RandomRotate90(p=0.5),  # Random 90° rotations
    A.Rotate(limit=10, p=0.5),  # Small rotations [-10°, +10°]
    A.RandomBrightnessContrast(p=0.5),  # Simulate exposure differences
    A.GaussNoise(var_limit=(10.0, 50.0), mean=0, p=0.3),  # Simulate noise
    A.ElasticTransform(alpha=1, sigma=50, p=0.2),  # Simulate tissue deformation
    A.HorizontalFlip(p=0.5),  # Flip horizontally (check if clinically valid!)
    A.Affine(translate_percent=0.05, scale=1.0, rotate=0, shear=0, p=0.5),  # Small shifts
    A.Normalize(mean=(0.5,), std=(0.5,)),  # Normalize to [-1, 1]
    ToTensorV2()
])

# ✅ Load grayscale image
image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError(f"Image '{input_image_path}' not found.")

# ✅ Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# ✅ Generate and save augmented images
for i in range(num_augmented_images):
    augmented = transform(image=image)["image"]
    augmented_np = (augmented.squeeze().numpy() * 255).astype("uint8")  # Convert back to uint8
    output_path = os.path.join(output_dir, f"augmented_{i+1}.png")
    cv2.imwrite(output_path, augmented_np)
    print(f"✅ Saved augmented image: {output_path}")

print("✅ Data augmentation complete.")
