# -*- coding: utf-8 -*-
# @Author: Luke
# @Date:   2017-04-01 21:13:20
# @Last Modified by:   Luke
# @Last Modified time: 2017-04-02 02:55:58
import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import cellWaterTower
import utilConnectivity

class cellularAutomaton:

    def __init__(self):
        self.connectivityInfo = utilConnectivity.gridGen()
        self.cells = {}
        self.flowCoeff = 0.5
        self.diffusionCoeff = 0.0

    def populateCells(self):
        for i in range(len(self.connectivityInfo)):
            cell = cellWaterTower.cellWaterTower(1000,100,i)
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
        print(cell.index)
        for neighborIndex in neighbors:
            neighborCell = self.cells[neighborIndex]
            print(cell.index)
            print(neighborCell.index)
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
        # for cell in self.cells:
        order = self.getPropagationOrder(root_cell)
        print("order: ",order)
        for cellIndex in order:
            cell = self.cells[cellIndex]
            self.genNeighborWaterTransfer(cell)
            # print(cell.neighborWaterTransfer)
            # print(self.connectivityInfo)

        for cellIndex in order:
            cell = self.cells[cellIndex]
            cell.water = max(0, cell.water + self.sumDiffNeighborWater(cell))


    def inkPropagate(self, root_cell):
        order = self.getPropagationOrder(root_cell)
        for cellIndex in order:
            cell = self.cells[cellIndex]
            self.genNeighborInkTransfer(cell)
            self.genInkDiffusionTransfer(cell)
        for cellIndex in order:
            cell = self.cells[cellIndex]
            cell.ink = cell.ink + self.sumDiffNeighborInk(cell) + self.sumDiffusion(cell)

    def printCells(self):
        for cellIndex in self.cells:
            print("index: ", self.cells[cellIndex].index)
            print("ink: ", self.cells[cellIndex].ink)
            print("water: ", self.cells[cellIndex].water)
            print("......")

    def retrieveRatio(self):
        result = []
        for cellIndex in self.cells:
            result.append(self.cells[cellIndex].ink/self.cells[cellIndex].water)
        return result

def main():
    automaton = cellularAutomaton()
    automaton.populateCells()
    for i in range(200):
        automaton.setCell(0, 10000, 100, 1000, 5000)
        automaton.waterPropagate(automaton.cells[0])
        automaton.inkPropagate(automaton.cells[0])
    automaton.printCells()
    print(automaton.retrieveRatio())


main()


