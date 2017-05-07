# -*- coding: utf-8 -*-
# @Author: ruian2, kelu2
# @Date:   2017-04-01 21:34:40
# @Last Modified by:   Luke
# @Last Modified time: 2017-05-07 00:03:39
# import bpy

import pymesh
import numpy as np
import csv

#TODO You also need to update the colors in the csv color, each row corresponds to the color you want fill to that segment
#TODO The default fine name is colorscheme.csv

def gridGen(mesh_name):
    mesh = pymesh.load_mesh(mesh_name)
    mesh.enable_connectivity()
    grid = {}
    # print mesh.vertices
    for v in range(len(mesh.vertices)):
        grid[v] = list(mesh.get_vertex_adjacent_vertices(int(v)))
    return grid


def alpha_blending(src, dest, alpha):
    list = alpha * (src - dest) + dest
    result = []
    for i in list:
        result.append(int(i))
    return result


def color_vertices(obj, alpha, mesh_name, seg_number):
    mesh = obj
    vertices_colors = mesh.get_attribute("vertex_color")
    counter = 0
    redVal = 0
    greenVal = 0
    blueVal = 0
    f = open("colorscheme.csv", "r")
    color_csv = csv.reader(f)
    print "the fucking shit is " + str(seg_number)
    for row in color_csv:
        print counter
        print seg_number
        if seg_number-1 == counter:
            redVal = row[0]
            blueVal = row[1]
            greenVal = row[2]
            print redVal
            print blueVal
            print greenVal
        counter += 1

    for i in range(mesh.num_vertices):
        if(np.array_equal(vertices_colors[i*3: i*3+3], np.array([246,245,240]))):
            vertices_colors[0 + 3 * i] = redVal
            vertices_colors[1 + 3 * i] = greenVal
            vertices_colors[2 + 3 * i] = blueVal
            vertices_colors[i*3: i*3+3] = alpha_blending(vertices_colors[i*3: i*3+3], np.array([251, 247, 240]), alpha[i])
        # vertices_colors[i*3: i*3+3] = alpha_blending(vertices_colors[i*3: i*3+3], np.array([255,255,255]), alpha[i])
    mesh.set_attribute("vertex_color", vertices_colors)
    f.close()


def change_format(inputFileName, outputFileName):
    file = open(inputFileName)
    lines = []
    for line in file:
        lines.append(line)
    # print lines
    file.close()
    num_vertices = int(lines[3][15:-1])
    del lines[7]
    lines.insert(7, "property uchar red\n")
    lines.insert(8, "property uchar green\n")
    lines.insert(9, "property uchar blue\n")
    for i in range(13,num_vertices+13):
        line_list = lines[i].split(" ")
        del line_list[3]
        new_line = " ".join(line_list)
        del lines[i]
        lines.insert(i, new_line)
    file = open(outputFileName, "w")
    for line in lines:
        file.write(line)
    file.close()


def get_mesh(mesh_name):
    mesh = pymesh.load_mesh(mesh_name)
    mesh.enable_connectivity()
    # vertex color should be the initiated first to ensure multiple times coloring for the same model
    mesh.add_attribute("vertex_color")
    vertices_colors = np.zeros(3*mesh.num_vertices)
    for i in range(mesh.num_vertices):
        vertices_colors[i*3: i*3+3] = np.array([251,247,240])
    mesh.set_attribute("vertex_color", vertices_colors)
    return mesh

