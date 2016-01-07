
import subprocess

'''from abaqus import *
from abaqusConstants import *
import part
import assembly
import step
import load
import interaction'''


class AbaqusLayers():

    def __init__(self, inputfile, giveninstances, givenParts, model, numlayer, startingLayer,):
        self.inputfile = inputfile
        self.givenInstances = giveninstances
        self.givenParts = givenParts
        self.model = model
        self.numlayer = numlayer
        self.startLayer = startingLayer


    def getlayers(self):

        for i in range(max(self.numlayer)):
            layermerge = []
            for index in range(len(self.givenInstances)):
                if i <= self.numlayer[index]:
                    layermerge.append(self.model.rootAssembly.sets[self.givenInstances[index] + '_BoxSectionSet_' +
                                                                   str(i + self.startLayer[index])])
            BoxSectionSet = self.model.rootAssembly.SetByBoolean(name="MergedSet_" + str(i), sets=layermerge)
            if i == 0:
                self.model.HeatTransferStep(name='test_' + str(i), previous='Initial',timePeriod=3, initialInc=.001,
                                            minInc=0.00001, maxInc=1, deltmx=100.0)
                self.model.ModelChange(name='Model_Change_Test_' + str(i), createStepName='test_' + str(i),
                                       regionType=ELEMENTS, region=BoxSectionSet)
                self.model.FieldOutputRequest(name='F-Output-layer-' + str(i),  createStepName='test_' + str(i),
                                              variables=('NT', 'HFL', 'RFL'))


            else:
                self.model.HeatTransferStep(name='test_' + str(i), previous='test_' + str(i-1),
                                            timePeriod=3, initialInc=.001, minInc=0.00001, maxInc=1, deltmx=100.0)
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
                                           region=boxSurface, magnitude=10000000.0, amplitude='Heat_Transfer_Amp')

            else:
                self.model.SurfaceHeatFlux(name='Heat_Flux_' + str(i), createStepName='test_' + str(i),
                                           region=boxSurface, magnitude=10000000.0, amplitude='Heat_Transfer_Amp')

if __name__ == "__main__":