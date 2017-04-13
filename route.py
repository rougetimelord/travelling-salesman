from random import randint
class Route(object):
    """tracks a new route"""
    def __init__(self, args, place_list):
        self.route_stack = []
        self.places = place_list
        self.zero_gen = False
        self.dist = 0
        if args['gen'] == 0:
            self.zero_gen = True
        else:
            self.dna = args['dna']
        self.gen_route()

    def gen_route(self):
        if self.zero_gen:
            for i in range(len(self.places)):
                rand = randint(0, len(self.places) - (i + 1))
                self.route_stack.append(rand)
        else:
            for i in range(len(self.dna)):
                rand = randint(1, 1E3)
                if rand <= 5:
                    rand = randint(0, len(self.places) - (i + 1))
                    self.route_stack.append(rand)
                else:
                    self.route_stack.append(self.dna[i])
        self.dna = self.route_stack
        self.calc_dist()

    def calc_dist(self):
        from travelling_salesman import find_dist
        tmp_places = self.places[:]
        for i in range(len(self.route_stack) - 2):
            one = tmp_places[self.route_stack[i]]
            tmp_places.pop(self.route_stack[i])
            two = tmp_places[self.route_stack[i + 1]]
            self.dist += find_dist(one['x'], two['x'], one['y'], two['y'])
        one = tmp_places[0]
        two = self.places[self.route_stack[0]]
        self.dist += find_dist(one['x'], two['x'], one['y'], two['y'])
        