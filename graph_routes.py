import json
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from time import sleep

graph_list = []
place_list = {}
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.axes.get_xaxis().set_ticklabels([])
ax.axes.get_yaxis().set_ticklabels([])


def update():
    for i in range(len(points)):
        p = points[i]
        if i < len(points) -1:
            p2 = points[i+1]
        else:
            p2 = points[0]
        ax.scatter(float(p[0]), float(p[1]),s=5,marker='o',c='b')
        ax.plot([float(p[0]),float(p2[0])], [float(p[1]),float(p2[1])])
    if gen % 500 == 0:
        fig.savefig('graphs/gen_{}.png'.format(gen))

def main():
    global graph_list
    global place_list
    start = int(input('Start index? '))
    step = int(input('Step amount? '))
    with open('best.json', 'r') as f:
        json_data = json.load(f)
    place_list = json_data['setup']
    for ii in range(start):
        json_data.pop(str(ii))
    i = 0
    while i < len(json_data):
        print('running gen {}'.format(start + i))
        data = json_data[str(start + i)]
        data.update({'gen': i + start})
        graph_list.append(data)
        i += step
    print('JSON loaded')
    ani = anim.Animation(fig, update, blit=True)
    fig.show(); 

if __name__ == '__main__':
    main()
