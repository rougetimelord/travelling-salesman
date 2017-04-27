import json
import matplotlib.pyplot as plt
from time import sleep

json_data = {}
lastfig = 0

def drawGraphs(points, labels, gen, dist):
    global lastfig
    fig = plt.figure(gen)
    fig.canvas.set_window_title('Gen {}'.format(gen))
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.axes.get_xaxis().set_ticklabels([])
    ax.axes.get_yaxis().set_ticklabels([])
    str = "Gen: {} Dist: {}".format(gen,dist)
    ax.annotate(str, xy=(0,1),
        xytext=(0.8, 0.95), xycoords='figure fraction',
        horizontalalignment='right', verticalalignment='top',
        fontsize=20)
    for i in range(len(points)):
        p = points[i]
        if i < len(points) -1:
            p2 = points[i+1]
        else:
            p2 = points[0]
        ax.scatter(float(p[0]), float(p[1]),s=5,marker='o',c='b')
        ax.plot([float(p[0]),float(p2[0])], [float(p[1]),float(p2[1])])
    if not gen == 0:
        sleep(2)
        plt.close(lastfig)
        lastfig = gen
    fig.show()

def loadJSON():
    global json_data
    with open('best.json', 'r') as f:
        json_data = json.load(f)
    print('JSON loaded')

def main():
    print('Started')
    loadJSON()
    for i in range(len(json_data)):
        print('running gen {}'.format(i))
        data = json_data[str(i)]
        p = data['coords']
        n = data['names']
        d = data['dist']
        drawGraphs(p, n, i, d)
    input('Enter to exit')
    exit()

if __name__ == '__main__':
    main()