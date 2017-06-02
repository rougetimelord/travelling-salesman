from random import randint
import math

class Route(object):
    """tracks a route"""
    def __init__(self, args, place_list):
        self.route_stack = []
        self.places = place_list
        self.zero_gen = False
        self.dist = 0
        if args['gen'] == 0:
            self.zero_gen = True
        else:
            self.dna = args['dna']
        self.id = args['id'] 
        self.gen_route()

    def gen_route(self):
        if self.zero_gen:
            for i in range(len(self.places)):
                rand = randint(0, len(self.places) - (i + 1))
                self.route_stack.append(rand)
        else:
            for i in range(len(self.dna)):
                rand = randint(1, 1E3)
                if rand <= 10 and self.id != 0:
                    self.route_stack.append(randint(0, len(self.places)-(i+1)))
                else:
                    self.route_stack.append(self.dna[i])
        self.dna = self.route_stack
        self.calc_dist()

    def calc_dist(self):
        tmp_places = self.places[:]
        for i in range(len(self.route_stack) - 1):
            one = tmp_places[self.route_stack[i]]
            tmp_places.pop(self.route_stack[i])
            two = tmp_places[self.route_stack[i + 1]]
            self.dist += self.find_dist(one, two)
        one = tmp_places[0]
        two = self.places[self.route_stack[0]]
        self.dist += self.find_dist(one, two)
        
    def find_dist(self, one, two):
        return math.sqrt(pow(abs(one['x']-two['x']),2)
                + pow(abs(one['y']-two['y']),2))
