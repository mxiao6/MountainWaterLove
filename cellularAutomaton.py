# -*- coding: utf-8 -*-
# @Author: Luke
# @Date:   2017-04-01 21:13:20
# @Last Modified by:   Luke
# @Last Modified time: 2017-04-02 04:03:04
import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)

if not dir in sys.path:
    sys.path.append(dir)

import cellWaterTower
import utilConnectivity
import random

class cellularAutomaton:

    def __init__(self):
        self.connectivityInfo = utilConnectivity.gridGen()
        print(self.connectivityInfo)
        self.cells = {}
        self.flowCoeff = 0.2
        self.diffusionCoeff = 0.0

    def populateCells(self):
        print("enter populate")
        for i in range(len(self.connectivityInfo)):
            randBottomRange = random.random()*100-50
            randCapRange = random.random()*100-50
            cell = cellWaterTower.cellWaterTower(10000+randBottomRange, 100+randCapRange, i)
            self.cells[i] = cell

    def setCell(self, index, bottom, capacity, ink, water):
        cell = self.cells[index]
        cell.bottom = bottom
        cell.capacity = capacity
        cell.ink = ink
        cell.water = water
        self.cells[index] = cell

    def calcWaterTransferable(self, cell, otherCell, transferCoeff, numOfNeighborCells):
        sumOfSelf = cell.bottom + cell.water
        difference = min(sumOfSelf - (otherCell.bottom + otherCell.water), \
            sumOfSelf - cell.calcPipeHeight(otherCell))
        return max(0, (transferCoeff/numOfNeighborCells) * difference)

    def calcInkTransferable(self, cell, otherCell):
        deltaW = cell.neighborWaterTransfer[otherCell.index]
        if cell.water == 0:
            return 0
        return deltaW * cell.ink/cell.water

    def genNeighborWaterTransfer(self, cell):
        neighbors = self.connectivityInfo[cell.index]
        for neighborIndex in neighbors:
            neighborCell = self.cells[neighborIndex]
            cell.neighborWaterTransfer[neighborIndex] = \
            self.calcWaterTransferable(cell, neighborCell, self.flowCoeff, len(neighbors))

    def genNeighborInkTransfer(self, cell):
        neighbors = self.connectivityInfo[cell.index]
        for neighborIndex in neighbors:
            neighborCell = self.cells[neighborIndex]
            cell.neighborInkTransfer[neighborIndex] = \
            self.calcInkTransferable(cell, neighborCell)

    def inkDiffuse(self, cell, otherCell):
        if cell.water + otherCell.water == 0:
            return self.diffusionCoeff * otherCell.ink
        return self.diffusionCoeff * (otherCell.ink - otherCell.water \
            *(cell.ink+otherCell.ink)/(cell.water+otherCell.water))

    def genInkDiffusionTransfer(self, cell):
        neighbors = self.connectivityInfo[cell.index]
        for neighborIndex in neighbors:
            # print("reach")
            neighborCell = self.cells[neighborIndex]
            cell.inkDiffusionTransfer[neighborIndex] = self.inkDiffuse(cell, neighborCell)        

    def sumDiffNeighborWater(self, cell):
        result = 0.0
        neighbors = self.connectivityInfo[cell.index]
        # print(cell.index)
        for neighborIndex in neighbors:
            neighborCell = self.cells[neighborIndex]
            # print(cell.index)
            # print(neighborCell.index)
            result += neighborCell.neighborWaterTransfer[cell.index] - cell.neighborWaterTransfer[neighborIndex]

        return result

    def sumDiffNeighborInk(self, cell):
        result = 0.0
        neighbors = self.connectivityInfo[cell.index]
        for neighborIndex in neighbors:
            neighborCell = self.cells[neighborIndex]
            result += neighborCell.neighborInkTransfer[cell.index] - cell.neighborInkTransfer[neighborIndex]
        return result

    def sumDiffusion(self, cell):
        result = 0.0
        neighbors = self.connectivityInfo[cell.index]
        for neighborIndex in neighbors:
            neighborCell = self.cells[neighborIndex]
            result += neighborCell.inkDiffusionTransfer[cell.index] 
        return result

    def getPropagationOrder(self, root):
        # order_list = [root.index]
        # progress_marker = set()
        # order_list = order_list + self.connectivityInfo[root.index]
        # progress_marker.update(order_list)
        # while(len(progress_marker) < len(self.connectivityInfo)):
        #     tempList = list(progress_marker)
        #     for item in tempList:
        #         progress_marker.update(self.connectivityInfo[item])
        return utilConnectivity.genOrder(root.index)    


    def waterPropagate(self, root_cell):
        print("enter waterPropagate")
        # for cell in self.cells:
        # order = self.getPropagationOrder(root_cell)
        # print(self.getPropagationOrder(root_cell))
        # print("order: ",order)
        largestIdx = 8
        for cellIndex in range(largestIdx):
        # for cellIndex in order:
            cell = self.cells[cellIndex]
            self.genNeighborWaterTransfer(cell)
            # print(cell.neighborWaterTransfer)
            # print(self.connectivityInfo)

        # for cellIndex in order:
        for cellIndex in range(largestIdx):
            cell = self.cells[cellIndex]
            cell.water = max(0, cell.water + self.sumDiffNeighborWater(cell))


    def inkPropagate(self, root_cell):
        # order = self.getPropagationOrder(root_cell)
        largestIdx = 8
        for cellIndex in range(largestIdx):
        # for cellIndex in order:
            cell = self.cells[cellIndex]
            self.genNeighborInkTransfer(cell)
            self.genInkDiffusionTransfer(cell)
        # for cellIndex in order:
        for cellIndex in range(largestIdx):
            cell = self.cells[cellIndex]
            cell.ink = cell.ink + self.sumDiffNeighborInk(cell) + self.sumDiffusion(cell)

    def printCells(self):
        for cellIndex in self.cells:
            print("index: ", self.cells[cellIndex].index)
            print("ink: ", self.cells[cellIndex].ink)
            print("water: ", self.cells[cellIndex].water)
            print("......")

    def retrieveInkLevel(self):
        result = []
        for cellIndex in self.cells:
            result.append(self.cells[cellIndex].ink)
        return result

    def evaporation(self, depthMap, rate):
        for i in range(len(depthMap)):
            for cellIndex in depthMap[i]:
                self.cells[cellIndex].water -= (len(depthMap) - i) * rate
                if self.cells[cellIndex].water <= 0:
                    self.cells[cellIndex].water = 0

    def retrieveAlphaRatio(self, maxInkLevel):
        intValues = self.retrieveInkLevel()
        res = []
        for item in intValues:
            res.append(item/maxInkLevel)
        return res



def main():
    automaton = cellularAutomaton()
    automaton.populateCells()
    depth = 3
    for i in range(depth):
        automaton.setCell(0, 10000, 100, 500, 5000)
        automaton.setCell(6, 10000, 100, 500, 5000)
        automaton.waterPropagate(automaton.cells[0])
        automaton.inkPropagate(automaton.cells[0])

    # depthMap = utilConnectivity.genDepth(0)
    # automaton.evaporation(depthMap, 1000)




    # for i in range(depth):
    #     automaton.setCell(6, 10000, 100, 500, 5000)
        automaton.waterPropagate(automaton.cells[6])
        automaton.inkPropagate(automaton.cells[6])

    depthMap = utilConnectivity.genDepth(6)
    automaton.evaporation(depthMap,1000)

    # automaton.printCells()
    print(automaton.retrieveInkLevel())
    print(automaton.retrieveAlphaRatio(500))


    mesh = None
    obs = bpy.data.objects
    for ob in obs:
        if ob.name == "Cube":
            # print("found")
            mesh = ob
    utilConnectivity.color_vertex(mesh, automaton.retrieveAlphaRatio(500))

main()


