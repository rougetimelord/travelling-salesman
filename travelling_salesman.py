import csv
import os
from datetime import datetime
from route import Route
from random import randint
import json

place_list = []
gen = []
gen_num = 0
gen_size = 75
dna_seqs = []
json_out = {}
fit_array = [] 
pool = 0

def load():
    global place_list
    global json_out
#Check that file exists
    if not os.path.isfile('places.csv'):
        print("No place list found")
        exit()
#Read place list
    temp = []
    with open('places.csv', 'r') as f:
        reader = csv.reader(f)
        temp = list(reader)
#Turn raw place list into a list filled with dictionaries
#Also create the setup field
    setup = {}
    for cur in temp:
        try:
            place_obj = {'x': float(cur[1]), 'y': float(cur[2])}
            setup.update({cur[0]: place_obj})
            place_list.append(place_obj)
        except ValueError:
            #Make sure we have an actual number
            print('%s has an invalid float value' % cur[0])
            exit()
    json_out.update({'setup': setup})
    main()

def make_dna(dna_s):
#Make new DNA strands
    res = []
    for i in range(gen_size - 1):
#Find two parents and merge
        one = dna_s[pick_parent()]
        two = dna_s[pick_parent()]
        if randint(0, 1) == 0:
            res.append(one[:len(one)] + two[len(two):])
        else:
            res.append(two[:len(two)] + one[len(one):])
    return res

def pick_parent():
#Randomly pick a parent
    select = randint(0, pool - 1)
    for i in range(len(fit_array)):
        if select >= fit_array[i]['floor'] and select < fit_array[i]['ciel']:
            return i
            
def run_gen():
#Run a generation
    global gen_num
    global gen
    global dna_seqs
    global json_out
    global fit_array
    global pool
#Clear variables
    gen.clear()
    fit_array.clear()
#Start time
    start_time = datetime.now()
    for i in range(gen_size):
    #Run an indvidual route
        dna = []
        if len(dna_seqs) > 0:
            dna = dna_seqs[i]
        gen.append(Route({'gen': gen_num, 'dna': dna, 'id': i}, place_list))
#Sort generation
    gen = sorted(gen, key = lambda route: route.dist)
#Figure out total distance and temporarily clone DNA
    dnas = []
    total_dist = 0
    for route in gen:
        dnas.append(route.dna)
        total_dist += route.dist
#Calculate selection ranges, probably could be better
    floor = 0
    for route in gen:
        tmp = route.dist / total_dist
        ciel = floor + int((1-tmp)*10000)
        fit_array.append({'floor': floor, 'ciel': ciel})
        floor = ciel
    pool = ciel
#Breed different routes
    dna_seqs = [dnas[0]] + make_dna(dnas)
#Finish time eveything that affects routes is done
    total_time = datetime.now() - start_time

#Get top 5 distances to print later
    top_five = ''
    for i in range(5):
        top_five += str(int(gen[i].dist)) + ' '
#Create a profile of the best route
    data = {'coords': [], 'dist': gen[0].dist}
    tmp_places_xy = place_list[:]
    for d in gen[0].dna:
        data['coords'].append(tmp_places_xy[d])
        tmp_places_xy.pop(d)
        json_out[gen_num] = data
#Dump best route data into a .json every 500 generations
    if gen_num % 500 == 0:
        print('Dumping JSON')
        with open('best.json', 'w', newline='') as file:
            json.dump(json_out, file, separators=(',', ': '), indent=4)
#Print out generation data
    print("Generation %s \n \
    Best 5 distances: %s \n \
    Time taken: %s \n \
    Gen size: %s \n \
    Number of places: %s \n"  % ( gen_num,
        top_five, total_time, 
        gen_size, len(place_list)))
#Increment generation number
    gen_num += 1
    
def main():
#Constantly run generations
    while True:
        run_gen()

if __name__ == '__main__':
    load()
