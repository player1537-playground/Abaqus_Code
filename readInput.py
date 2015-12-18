__author__ = 'michael'
import re
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class GetElements():

    def __init__(self, inputfile):
        self.inputfile = inputfile
        pass


    def getnodes(self, layers):

        nodes = []
        elements=[]
        filehandle = open(self.inputfile, 'r')

        with filehandle as f:
            content = f.readlines()
            count = 0
            start = 0
            end = 0
            for line in content:
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

            count = 0

            for line in content:
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
            last_layer = min(nodes, key=lambda x: x[2],)[2]
            list_of_layers = []

            y = [i[2] for i in nodes]

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
                    if i[2] <= layer and i[2] >= last_layer:
                        node_numbers.append((i[0]))
                        x.append(i[1])
                        y.append(i[2])
                        z.append(i[3])

                #print y
                last_layer = layer

                for i in elements:
                    element_numbers.append(i[0])

                elements_to_write = []

                for index, elemnum  in enumerate(element_numbers):
                    number_of_nodes = 0
                    for node in node_numbers:
                        if node in elements[index][1:8]:
                            number_of_nodes+= 1

                    if number_of_nodes == 7:
                        elements_to_write.append(elemnum)

                elements_to_write = [int(i) for i in elements_to_write]
                print elements_to_write
                list_of_layers.append(elements_to_write)

            print list_of_layers
            '''fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z, zdir='y')
            ax.set_xlim(-.5,.25)
            ax.set_ylim(-.25,.5)
            ax.set_zlim(-.25,.25)
            plt.show()'''

if __name__== "__main__":
    grabnodes =GetElements("Heat_Job.inp")
    grabnodes.getnodes(20)