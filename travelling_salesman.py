import csv
import os
from datetime import datetime
from route import Route
import math
from random import randint
import genetics

place_list = []
gen = []
gen_num = 0
gen_size = 20
dna_seqs = []

def load():
    if not os.path.isfile('places.csv'):
        return -1
    
    temp = []
    with open('places.csv', 'r') as f:
        reader = csv.reader(f)
        temp = list(reader)

    id_list = []
    for cur_place in temp:
        place_obj = {'id': '', 'x': '', 'y': ''}
        go = True
        id_len = 3
        while go:
            id = cur_place[0][:id_len]
            if id not in id_list:
                id_list.append(id)
                go = False
            else:
                 id_len += 1
        place_obj['id'] = id
        success = True
        try:
            place_obj['x'] = float(cur_place[1])
            place_obj['y'] = float(cur_place[2])
        except ValueError:
            success = False
            print('%s has an invalid float value' % cur_place[0])
        if success:        
            place_list.append(place_obj)
    main()
            
def find_dist(x1, x2, y1, y2):
    delt_x = abs(x1 - x2)
    delt_y = abs(y1 - y2)
    return math.sqrt(pow(delt_x, 2) + pow(delt_y, 2))

def main():
    global gen_num
    global gen
    global dna_seqs
    gen.clear()
    start_time = datetime.now()
    i = 0
    for i in range(gen_size):
        dna = []
        if len(dna_seqs) > 0:
            dna = dna_seqs[i]
        gen.append(Route({'gen': gen_num, 'dna': dna}, place_list))
    gen = sorted(gen, key = lambda route: route.dist)
    dnas = []
    total_dist = 0
    for route in gen:
        dnas.append(route.dna)
        total_dist += route.dist
    fitnesses = []
    floor = 0
    for route in gen:
        tmp = route.dist / total_dist
        ciel = floor + int((1 - tmp) * 1000)
        fit = {'floor': floor, 'ciel': ciel}
        floor = int(ciel)
        fitnesses.append(fit)
    dna_seqs = genetics.make_dna(gen_size, dnas, fitnesses)
    total_time = datetime.now() - start_time
    top_five = []
    for i in range(5):
        top_five.append(str(int(gen[i].dist)))
    with open('best.csv', 'w', newline='') as file:
        w = csv.writer(file)
        res = []
        tmp = gen[0].dna[:]
        tmp_places = place_list[:]
        for i in range(len(tmp) - 2):
            res.append(tmp_places[tmp[i]]['id'])
            tmp_places.pop(tmp[i])
        w.writerow([res, gen[0].dist])
    print("Generation %s \n \
    Best 5 distances: %s \n \
    Time taken: %s \n \
    Gen size: %s \n \
    Number of places: %s \n"  % ( gen_num,
        ' '.join(top_five), total_time, 
        gen_size, len(place_list)))
    gen_num += 1
    main()

if __name__ == '__main__':
    load()