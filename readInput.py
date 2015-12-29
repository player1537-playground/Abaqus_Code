__author__ = 'michael'

import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

'''from abaqus import *
from abaqusConstants import *
import part
import assembly
import step
import load
import interaction'''


class GetElements():

    def __init__(self, inputfile, giveninstance, model, ):
        self.inputfile = inputfile
        self.givenInstance = giveninstance
        self.model = model



    def getnodes(self, layers):

        nodes = []
        elements=[]
        filehandle = open(self.inputfile, 'r')

        with filehandle as f:
            content = f.readlines()
            count = 0
            loop_count = 0
            start = 0
            end = 0
            while True:

                for line in content[count:]:
                    if "*Node" in line:
                        count += 1
                        start = count
                    elif '*Element' in line:
                        end = count
                        break
                    else:
                        count += 1

                temp = []


                if count >= len(content):
                    break


                for i in range(start, end):
                    temp.append(re.findall(r'[+-]?\d+\.*\d*', content[i]))
                nodes.append(temp)

                for line in content[count:]:
                    if "*Element" in line:
                        count += 1
                        start = count
                    elif '*Nset,' in line:
                        end = count
                        break
                    else:
                        count += 1

                temp = []
                for i in range(start, end):
                    temp.append(re.findall(r'[+-]?\d+\.*\d*', content[i]))
                elements.append(temp)

            elements = [[[float(f) for f in row] for row in dimension] for dimension in elements]
            nodes = [[[float(f) for f in row] for row in dimension] for dimension in nodes]
            # cool = sorted(nodes, key=lambda x: x[2],)
            # print elements
            # print cool
            last_layer = []
            for obj in range(len(nodes)):
                last_layer.append(min(nodes[obj], key=lambda x: x[2],)[2])
                # print obj
            list_of_layers = []
            print last_layer

            y = [[i[2] for i in dimension] for dimension in nodes]

            layers = []
            seen = set()
            seen_add = seen.add
            layer = [dimension for dimension in y]
            for i in layer:
                i = [x for x in i if not (x in seen or seen_add(x))]
                layers.append(i[::-1])

            print zip(layers[:][1:])
            print zip(layers[0][1:], layers[1][1:])

            for layer in zip(layers[0][1:], layers[1][1:]):
                list(layer)
                x = []
                y = []
                z = []
                node_numbers = []
                element_numbers = []

                print "layer =" + str(layer)
                print "Last Layer =" + str(last_layer)

                for k, first_layer, second_layer in zip(nodes, layer, last_layer):
                    for i in k:
                        print first_layer
                        if i[2] <= first_layer and i[2] >= second_layer:
                            node_numbers.append((i[0]))
                            x.append(i[1])
                            y.append(i[2])
                            z.append(i[3])

                #print y
                last_layer = layer

                for k in elements:
                    for i in k:
                        element_numbers.append(i[0])

                elements_to_write = []

                for index, elemnum  in enumerate(element_numbers):
                    number_of_nodes = 0
                    for node in node_numbers:
                        if node in elements[0][index][1:8] or elements[1][index][1:8]:
                            number_of_nodes += 1

                    if number_of_nodes == 7:
                        elements_to_write.append(elemnum)

                elements_to_write = [int(i) for i in elements_to_write]
                print elements_to_write
                list_of_layers.append(elements_to_write)

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(x, y, z, zdir='y')
                ax.set_xlim(-.5, .25)
                ax.set_ylim(-.25, .5)
                ax.set_zlim(-.25, .25)
                plt.show()

            list_of_layers = [[int(x) for x in row] for row in list_of_layers]
            print list_of_layers




if __name__== "__main__":

    #mymodel = mdb.models['Contact_Test']
    mymodel = None

    grabnodes =GetElements("Heat_Job.inp", 'Block-1-1', mymodel)
    grabnodes.getnodes(20)