import os
import vtk

# Define your file path
vtp_path = '/home/kartik/Documents/gdrive/MeshSeg/dataset/'
file_name = 'U1K5LD24_predicted_refined.vtp'  

# Read the mesh
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(vtp_path, file_name))
reader.Update()

# Get the polydata (mesh)
mesh = reader.GetOutput()

# Check if there are labels in the PointData or CellData
point_data = mesh.GetPointData()
cell_data = mesh.GetCellData()

print(f"Number of points: {mesh.GetNumberOfPoints()}")
print(f"Number of cells: {mesh.GetNumberOfCells()}")

# Checking for label data in PointData
if point_data.GetNumberOfArrays() > 0:
    print("Point Data Arrays:")
    for i in range(point_data.GetNumberOfArrays()):
        array_name = point_data.GetArrayName(i)
        print(f"- {array_name}")
        # Assuming the array contains integer labels, we can retrieve and print the values
        array = point_data.GetArray(i)
        if array:
            for j in range(array.GetNumberOfTuples()):
                print(f"  Point {j}: {array.GetValue(j)}")
else:
    print("No Point Data.")

# Checking for label data in CellData
if cell_data.GetNumberOfArrays() > 0:
    print("Cell Data Arrays:")
    for i in range(cell_data.GetNumberOfArrays()):
        array_name = cell_data.GetArrayName(i)
        print(f"- {array_name}")
        # Assuming the array contains integer labels, we can retrieve and print the values
        array = cell_data.GetArray(i)
        if array:
            for j in range(array.GetNumberOfTuples()):
                if array.GetValue(j)==13:
                    print(f"  Cell {j}: {array.GetValue(j)}")
else:
    print("No Cell Data.")

