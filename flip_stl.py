import vtk
import os

# Directory containing the STL files
stl_path = '/home/kartik/Documents/gdrive/MeshSeg/dataset/'  # Set your directory path here
output_save_path = './flipped_stl_data'  # Set your output path here

# Get a list of all STL files in the directory
stl_files = [f for f in os.listdir(stl_path) if f.endswith('.stl')]

# Iterate over each STL file in the directory
for stl_file in stl_files:
    # Read the STL file
    reader = vtk.vtkSTLReader()
    reader.SetFileName(os.path.join(stl_path, stl_file))  # Use full path to read the file
    reader.Update()

    # Get the polydata
    polydata = reader.GetOutput()

    # Flip along the X-axis
    transform = vtk.vtkTransform()
    transform.Scale(-1, 1, 1)  # Flip the X-axis by scaling it with -1

    # Apply the transformation
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputData(polydata)
    transformFilter.SetTransform(transform)
    transformFilter.Update()

    # Define the output file name
    output_file_name = stl_file.replace('.stl', '_flipped.stl')

    # Write the flipped mesh to a new file
    writer = vtk.vtkSTLWriter()
    writer.SetFileName(os.path.join(output_save_path, output_file_name))  # Save to the output directory
    writer.SetInputData(transformFilter.GetOutput())
    writer.Write()
