import os
import pydicom
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import glob

# === 🔧 GLOBAL PATH SETTINGS ===
INPUT_PATH = "dicomData/stage_2_test_images"  # Can be a file or folder
OUTPUT_DIR = "dicomOutput"

# === 🔧 DICOM VIEWER FUNCTIONS ===
def load_dicom(path):
    return pydicom.dcmread(path)

def save_frame(frame, output_path, cmap='gray'):
    plt.imshow(frame, cmap=cmap)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"Saved: {output_path}")

def save_multiframe(dataset, base_output_path):
    pixel_array = dataset.pixel_array
    num_frames = pixel_array.shape[0]
    for i in range(num_frames):
        output_path = f"{base_output_path}_frame_{i+1}.png"
        save_frame(pixel_array[i], output_path)

def view_dicom(file_path):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(OUTPUT_DIR, filename)

    ds = load_dicom(file_path)
    if hasattr(ds, 'NumberOfFrames') and ds.NumberOfFrames > 1:
        save_multiframe(ds, output_path)
    else:
        save_frame(ds.pixel_array, f"{output_path}.png")

# === 🚀 MAIN ENTRYPOINT ===
if __name__ == '__main__':
    if not os.path.exists(INPUT_PATH):
        print(f"Input path does not exist: {INPUT_PATH}")
    elif os.path.isfile(INPUT_PATH):
        view_dicom(INPUT_PATH)
    elif os.path.isdir(INPUT_PATH):
        dicom_files = glob.glob(os.path.join(INPUT_PATH, "*.dcm"))
        if not dicom_files:
            print(f"No DICOM files found in folder: {INPUT_PATH}")
        else:
            for dicom_file in dicom_files:
                print(f"Processing: {dicom_file}")
                view_dicom(dicom_file)
    else:
        print("Invalid path.")
