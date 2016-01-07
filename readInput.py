__author__ = 'michael'

# from sys import path
# path.append('C:\Python27\Lib\site-packages')

import os
from pathos.multiprocessing import ProcessingPool
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

'''from abaqus import *
from abaqusConstants import *
import part
import assembly
import step
import load
import interaction'''


class GetElements():

    def __init__(self, inputfile, giveninstances, givenParts, model, numlayer, startingLayer,):
        self.inputfile = inputfile
        self.givenInstances = giveninstances
        self.givenParts = givenParts
        self.model = model
        self.numlayer = numlayer
        self.startLayer = startingLayer

    def getnodes(self, givenInstances):

        import re
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        output_list = None

        print "locating nodes"
        model = givenInstances
        filehandle = open(self.inputfile, 'r')
        with filehandle as f:
            content = f.readlines()
        #   for model in givenInstances: #was self.givenInstaces
            nodes = []
            elements = []
            count = 0
            start = 0
            end = 0
            for index, line in enumerate(content):
                if line.find(model) >= 0:
                    count = index
                    break

            for line in content[count:]:
                if "*Node" in line:
                    count += 1
                    start = count
                elif '*Element' in line:
                    end = count
                    break
                else:
                    count += 1

            for i in range(start, end):
                nodes.append(re.findall(r'[+-]?\d+\.*\d*', content[i]))


            for line in content[count:]:
                if "*Element" in line:
                    count += 1
                    start = count
                elif '*Nset,' in line:
                    end = count
                    break
                else:
                    count += 1

            for i in range(start, end):
                elements.append(re.findall(r'[+-]?\d+\.*\d*', content[i]))

            elements = [[float(f) for f in row] for row in elements]
            nodes = [[float(f) for f in row] for row in nodes]
            cool = sorted(nodes, key=lambda x: x[2],)
            # print elements
            # print cool
            last_layer = min(nodes, key=lambda x: x[3],)[3] #change axis from 2
            list_of_layers = []

            y = [i[3] for i in nodes] # change axis from 2

            seen = set()
            seen_add = seen.add
            layers = [x for x in y if not (x in seen or seen_add(x))]
            layers = layers[::-1]
            print layers[1:]

            for layer in layers[1:]:
                x = []
                y = []
                z = []
                node_numbers = []
                element_numbers = []

                print layer
                print last_layer

                for i in nodes:
                    if i[3] <= layer and i[3] >= last_layer: # change axis from 2
                        node_numbers.append((i[0]))
                        x.append(i[1])
                        y.append(i[2])
                        z.append(i[3])

                #print y
                last_layer = layer

                for i in elements:
                    element_numbers.append(i[0])

                elements_to_write = []

                print("gathering Elements")
                for index, elemnum  in enumerate(element_numbers):
                    number_of_nodes = 0
                    for node in node_numbers:
                        if node in elements[index][1:8]:
                            number_of_nodes += 1

                    if number_of_nodes == 7:
                        elements_to_write.append(elemnum)
                print("Converting array")
                elements_to_write = [int(i) for i in elements_to_write]
                print elements_to_write
                list_of_layers.append(elements_to_write)

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(x, y, z, zdir='y')
                #ax.set_xlim(-.5,.25)
                #ax.set_ylim(-.25,.5)
                #ax.set_zlim(-.25,.25)
                # plt.show()

            list_of_layers = [[int(x) for x in row] for row in list_of_layers]
            print list_of_layers

            first_layer = 1
            temp_list = []
            for i in list_of_layers[first_layer:]:
                for k in i:
                    temp_list.append(k)
            print temp_list
            # print model
            output_list = list_of_layers
            '''boxElements = self.model.rootAssembly.instances[model].elements
            boxSet = boxElements.sequenceFromLabels(temp_list)
            BoxSectionSet = self.model.rootAssembly.Set(name=model + '_BoxSectionSet_0', elements=boxSet)
            boxSet = boxElements.sequenceFromLabels(list_of_layers[first_layer-1])
            boxSurface = self.model.rootAssembly.Surface(name=model + '_BoxSectionSurface_0', face6Elements=boxSet)
            count = 1
            for i in list_of_layers[first_layer:]:
                boxSet = boxElements.sequenceFromLabels(i)
                BoxSectionSet = self.model.rootAssembly.Set(name=model + '_BoxSectionSet_' + str(count), elements=boxSet)
                boxSurface = self.model.rootAssembly.Surface(name=model + '_BoxSectionSurface_' + str(count),
                                                         face6Elements=boxSet)'''

        filehandle.close()
        filehandle = open(str(model) + "_layer", 'w')
        # output_list = [[str(x) for x in row] for row in output_list]
        filehandle.write(str(output_list))


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


'''def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)


def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)'''


if __name__== "__main__":

    # copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
    # mymodel = mdb.models['Simplified Arcam model']

    os.chdir("C:\Users\Michael Haines\PycharmProjects\Abaqus_Code")

    filehandle = open("Heat_Transfer_Test_1.inp", 'r')
    content = None
    with filehandle as f:
            content = f.readlines()
    filehandle.close()

    grabnodes =GetElements("Heat_Transfer_Test_1.inp",
                           ['test_sample-1', 'test_sample-1-lin-2-1', 'test_sample-1-lin-3-1', 'test_sample-1-lin-4-1',
                            'test_sample-1-rad-2', 'test_sample-1-rad-4'],
                           ['test_sample-1', 'test_sample-1-lin-2-1', 'test_sample-1-lin-3-1', 'test_sample-1-lin-4-1',
                            'test_sample-1-rad-2', 'test_sample-1-rad-4'], 'mymodel', [20, 20, 20, 20, 20, 20],
                           [0, 0, 0, 0, 0, 0])

    items = ['test_sample-1', 'test_sample-1-lin-2-1', 'test_sample-1-lin-3-1', 'test_sample-1-lin-4-1',
                            'test_sample-1-rad-2', 'test_sample-1-rad-4']

    p = ProcessingPool(6)
    p.map(GetElements.getnodes, [grabnodes]*6, items)
