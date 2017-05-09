import pymesh
import numpy as np
mesh = pymesh.load_mesh("./mt.ply") 
mesh.enable_connectivity()
print mesh.vertices


