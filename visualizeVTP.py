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

# Get Cell Data
cell_data = mesh.GetCellData()

# Ensure there is at least one array in CellData
if cell_data.GetNumberOfArrays() > 0:
    # Use the first array for visualization
    label_array = cell_data.GetArray(0)
    
    # Check if the label array exists
    if label_array:
        print("Label array found!")
        print(f"Array Name: {cell_data.GetArrayName(0)}")
        
        # Automatically allocate colors for 15 labels (1 to 15)
        num_labels = 15
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(num_labels)
        lut.SetRange(1, num_labels)  # Label range
        lut.Build()

        for i in range(0, num_labels):
            rgba = lut.GetTableValue(i)
            print(f"Label {i}: RGB = {rgba[:3]}")


        # Automatically generate colors for each label
        for i in range(num_labels):
            if i == 0:
                # Set white color for label 0
                lut.SetTableValue(i, 1.0, 1.0, 1.0, 1.0)  # White (R=1, G=1, B=1, A=1)
            else:
                # Generate unique RGB values (Hue-based gradient)
                hue = (i*2) / num_labels  # Evenly spaced hues
                hsv = [hue, 1.0, 1.0]  # Hue, Saturation, Value
                rgb = [0.0, 0.0, 0.0]  # Placeholder for RGB
                vtk.vtkMath.HSVToRGB(hsv, rgb)  # Updates RGB in-place
                lut.SetTableValue(i + 1, rgb[0], rgb[1], rgb[2], 1.0)  # RGBA

        
        for i in range(0, num_labels):
            rgba = lut.GetTableValue(i)
            print(f"Label {i}: RGB = {rgba[:3]}")

        # Map the label array to scalar visibility
        mesh.GetCellData().SetActiveScalars(cell_data.GetArrayName(0))  # Set the active array by name

        # Create a mapper and set the lookup table
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        mapper.SetScalarVisibility(True)
        mapper.SetLookupTable(lut)
        mapper.SetScalarRange(1, num_labels)  # Match the range of the labels

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Create a renderer and add the actor
        renderer = vtk.vtkRenderer()
        renderer.AddActor(actor)

        # Create a render window
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)

        # Create a render window interactor
        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(render_window)

        # Start the visualization
        render_window.Render()
        interactor.Start()
    else:
        print("No valid label array found in CellData.")
else:
    print("No CellData arrays found.")
