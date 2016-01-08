

import re
import os

from abaqus import *
from abaqusConstants import *
import part
import assembly
import step
import load
import interaction


class AbaqusLayers:

    def __init__(self, inputfile, giveninstances, givenParts, model, numlayer, startingLayer,):
        self.inputfile = inputfile
        self.givenInstances = giveninstances
        self.givenParts = givenParts
        self.model = model
        self.numlayer = numlayer
        self.startLayer = startingLayer

    def getregions(self):

        abaqus_directory = os.getcwd()
        os.chdir('C:\Users\Michael Haines\PycharmProjects\Abaqus_Code')

        for model in self.givenInstances:

            list_of_layers = []

            filehandle = open(model + '_layer', 'r')
            with filehandle as f:
                content = f.readlines()
                temp = []

                for line in content:
                    # temp.append(re.findall(r'[+-]?\d+\.*\d*', line))
                    list_of_layers.append(re.findall(r'[+-]?\d+\.*\d*', line))

            list_of_layers = [[int(x) for x in row] for row in list_of_layers]
            first_layer = 1

            temp_list = []
            for i in list_of_layers[first_layer:]:
                for k in i:
                    temp_list.append(k)

            boxElements = self.model.rootAssembly.instances[model].elements
            boxSet = boxElements.sequenceFromLabels(temp_list)
            BoxSectionSet = self.model.rootAssembly.Set(name=model + '_BoxSectionSet_0', elements=boxSet)
            boxSet = boxElements.sequenceFromLabels(list_of_layers[first_layer-1])
            boxSurface = self.model.rootAssembly.Surface(name=model + '_BoxSectionSurface_0', face2Elements=boxSet)
            count = 1
            for i in list_of_layers[first_layer:]:
                boxSet = boxElements.sequenceFromLabels(i)
                BoxSectionSet = self.model.rootAssembly.Set(name=model + '_BoxSectionSet_' + str(count), elements=boxSet)
                boxSurface = self.model.rootAssembly.Surface(name=model + '_BoxSectionSurface_' + str(count),
                                                             face2Elements=boxSet)
                count += 1

    def getlayers(self):

        for i in range(max(self.numlayer)):
            layermerge = []
            for index in range(len(self.givenInstances)):
                if i <= self.numlayer[index]:
                    layermerge.append(self.model.rootAssembly.sets[self.givenInstances[index] + '_BoxSectionSet_' +
                                                                   str(i + self.startLayer[index])])
            BoxSectionSet = self.model.rootAssembly.SetByBoolean(name="MergedSet_" + str(i), sets=layermerge)
            if i == 0:
                self.model.HeatTransferStep(name='test_' + str(i), previous='Initial',timePeriod=60, initialInc=.001,
                                            minInc=0.00001, maxInc=1, maxNumInc=500, deltmx=100.0)
                self.model.ModelChange(name='Model_Change_Test_' + str(i), createStepName='test_' + str(i),
                                       regionType=ELEMENTS, region=BoxSectionSet)
                self.model.FieldOutputRequest(name='F-Output-layer-' + str(i),  createStepName='test_' + str(i),
                                              variables=('NT', 'HFL', 'RFL'))


            else:
                self.model.HeatTransferStep(name='test_' + str(i), previous='test_' + str(i-1),
                                            timePeriod=60, initialInc=.001, minInc=0.00001, maxInc=1, maxNumInc=500, deltmx=100.0)
                self.model.ModelChange(name='Model_Change_Test_' + str(i), createStepName='test_' + str(i),
                                       regionType=ELEMENTS, region=BoxSectionSet, activeInStep=True)
                self.model.FieldOutputRequest(name='F-Output-layer-' + str(i),  createStepName='test_' + str(i),
                                              variables=('NT', 'HFL', 'RFL'))

        for i in range(max(self.numlayer)):
            surfacemerge = []
            for index in range(len(self.givenParts)):
                if i <= self.numlayer[index]:
                    surfacemerge.append(self.model.rootAssembly.surfaces[self.givenParts[index] + '_BoxSectionSurface_' +
                                                                     str(i)])

            boxSurface = self.model.rootAssembly.SurfaceByBoolean(name="MergedSurface_" + str(i), surfaces=surfacemerge)
            if i == 0:
                self.model.SurfaceHeatFlux(name='Heat_Flux_' + str(i), createStepName='test_' + str(i),
                                           region=boxSurface, magnitude=500000000.0, amplitude='Heat_Transfer_Amp')

            else:
                self.model.SurfaceHeatFlux(name='Heat_Flux_' + str(i), createStepName='test_' + str(i),
                                           region=boxSurface, magnitude=500000000.0, amplitude='Heat_Transfer_Amp')

if __name__ == "__main__":

    abaqus_directory = os.getcwd()
    mymodel = mdb.models['Simplified Arcam model']

    grabnodes = AbaqusLayers("Heat_Transfer_Test_1.inp",
                           ['test_sample-1', 'test_sample-1-lin-2-1', 'test_sample-1-lin-3-1', 'test_sample-1-lin-4-1',
                            'test_sample-1-rad-2', 'test_sample-1-rad-4'],
                           ['test_sample-1', 'test_sample-1-lin-2-1', 'test_sample-1-lin-3-1', 'test_sample-1-lin-4-1',
                            'test_sample-1-rad-2', 'test_sample-1-rad-4'], mymodel, [20, 20, 20, 20, 20, 20],
                           [0, 0, 0, 0, 0, 0])

    grabnodes.getregions()
    grabnodes.getlayers()
    os.chdir(abaqus_directory)