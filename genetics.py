from random import randint

pool = 0
fit_array = []
dna_seqs = []

def make_dna(gen_size, dnas, fitnesses):
    global pool
    global fit_array
    pool = fitnesses[len(fitnesses) - 1]['ciel']
    fit_array = fitnesses
    res = []
    for i in range(gen_size):
        one = dnas[pick_parent()]
        two = dnas[pick_parent()]
        order = randint(0, 1)
        if order == 0:
            res.append(one[:len(one)] + two[len(two):])
        else:
            res.append(two[:len(two)] + one[len(one):])
    return res

def pick_parent():
    select = randint(0, pool - 1)
    for i in range(len(fit_array)):
        if select >= fit_array[i]['floor'] and select < fit_array[i]['ciel']:
            return i