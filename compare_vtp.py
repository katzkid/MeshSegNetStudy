import vtk
import numpy as np

# Paths to the VTP files
reference_file = "/home/kartik/Documents/gdrive/MeshSeg/dataset/Sample_01_d.vtp"
prediction_file = "/home/kartik/Documents/gdrive/MeshSeg/dataset/U1CUXHEX_d_predicted.vtp"

# Read the reference mesh
reference_reader = vtk.vtkXMLPolyDataReader()
reference_reader.SetFileName(reference_file)
reference_reader.Update()
reference_mesh = reference_reader.GetOutput()

# Read the predicted mesh
prediction_reader = vtk.vtkXMLPolyDataReader()
prediction_reader.SetFileName(prediction_file)
prediction_reader.Update()
prediction_mesh = prediction_reader.GetOutput()

# Compute the Hausdorff distance
hausdorff_filter = vtk.vtkHausdorffDistancePointSetFilter()
hausdorff_filter.SetInputData(0, reference_mesh)
hausdorff_filter.SetInputData(1, prediction_mesh)
hausdorff_filter.Update()

# Get the results
max_distance = hausdorff_filter.GetHausdorffDistance()

print(f"Hausdorff Distance (Max): {max_distance}")

# Compute Mean Distance Manually
reference_points = np.array(
    [reference_mesh.GetPoint(i) for i in range(reference_mesh.GetNumberOfPoints())]
)
prediction_points = np.array(
    [prediction_mesh.GetPoint(i) for i in range(prediction_mesh.GetNumberOfPoints())]
)

# Create a point locator for the prediction points
locator = vtk.vtkPointLocator()
locator.SetDataSet(prediction_mesh)
locator.BuildLocator()

# Compute distances from reference points to the closest prediction points
distances = []
for point in reference_points:
    closest_point_id = locator.FindClosestPoint(point)
    closest_point = prediction_mesh.GetPoint(closest_point_id)
    distance = np.linalg.norm(np.array(point) - np.array(closest_point))
    distances.append(distance)

mean_distance = np.mean(distances)
print(f"Mean Distance: {mean_distance}")