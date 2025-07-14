# Medical Scan Data Preprocessing Pipeline

A comprehensive toolkit for preprocessing, visualizing, and augmenting medical DICOM images, specifically designed for chest X-ray analysis and lung opacity detection tasks.

## 📋 Overview

This project provides a complete pipeline for medical image preprocessing with the following capabilities:
- DICOM file reading and metadata extraction
- Data augmentation for medical images
- 3D visualization of DICOM stacks
- Batch processing of medical imaging datasets

## 🗂️ Project Structure

```
medicalScanDataPreProc/
├── 3Ddicom.py              # 3D visualization of DICOM stacks
├── aug.py                  # Data augmentation with spatial transforms
├── augSeg.py               # Data augmentation without spatial transforms
├── dicomMetaData.py        # DICOM metadata extraction
├── dicomview.py            # DICOM to PNG conversion and visualization
├── 1000.png                # Sample image files
├── 1002.png                
├── augmented_images/       # Output: Augmented images with spatial transforms
├── augmented_images_no_spatial/ # Output: Augmented images without spatial transforms
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd medicalScanDataPreProc

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

#### View DICOM Metadata
```bash
python dicomMetaData.py
```

#### Convert DICOM to PNG
```bash
python dicomview.py
```

#### Generate Augmented Data
```bash
# With spatial transforms (rotations, flips)
python aug.py

# Without spatial transforms (brightness, noise only)
python augSeg.py
```

#### 3D Visualization
```bash
python 3Ddicom.py
```

## 📄 Script Details

### 🔍 `dicomMetaData.py`
**Purpose**: Extract and display DICOM metadata

**Features**:
- Read DICOM file headers
- Extract patient information, study details
- Display image dimensions and pixel spacing
- Useful for understanding dataset structure

**Usage**:
```python
import pydicom
ds = pydicom.dcmread('path/to/dicom/file.dcm')
print("Patient Name:", ds.get("PatientName", "N/A"))
print("Modality:", ds.get("Modality", "N/A"))
```

### 🖼️ `dicomview.py`
**Purpose**: Convert DICOM files to PNG format for visualization

**Features**:
- Batch conversion of DICOM to PNG
- Handles both single-frame and multi-frame DICOM files
- Automatic output directory creation
- Progress tracking for large datasets

**Configuration**:
```python
INPUT_PATH = "path/to/your/dicom/files"  # Input folder
OUTPUT_DIR = "dicomOutput"               # Output folder
```

### 🔄 `aug.py`
**Purpose**: Data augmentation with spatial transformations

**Augmentation Techniques**:
- **Spatial**: Random rotations (90°), small angle rotations (±10°)
- **Geometric**: Horizontal flips, elastic transforms, affine transforms
- **Intensity**: Brightness/contrast adjustment, Gaussian noise
- **Preprocessing**: Normalization to [-1, 1] range

**Medical Considerations**:
- ⚠️ **Horizontal flips**: Verify clinical validity (heart position)
- Small rotation angles to preserve anatomical orientation
- Conservative elastic transforms to avoid unrealistic deformations

### 🔄 `augSeg.py`
**Purpose**: Data augmentation without spatial transformations

**Augmentation Techniques** (Segmentation-safe):
- **Intensity Only**: Brightness/contrast, Gaussian noise, ISO noise
- **Blur Effects**: Motion blur, median blur
- **No Spatial Changes**: Preserves anatomical positioning

**Use Cases**:
- Segmentation tasks where spatial consistency is critical
- When anatomical orientation must be preserved
- Training models sensitive to spatial relationships

### 🎯 `3Ddicom.py`
**Purpose**: 3D visualization of DICOM image stacks

**Features**:
- Load and stack multiple DICOM slices
- Interactive 3D visualization with Napari
- Proper slice ordering and volume reconstruction
- Grayscale rendering optimized for medical images

**Requirements**:
- Napari viewer for 3D visualization
- DICOM files must be properly ordered by slice position

## 🛠️ Key Dependencies

### Core Libraries
- **pydicom**: DICOM file reading and processing
- **opencv-python**: Image processing and I/O
- **numpy**: Numerical computations
- **matplotlib**: Plotting and visualization

### Image Processing
- **scikit-image**: Advanced image processing (wavelet denoising)
- **albumentations**: Professional data augmentation
- **Pillow**: Basic image operations

### 3D Visualization
- **napari**: Interactive 3D medical image viewer
- **PyQt5**: GUI framework for napari

### Machine Learning
- **torch/torchvision**: PyTorch for tensor operations
- **pandas**: Data manipulation for CSV files

## ⚙️ Configuration

### Common Settings

**Input Images**: The scripts are configured to work with:
- `1000.png` and `1002.png` as sample images
- Any DICOM files you provide

**Output Directories**:
- `augmented_images/`: Augmented data with spatial transforms
- `augmented_images_no_spatial/`: Augmented data without spatial transforms
- `dicomOutput/`: PNG conversions from DICOM (created by dicomview.py)

**Augmentation Parameters**:
```python
# Number of augmented versions per image
num_augmented_images = 10

# Spatial transform limits
rotate_limit = 10  # degrees
brightness_limit = 0.2
contrast_limit = 0.2
```

## 🔬 Medical Imaging Best Practices

### Data Augmentation Guidelines
1. **Preserve Anatomical Integrity**: Avoid extreme transformations
2. **Clinical Validation**: Verify that augmentations are medically plausible
3. **Modality Awareness**: Different imaging modalities have different constraints
4. **Bias Prevention**: Ensure augmentations don't introduce artificial patterns

### Preprocessing Considerations
1. **Intensity Normalization**: Critical for consistent model performance
2. **Noise Reduction**: Balance between denoising and detail preservation
3. **Contrast Enhancement**: Improve visibility without over-enhancement
4. **Spatial Resolution**: Maintain clinically relevant image quality

## 📊 Performance Tips

### For Large Datasets
1. **Batch Processing**: Use the batch capabilities in `dicomview.py`
2. **Memory Management**: Process images in chunks for large volumes
3. **Parallel Processing**: Consider multiprocessing for CPU-intensive tasks
4. **Storage**: Use efficient formats (PNG for visualization, NPY for arrays)

### Optimization
```python
# Example: Efficient batch processing
import glob
dicom_files = glob.glob("path/to/dicom/files/*.dcm")
for dicom_file in dicom_files[:100]:  # Process first 100 files
    process_dicom(dicom_file)
```

## 🚨 Common Issues and Solutions

### DICOM Reading Problems
```python
# Handle corrupted or non-standard DICOM files
try:
    ds = pydicom.dcmread(file_path)
except Exception as e:
    print(f"Error reading {file_path}: {e}")
    continue
```

### Memory Issues with Large Volumes
```python
# Process slices individually instead of loading entire volume
for slice_file in sorted(slice_files):
    slice_data = pydicom.dcmread(slice_file).pixel_array
    # Process slice_data
    del slice_data  # Free memory
```

### Visualization Issues
- Ensure proper grayscale conversion: `cv2.IMREAD_GRAYSCALE`
- Check pixel value ranges before display
- Use appropriate colormaps for medical images (`'gray'`)

