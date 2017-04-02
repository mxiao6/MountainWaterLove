# -*- coding: utf-8 -*-
# @Author: Luke
# @Date:   2017-04-01 21:34:40
# @Last Modified by:   Luke
# @Last Modified time: 2017-04-02 02:39:39
import bpy

def getEdgesForVertex(v_index, mesh, marked_edges):
    all_edges = [e for e in mesh.edges if v_index in e.vertices]
    unmarked_edges = [e for e in all_edges if e.index not in marked_edges]
    return unmarked_edges

def findConnectedVerts(v_index, mesh, connected_verts, marked_edges, maxdepth=1, level=0):  
    if level >= maxdepth:
        return

    edges = getEdgesForVertex(v_index, mesh, marked_edges)

    for e in edges:
        othr_v_index = [idx for idx in mesh.edges[e.index].vertices if idx != v_index][0]
        connected_verts[othr_v_index] = True
        marked_edges.append(e.index)
        findConnectedVerts(othr_v_index, mesh, connected_verts, marked_edges, maxdepth=maxdepth, level=level+1)





def gridGen():
    mesh = bpy.context.object.data

    connected_verts = {}
    marked_edges = []
    grid = {}
    result = []
    for v in mesh.vertices:
        findConnectedVerts(v.index, mesh, connected_verts, marked_edges, maxdepth=1)
        #print(",".join([str(v) for v in connected_verts.keys()]))
        grid[v.index] = connected_verts.keys()
        connected_verts = {}
        marked_edges = []
    return grid
    # connected_verts = {}
    # marked_edges = []

    # findConnectedVerts(0, mesh, previous, marked_edges_1, maxdepth=1)
    # # print(",".join([str(v) for v in previous.keys()]))
    # result = result + list(previous.keys())

    # current = {}
    # marked_edges_2 = []

    # findConnectedVerts(0, mesh, current, marked_edges_2, maxdepth=2)
    # # print(",".join([str(v) for v in current.keys()]))

    # temp = [x for x in current if x not in previous]
    # result = result + temp

    # connected_verts_3 = {}
    # marked_edges_3 = []

    # findConnectedVerts(0, mesh, connected_verts_3, marked_edges_3, maxdepth=3)
    # # print(",".join([str(v) for v in connected_verts.keys()]))

    # temp = [x for x in connected_verts_3 if x not in current]
    # result = result + temp
    # print(result)

def genOrder(beginningIndex):
    mesh = bpy.context.object.data

    previous = {}
    marked_edges_1 = []
    grid = {}
    result = []
    for i in range(1, len(mesh.vertices)):
        current = {}
        marked_edges_2 = []
        findConnectedVerts(beginningIndex, mesh, current, marked_edges_2, maxdepth=i)
        # print(",".join([str(v) for v in current.keys()]))

        temp = [x for x in current if x not in previous]
        result = result + temp
        previous = current
    return [beginningIndex]+result[:-1]

# genOrder(0)

# print(gridGen())

