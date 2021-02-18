#Author: Gordon Tang
#Citations:
#K Hong, Ph.D. (Feb 2021) <GRAPH DATA STRUCTURE> [example code]. https://www.bogotobogo.com/python/python_graph_data_structures.php
from random import random, randint, seed
import csv

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return "Vertex: " + str(self.id) + '   Adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0, pLevel=0):
        self.adjacent[neighbor] = [weight, pLevel]

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor][0]

    def get_pLevel(self, neighbor):
        return self.adjacent[neighbor][1]

    def add_pLevel(self,neighbor, amount):
        self.adjacent[neighbor][1] = amount + self.adjacent[neighbor][1]

    def set_pLevel(self,neighbor, amount):
        self.adjacent[neighbor][1] = amount

    def print_pLevel(self):
        for a in self.adjacent:
            print(self.id, "-", a.id, str(self.get_pLevel(a)))

    def print_weight(self):
        for a in self.adjacent:
            print(self.id, "-", a.id, str(self.get_weight(a)))

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def print(self):
        self.print_weighted_graph()
        print("")
        self.print_pLevel()

    def print_weighted_graph(self):
        print("Graph:")
        for v in self.vert_dict:
            print(self.get_vertex(v))

        print("")
        print("Weights:")
        for v in self.vert_dict:
            self.get_vertex(v).print_weight()

    def print_pLevel(self):
        print("P-Levels:")
        for v in self.vert_dict:
            self.get_vertex(v).print_pLevel()

    def get_pLevel(self):
        lis = []
        for v in self.vert_dict:
            v = self.get_vertex(v)
            for n in v.get_connections():
                lis.append(v.get_pLevel(n))
        return lis

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def decay(self,rate):
        for frm in self.vert_dict:
            frm = self.get_vertex(frm)
            for to in frm.get_connections():
                curr_pLevel = frm.get_pLevel(to)
                curr_pLevel = curr_pLevel * rate
                frm.set_pLevel(to,curr_pLevel)


    def get_distance(self, route):
        dist = 0

        for i in range(len(route)-1):
            frm = self.get_vertex(route[i])
            to = self.get_vertex(route[i+1])
            dist = dist + frm.get_weight(to)
        return dist

    def updateP(self, route):
        '''takes a route array and update pLevel of edges visited'''
        #loop through the route and update pheremone trail based on quality of route as determined by distance
        update_amount = self.generate_score(route)
        for i in range(len(route)-1):

            #get vertices to compare with
            frm = self.get_vertex(route[i])
            to = self.get_vertex(route[i+1])
            frm.add_pLevel(to, update_amount)

    def generate_score(self, route):
        return abs(self.get_distance(route)-26)

class Ant():
    def __init__(self,id):
        self.id = id

    def construct_path(self):
        temp_list = list(g.get_vertices()).copy()
        temp_list = temp_list[1:]
        path = ['a']
        curr_node = g.get_vertex('a')

        while temp_list:
            if random() < 0.2:
                random_index = randint(0,len(temp_list)-1)
                max_node = temp_list[random_index]
            else:
                #get max pLevel
                max = 0
                max_node = ''
                for key in temp_list:
                    key = g.get_vertex(key)
                    if curr_node.get_pLevel(key) > max:
                        max = curr_node.get_pLevel(key)
                        max_node = key.get_id()

                if not max_node:
                    random_index = randint(0,len(temp_list)-1)
                    max_node = temp_list[random_index]

                #update list and path
                temp_list.remove(max_node)
                path.append(max_node)

        pass
        path.append('a')
        return path


g = Graph()
seed(10)
filename = 'weWinThese.csv'

if __name__ == '__main__':
    count = 100
    agents = []

    with open(filename, 'w', newline='') as write_obj:
        fieldnames = ['time', '1', '2','3','4','5','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12']
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(fieldnames)

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')

    g.add_edge('a', 'b', 5)
    g.add_edge('a', 'c', 8)
    g.add_edge('a', 'd', 10)
    g.add_edge('b', 'a', 5)
    g.add_edge('b', 'c', 6)
    g.add_edge('b', 'd', 3)
    g.add_edge('c', 'a', 8)
    g.add_edge('c', 'b', 6)
    g.add_edge('c', 'd', 5)
    g.add_edge('d', 'a', 10)
    g.add_edge('d', 'b', 3)
    g.add_edge('d', 'c', 5)


    for i in range(1):
        agents.append(Ant(i))

    while count>0:
        for x in agents:
            path = x.construct_path()
            pLvl = g.get_pLevel()
            #save path 
            with open(filename, 'a+', newline='') as write_obj:
                csv_writer = csv.writer(write_obj)
                csv_writer.writerow([count,path[0],path[1],path[2],path[3],path[4],
                pLvl[0],pLvl[1],pLvl[2],pLvl[3],pLvl[4],pLvl[5],pLvl[6],pLvl[7],pLvl[8],pLvl[9],pLvl[10],pLvl[11]])

            g.updateP(path)
        g.decay(rate = 0.9)
        count -= 1

    print("program end")


''' conversion between pLvl-index and node pair
a - b
a - c
a - d
b - a
b - c
b - d
c - a
c - b
c - d
d - a
d - b
d - c
'''
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print(f'( {vid} , {wid}, {v.get_weight(w):.2f})')
    #
    # for v in g:
    #     print('g.vert_dict[%s]=%s' %(v.get_id(), g.vert_dict[v.get_id()]))

    # print(g.vert_dict['a'])
