__author__ = 'michael'

import multiprocessing

'''from abaqus import *
from abaqusConstants import *
import part
import assembly
import step
import load
import interaction'''

class AbaqusInput(object):
    def __init__(self, nodes, elements):
        pass

    @classmethod
    def from_file(cls, fileobj):
        pass

class LayerSplitter(object):
    def __init__(self, abaqus_input):
        pass

    def _create_mappings(self):
        layers = sorted(set([z values]))
        layer_levels = [i for i, _ in enumerate(layers)]

        # maybe
        # node_to_elements: layer # => [node #'s]

        # node_mapping: layer # => [node #'s]
        # element_mapping: node # => [element #'s]
        pass

    def get_layers(self):
        self._create_mappings()

        layers = []
        for layer_number in self.layer_levels:
            layers.append([])

            nodes = self.nodes_mapping[layer_number]

            element_counts = collections.defaultdict(int)
            for node in nodes:
                elements = self.element_mapping[node]

                for element in elements:
                    element_counts[element] += 1

            for element_number, count in element_counts.iteritems():
                if count == 8:
                    layers[-1].append(element_number)

        return layers

def main(input_filename):
    with open(input_filename, "r") as f:
        input_data = AbaqusInput.from_file(f)

    layer_splitter = LayerSplitter(input_data)
    layers = layer_splitter.get_layers()

    with open("output.json", "w") as f:
        data = {
            "created_on": now(),
            "input_file": input_filename,
            "layers": layers
        }

        json.dump(data, f, separators=(',', ':'))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename')
    args = parser.parse_args()

    main(**vars(args))

def getnodes(givenInstances, inputfile):

    import re
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D

    # AbaqusInput.from_file START

    print "locating nodes"
    model = givenInstances
    filehandle = open(inputfile, 'r')
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
            elif '*End Instance' in line:
                end = count
                break
            else:
                count += 1

        for i in range(start, end):
            elements.append(re.findall(r'[+-]?\d+\.*\d*', content[i]))

        elements = [[int(f) if i == 0 else float(f) for i, f in enumerate(row)] for row in elements]
        nodes = [[int(f) if i == 0 else float(f) for i, f in enumerate(row)] for row in nodes]

        # AbaqusInput.from_file END

        # _get_mapping
        element_map = {
            element[0]: element
            for element in elements
        }

        node_map = {
            node[0]: node
            for node in nodes
        }

        #cool = sorted(nodes, key=lambda x: x[2],)
        # print elements
        # print cool
        last_layer = min(nodes, key=lambda x: x[2],)[2] #change axis from 3
        list_of_layers = []

        y = [i[2] for i in nodes] # change axis from 3

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
                if i[2] <= layer and i[2] >= last_layer: # change axis from 3
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

            '''fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z, zdir='y')
            #ax.set_xlim(-.5,.25)
            #ax.set_ylim(-.25,.5)
            #ax.set_zlim(-.25,.25)
            # plt.show()'''

        list_of_layers = [[int(x) for x in row] for row in list_of_layers]
        print list_of_layers

        filehandle.close()
        filehandle = open(str(model) + "_layer", 'w')
        # output_list = [[str(x) for x in row] for row in output_list]
        for i in list_of_layers:
            filehandle.write(str(i) + '\n')
        filehandle.close()

def getlayers():

    for i in range(max(numlayer)):
        layermerge = []
        for index in range(len(givenInstances)):
            if i <= numlayer[index]:
                layermerge.append(model_attribute.rootAssembly.sets[givenInstances[index] + '_BoxSectionSet_' +
                                                                    str(i + startLayer[index])])
        BoxSectionSet = model_attribute.rootAssembly.SetByBoolean(name="MergedSet_" + str(i), sets=layermerge)
        if i == 0:
            model_attribute.HeatTransferStep(name='test_' + str(i), previous='Initial', timePeriod=3, initialInc=.001,
                                             minInc=0.00001, maxInc=1, deltmx=100.0)
            model_attribute.ModelChange(name='Model_Change_Test_' + str(i), createStepName='test_' + str(i),
                                        regionType=ELEMENTS, region=BoxSectionSet)
            model_attribute.FieldOutputRequest(name='F-Output-layer-' + str(i), createStepName='test_' + str(i),
                                               variables=('NT', 'HFL', 'RFL'))


        else:
            model_attribute.HeatTransferStep(name='test_' + str(i), previous='test_' + str(i - 1),
                                             timePeriod=3, initialInc=.001, minInc=0.00001, maxInc=1, deltmx=100.0)
            model_attribute.ModelChange(name='Model_Change_Test_' + str(i), createStepName='test_' + str(i),
                                        regionType=ELEMENTS, region=BoxSectionSet, activeInStep=True)
            model_attribute.FieldOutputRequest(name='F-Output-layer-' + str(i), createStepName='test_' + str(i),
                                               variables=('NT', 'HFL', 'RFL'))

    for i in range(max(numlayer)):
        surfacemerge = []
        for index in range(len(givenParts)):
            if i <= numlayer[index]:
                surfacemerge.append(model_attribute.rootAssembly.surfaces[givenParts[index] + '_BoxSectionSurface_' +
                                                                          str(i)])

        boxSurface = model_attribute.rootAssembly.SurfaceByBoolean(name="MergedSurface_" + str(i), surfaces=surfacemerge)
        if i == 0:
            model_attribute.SurfaceHeatFlux(name='Heat_Flux_' + str(i), createStepName='test_' + str(i),
                                            region=boxSurface, magnitude=10000000.0, amplitude='Heat_Transfer_Amp')

        else:
            model_attribute.SurfaceHeatFlux(name='Heat_Flux_' + str(i), createStepName='test_' + str(i),
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


# copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
# mymodel = mdb.models['Simplified Arcam model']

if __name__ == '__main__':

    # mymodel = mdb.models['Simplified Arcam model']

    inputfile = "Heat_Transfer_Test_1.inp"
    givenInstances = ['Powder_Bed']
    givenParts = ['Powder_Bed']
    model_attribute = 'mymodel'
    numlayer = [20, 20, 20, 20, 20, 20]
    startLayer = [0, 0, 0, 0, 0, 0]

    items = ['Powder_Bed']

    getnodes(givenInstances[0],inputfile)
    '''pool = multiprocessing.Pool() #use all available cores, otherwise specify the number you want as an argument
    for i in items:
        pool.apply_async(getnodes, args=(i, inputfile))
    pool.close()
    pool.join()'''

    # getlayers()
# p = ProcessingPool(6)
# p.map(getnodes, [grabnodes]*6, items)
