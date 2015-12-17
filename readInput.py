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
        filehandle = open(self.inputfile, 'r')

        with filehandle as f:
            content = f.readlines()
            count = 0
            start = 0
            end = 0
            for line in content:
                if line.find("*Node") >= 0:
                    count += 1
                    start = count
                elif line.find('*Element') >= 0:
                    end = count
                    break
                else:
                    count += 1



            for i in range(start, end):
                nodes.append(re.findall(r'[+-]?\d+\.*\d*', content[i]))
            #print sorted(nodes, key=lambda x: x[2],)
            x = []
            y = []
            z = []
            for i in nodes:
                x.append(i[1])
                y.append(i[2])
                z.append(i[3])

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z,)
            plt.show()

if __name__== "__main__":
    grabnodes =GetElements("Heat_Job.inp")
    grabnodes.getnodes()