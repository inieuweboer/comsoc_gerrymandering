import random
import math

import numpy as np
import matplotlib.pyplot as plt

from district import *
from rules import *
from voter import *


class Grid:
    def __init__(self, size, districts, percentages, hot_on, prop_lim, hotspots=[]):
        self.size = size
        self.grid = {}
        self.rule = ''
        self.percentages = percentages
        # defines if there are hotspots around which voters are grouped
        self.hot_on = hot_on
        # defines if there is a limit on the ratio between area and perimeter of a district
        self.prop_lim = prop_lim
        if hot_on:
            self.hotspots = self.hotspots()
        if len(hotspots) > 0:
            self.hotspots = hotspots
        self.districts = districts
        self.dist_list = []
        # creates the districts
        for i in range(districts):
            self.dist_list.append(District(i))
        # generates the voters
        for x in range(size):
            self.grid[x] = {}
            for y in range(size):
                self.grid[x][y] = Voter(self, x, y, percentages, hot_on)
        self.init_districts()

    # returns a list of all the voters
    def profile(self):
        profile = []
        for x in range(self.size):
            for y in range(self.size):
                profile.append(self.grid[x][y])
        return profile

    # randomly chooses the points in the grid to be hotspots setting a minimal distance from each other proportional to the grid size
    def hotspots(self):
        min_distance = self.size / 2 - 1
        points = []
        hotspots = []
        for x in range(self.size):
            for y in range(self.size):
                points.append((x,y))
        hotspots.append(random.choice(points))
        points = [point for point in points if self.distance(point, hotspots[0]) > min_distance]
        hotspots.append(random.choice(points))
        points = [point for point in points if self.distance(point, hotspots[1]) > min_distance]
        hotspots.append(random.choice(points))
        return hotspots

    # calculates the distance between two voters as if they are on a toroidal grid
    def distance(self, point1, point2):
        diff_x = abs(point1[0]-point2[0])
        diff_y = abs(point1[1]-point2[1])
        return math.sqrt(math.pow(min(diff_x, self.size - diff_x), 2) + math.pow(min(diff_y, self.size - diff_y), 2))

    def get_voter(self, x, y):
        return self.grid[x][y]

    # returns voters in a random order
    def random_order(self):
        voters = self.profile()
        random.shuffle(voters)
        return voters

    # the districts are initialized as rectangles of equal size
    def init_districts(self):
        div1, div2 = self.get_divisors()
        x_dist = self.size / div2
        y_dist = self.size / div1
        for y in range(self.size):
            for x in range(self.size):
                dist = int(int(y / y_dist) * div2 + int(x / x_dist))
                self.dist_list[dist].add_voter(self.grid[x][y])

    # returns the two largest numbers that multiplied together give the number of districts
    def get_divisors(self):
        divisor = math.floor(math.sqrt(self.districts))
        while self.districts % divisor != 0:
            divisor -= 1
        return divisor, self.districts / divisor

    # checks if removing a voter from a district leaves the district connected and in case there is a proportion limit checks the district's proportions
    def ask(self, voter):
        district = self.dist_list[voter.get_district()]
        voters = district.get_voter()[:]
        voters.remove(voter)
        approve = False
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        connected_voters = [voters[0]]
        new_voters = connected_voters[:]
        difference = True
        while difference:
            for voter in connected_voters:
                for option in options:
                    maybe_neighbour = self.grid[(voter.get_x()+option[0]) % self.size][(voter.get_y()+option[1]) % self.size]
                    if maybe_neighbour in voters and maybe_neighbour not in new_voters:
                        new_voters.append(maybe_neighbour)
            if len(new_voters) == len(connected_voters):
                difference = False
            connected_voters = new_voters[:]
        if len(connected_voters) == len(voters):
            approve = True
        if self.prop_lim and (self.check_prop(district, voter) == False):
            approve = False
        return approve

    # checks whether the number of inner voters in a district is above a threshold in order to keep low the ratio between perimeter / area of the district
    def check_prop(self, dist, voter):
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        inner_voters = []
        approve = True
        voters = dist.get_voter()[:]
        voters.remove(voter)
        for voter in voters:
            inner = True
            for option in options:
                neighbour = self.grid[(voter.get_x()+option[0]) % self.size][(voter.get_y()+option[1]) % self.size]
                if neighbour.get_district() != dist.get_number():
                    inner = False
            if inner:
                inner_voters.append(voter)
        if len(inner_voters) < int(len(voters) / 3):
            approve = False
        return approve

    # returns a list of the neighbour voters of a district
    def dist_neighbours(self, dist):
        neighbours = []
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        for voter in dist.get_voter():
            for option in options:
                maybe_neighbour = self.grid[(voter.get_x()+option[0]) % self.size][(voter.get_y()+option[1]) % self.size]
                if maybe_neighbour.get_district() != dist.get_number() and maybe_neighbour not in neighbours:
                    neighbours.append(maybe_neighbour)
        return neighbours

    # prints a map where districts are divided by colours and the first preference of the voters is displayed in red if the voter belongs to a conquered district,
    # in white if there is an hotspot in his position on the grid or in black otherwise
    def prepare_map(self):
        image = np.zeros(self.size*self.size)
        items = 0
        for x in range(self.size):
            for y in range(self.size):
                image[items] = self.grid[x][y].get_district()
                items += 1
        image = image.reshape((self.size, self.size)).swapaxes(0,1)
        fig, ax = plt.subplots(1)
        for x in range(self.size):
            for y in range(self.size):
                color = 'black'
                # if self.dist_list[self.grid[x][y].get_district()].get_conquer():
                #     color = 'green'
                if self.rule == 'plurality':
                    if self.dist_list[self.grid[x][y].get_district()].plur_victory():
                        color = 'red'
                if self.rule == 'borda':
                    if self.dist_list[self.grid[x][y].get_district()].borda_victory():
                        color = 'red'
                if self.rule == 'copeland':
                    if self.dist_list[self.grid[x][y].get_district()].cope_victory():
                        color = 'red'
                if self.hot_on and (x,y) in self.hotspots:
                    color = 'white'
                # ax.text(x, y, self.grid[x][y].get(1)+self.grid[x][y].get(2)+self.grid[x][y].get(3), va='center', ha='center', color=color)
                ax.text(x, y, self.grid[x][y].get(1), va='center', ha='center', color=color)
        ax.xaxis.tick_top()
        ax.imshow(image, interpolation ='none', aspect = 'auto')

    def set_districts(self, districts):
        self.dist_list = districts
        for dist in self.dist_list:
            voters = dist.get_voter()[:]
            for voter in voters:
                dist.add_voter(self.grid[voter.get_x()][voter.get_y()])
                dist.remove_voter(voter)

    def set_rule(self, rule):
        self.rule = rule
