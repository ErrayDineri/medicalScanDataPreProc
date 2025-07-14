import os
import pydicom
import numpy as np
import napari

def load_dicom_stack(folder_path):
    # List all DICOM files, sorted by filename (make sure slices are in order)
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.dcm')])
    slices = []
    for f in files:
        ds = pydicom.dcmread(os.path.join(folder_path, f))
        slices.append(ds.pixel_array)
    volume = np.stack(slices, axis=0)
    return volume

if __name__ == '__main__':
    dicom_folder = "smallerSample"  # Set your folder path here
    volume = load_dicom_stack(dicom_folder)

    # Start Napari viewer and add the volume stack
    viewer = napari.Viewer()
    viewer.add_image(volume, name='DICOM Volume', colormap='gray')
    napari.run()
