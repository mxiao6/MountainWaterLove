# -*- coding: utf-8 -*-
# @Author: ruian2, kelu2
# @Date:   2017-04-01 20:55:37
# @Last Modified by:   Luke
# @Last Modified time: 2017-04-02 02:11:01

class cellWaterTower:

    def __init__(self, bottom, capacity, index):
        self.index = index
        self.bottom = bottom
        self.capacity = capacity
        self.ink = 0
        self.water = 0
        self.dink = 0
        self.dwater = 0
        self.neighborWaterTransfer = {}
        self.neighborInkTransfer = {}
        self.inkDiffusionTransfer = {}


    def calcPipeHeight(self, otherCell):
        return max(otherCell.bottom, self.bottom + self.capacity)

    

