import pymesh

def retrieve_next_level(mesh, vertices):
	result = []
	print "vertices:", vertices
	for i in vertices:
		print "i", i
		# print "list", list(mesh.get_vertex_adjacent_vertices(1))
		result = result + list(mesh.get_vertex_adjacent_vertices(int(i)))
	return set(result)


def genDepth(mesh, init_index, depth):
	length = len(mesh.vertices)
	previous_list = [init_index]
	result = {}
	result[0] = previous_list
	for i in range(1, depth):
	    next_level_set = retrieve_next_level(mesh ,previous_list)
	    print next_level_set
	    for j in range(i):
		next_level_set = next_level_set - set(result[j])
	    result[i] = list(next_level_set)
	    previous_list = result[i]
	return result

def main():
	mesh = pymesh.load_mesh("testCube.obj")
	mesh.enable_connectivity()
	print genDepth(mesh, 0, 4)


main()



