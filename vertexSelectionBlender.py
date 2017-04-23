# -*- coding: utf-8 -*-
# @Author: ruian2, kelu2
# @Date:   2017-04-21 19:52:45
# @Last Modified by:   Luke
# @Last Modified time: 2017-04-21 19:57:20

import bpy

file_name = "/Users/Luke/Desktop/test.txt"

mode = bpy.context.active_object.mode
# we need to switch from Edit mode to Object mode so the selection gets updated
bpy.ops.object.mode_set(mode='OBJECT')
selectedVerts = [v for v in bpy.context.active_object.data.vertices if v.select]

file = open(file_name, "w")


for v in selectedVerts:
    # print(v.co)
    file.write(str(v.index))
    file.write("\n")


# back to whatever mode we were in
bpy.ops.object.mode_set(mode=mode)

