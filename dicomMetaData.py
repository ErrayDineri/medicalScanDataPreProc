import pydicom

ds = pydicom.dcmread('dicomData/stage_2_test_images/0000a175-0e68-4ca4-b1af-167204a7e0bc.dcm')

# Print all metadata (warning: very verbose)
print(ds)

# Access specific tags
print("Patient Name:", ds.get("PatientName", "N/A"))
print("Modality:", ds.get("Modality", "N/A"))
print("Study Date:", ds.get("StudyDate", "N/A"))
print("Image Size:", ds.Rows, "x", ds.Columns)
print("Pixel Spacing:", ds.get("PixelSpacing", "N/A"))
