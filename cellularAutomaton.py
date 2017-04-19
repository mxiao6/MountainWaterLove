# -*- coding: utf-8 -*-
# @Author: ruian2, kelu2
# @Date:   2017-04-01 21:13:20
# @Last Modified by:   Luke
# @Last Modified time: 2017-04-02 04:03:04

import cellWaterTower
import utilConnectivity
import random
import numpy as np

class cellularAutomaton:

    def __init__(self):
        self.mesh = utilConnectivity.get_mesh()
        self.connectivityInfo = utilConnectivity.gridGen()
        # print(self.connectivityInfo)
        self.cells = {}
        self.flowCoeff = 0.2
        self.diffusionCoeff = 0.0


    def populateCells(self):
        # print("enter populate")
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
        for neighborIndex in neighbors:
            neighborCell = self.cells[neighborIndex]
            #print (neighborCell.neighborInkTransfer[cell.index])
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


    def waterPropagate(self, root_cell):
        # print("enter waterPropagate")
        largestIdx = len(self.mesh.vertices)
        for cellIndex in range(largestIdx):
            cell = self.cells[cellIndex]
            self.genNeighborWaterTransfer(cell)

        for cellIndex in range(largestIdx):
            cell = self.cells[cellIndex]
            cell.water = max(0, cell.water + self.sumDiffNeighborWater(cell))


    def inkPropagate(self, root_cell):
        largestIdx = len(self.mesh.vertices)
        for cellIndex in range(largestIdx):
            cell = self.cells[cellIndex]
            self.genNeighborInkTransfer(cell)
            self.genInkDiffusionTransfer(cell)
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
            res.append(item/max(intValues))
        return np.array(res)


    def retrieve_next_level(self, vertices):
        result = []
        for i in vertices:
            result = result + list(self.mesh.get_vertex_adjacent_vertices(int(i)))
        return set(result)


    def genDepth(self, init_index, depth):
        previous_list = [init_index]
        result = {}
        result[0] = previous_list
        for i in range(1, depth):
            next_level_set = self.retrieve_next_level(previous_list)
            for j in range(i):
                next_level_set = next_level_set - set(result[j])
            result[i] = list(next_level_set)
            previous_list = result[i]
        return result


def main():
    automaton = cellularAutomaton()
    automaton.populateCells()
    depth = 300
    # automaton.setCell(5, 10000, 100, 100000, 500000)
    # automaton.setCell(6, 10000, 100, 100000, 500000)
    # automaton.setCell(1, 10050, 100, 50000, 500000)
    # automaton.setCell(2, 9950, 100, 60000, 500000)
    for i in range(250):
        automaton.setCell(i, 10000+random.random()*100-50, 100+random.random()*10-5, 100000+random.random()*5000-5000, 5000000+random.random()*10000-5000)
    # automaton.setCell(10, 10000, 100, 400, 5000)
    for i in range(depth):
        automaton.waterPropagate(automaton.cells[5])
        automaton.inkPropagate(automaton.cells[5])

        # automaton.waterPropagate(automaton.cells[11])
        # automaton.inkPropagate(automaton.cells[11])
        #
        # automaton.waterPropagate(automaton.cells[1])
        # automaton.inkPropagate(automaton.cells[1])
        #
        # automaton.waterPropagate(automaton.cells[2])
        # automaton.inkPropagate(automaton.cells[2])

    depthMap = automaton.genDepth(0, 3)
    automaton.evaporation(depthMap,1000)

    print "ink level:", (automaton.retrieveInkLevel())
    print "alpha values", (automaton.retrieveAlphaRatio(100000))
    utilConnectivity.color_vertices(automaton.mesh, automaton.retrieveAlphaRatio(100000))

    utilConnectivity.change_format("teapot.ply", "fantasticTeaPot.ply")

main()


