__author__ = 'michael'
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class GetElements():

    def __init__(self, inputfile):
        self.inputfile = inputfile
        pass


    def getnodes(self):

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

            x = []
            y = []
            z = []
            node_numbers = []
            element_numbers = []
            for i in nodes:
                if float(i[2]) <= -.2:
                    node_numbers.append((i[0]))
                    x.append(i[1])
                    y.append(i[2])
                    z.append(i[3])

            for i in elements:
                element_numbers.append(i[0])

            elements_to_write = []
            print element_numbers[len(element_numbers) - 1]

            for index, elemnum  in enumerate(element_numbers):
                number_of_nodes = 0
                for node in node_numbers:
                    if node in elements[index][1:8]:
                        number_of_nodes+= 1

                if number_of_nodes == 7:
                    elements_to_write.append(elemnum)

            elements_to_write = [int(i) for i in elements_to_write]
            print elements_to_write

            #print y
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z, zdir='y')
            ax.set_xlim(-.5,.25)
            ax.set_ylim(-.25,.5)
            ax.set_zlim(-.25,.25)
            plt.show()

if __name__== "__main__":
    grabnodes =GetElements("Heat_Job.inp")
    grabnodes.getnodes()