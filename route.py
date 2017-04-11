from random import randint
class Route(object):
    """tracks a new route"""
    def __init__(self, args, place_list):
        self.route_stack = []
        self.tmp_places = place_list
        self.zero_gen = False
        self.dist = 0
        if args['gen'] == 0:
            self.zero_gen = True
        else:
            self.dna = args['dna']
        self.gen_route()

    def gen_route(self):
        if self.zero_gen:
            self.route_stack.append(self.tmp_places[0])
            self.tmp_places = self.tmp_places[1:]
            while len(self.tmp_places) > 0:
                rand = randint(0, len(self.tmp_places) - 1)
                self.route_stack.append(self.tmp_places[rand])
                del self.tmp_places[rand]
            self.route_stack.append(self.route_stack[0])
        else:
            self.route_stack.append(self.dna[0])
            for item in self.dna:
                rand = randint(1, 1E3)
                if rand <= 5:
                    ind = self.dna.index(item)
                    swap_ind = randint(ind, len(self.dna) - 2)
                    self.route_stack.append(self.dna[swap_ind])
                    self.dna[swap_ind] = item
                else:
                    self.route_stack.append(item)
            self.route_stack.append(self.dna[0])
        self.dna = self.route_stack
        self.calc_dist()

    def calc_dist(self):
        from travelling_salesman import find_dist
        for i in range(len(self.route_stack) - 1):
            one = self.route_stack[i]
            two = self.route_stack[i + 1]
            self.dist += find_dist(one['x'], two['x'], one['y'], two['y'])