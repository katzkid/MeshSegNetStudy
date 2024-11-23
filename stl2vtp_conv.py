import vtk

# Read the STL file
reader = vtk.vtkSTLReader()
reader.SetFileName("../dataset/U1CUXHEX.stl")
reader.Update()

# Write to a VTP file
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("output.vtp")
writer.SetInputData(reader.GetOutput())
writer.Write()
