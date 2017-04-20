import pymesh
import numpy as np
mesh = pymesh.load_mesh("testCube.obj")
mesh.add_attribute("vertex_color")
val = np.zeros(3*mesh.num_vertices)
mesh.set_attribute("vertex_color", val)



pymesh.save_mesh("testCube.ply", mesh, "vertex_color", ascii = True)
