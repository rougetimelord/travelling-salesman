import csv
import os
from datetime import datetime
from route import Route
from random import randint
import genetics
import json

place_list = []
gen = []
names = []
gen_num = 0
gen_size = 75
dna_seqs = []
json_out = {} 

def load():
    global place_list
    if not os.path.isfile('places.csv'):
        print("No place list found")
        return -1
    
    temp = []
    with open('places.csv', 'r') as f:
        reader = csv.reader(f)
        temp = list(reader)

    for cur_place in temp:
        place_obj = {'x': '', 'y': ''}
        names.append(cur_place[0])
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
            
def run_gen():
    global gen_num
    global gen
    global dna_seqs
    gen.clear()
    start_time = datetime.now()
    for i in range(gen_size):
        dna = []
        if len(dna_seqs) > 0:
            dna = dna_seqs[i]
        gen.append(Route({'gen': gen_num, 'dna': dna, 'id': i}, place_list))
    gen = sorted(gen, key = lambda route: route.dist)
    dnas = []
    total_dist = 0
    for route in gen:
        dnas.append(route.dna)
        total_dist += route.dist
    fitnesses = []
    floor = 0
    dna_seqs.clear()
    dna_seqs.append(gen[0].dna)
    for route in gen:
        tmp = route.dist / total_dist
        rng = int((1-tmp)*10000)
        ciel = floor + rng
        fit = {'floor': floor, 'ciel': ciel}
        floor = ciel
        fitnesses.append(fit)
    dna_seqs += genetics.make_dna(gen_size - 1, dnas, fitnesses)
    total_time = datetime.now() - start_time
    top_five = []
    for i in range(5):
        top_five.append(str(int(gen[i].dist)))
    data = {'names': [],'coords': [], 'funcs': [], 'dist': 0}
    tmp = gen[0].dna[:]
    tmp_places = names[:]
    tmp_places_xy = place_list[:]
    for i in range(len(tmp)):
        data['names'].append(tmp_places[tmp[i]])
        tmp_places.pop(tmp[i])
        xy1 = tmp_places_xy[tmp[i]]
        tmp_places_xy.pop(tmp[i])
        if i < len(tmp) - 1:
            xy2 = tmp_places_xy[tmp[i + 1]]
        else:
            xy2 = place_list[tmp[0]]
        m = (xy2['y'] - xy1['y'])/(xy2['x']-xy1['x'])
        b = xy1['y']-m*xy1['x']
        if xy1['x'] > xy2['x']:
            gt = xy2['x']
            lt = xy1['x']
        else:
            lt = xy2['x']
            gt = xy1['x']
        data['funcs'].append("f(x)={}x+{}{{{}<x<{}}}".format(m,b,gt,lt))
        data['coords'].append([xy1['x'],xy1['y']])
        data['dist'] = gen[0].dist
        json_out[gen_num] = data
        if(gen_num % 10 ==0):
            with open('best.json', 'w', newline='') as file:
                json.dump(json_out, file, separators=(',', ': '), indent=4)
    print("Generation %s \n \
    Best 5 distances: %s \n \
    Time taken: %s \n \
    Gen size: %s \n \
    Number of places: %s \n"  % ( gen_num,
        ' '.join(top_five), total_time, 
        gen_size, len(place_list)))
    gen_num += 1
    
def main():
    while True:
        run_gen()

if __name__ == '__main__':
    load()
