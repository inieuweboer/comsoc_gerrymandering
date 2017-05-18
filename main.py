import random
import math
import numpy as np
import sys
from math import sqrt
from itertools import product
from random import shuffle

class Voter:
    def __init__(self, grid, position):
        self.grid = grid
        self.position = position
        # self.preferences = self.get_pref()
        self.preferences = self.get_hotspot_pref()

    def get(self, number):
        return self.preferences[number]

    def get_pref(self):
        prefList = ['a','b','c']
        shuffle(prefList)   
        return {1: prefList[0], 2: prefList[1], 3: prefList[2]}

    def get_hotspot_pref(self):
        prefList = ['a','b','c']
        distances = [pow(self.grid.distance(self.position, hotspot),1) for hotspot in self.grid.hotspots]
        random_scores = np.array([random.uniform(0, distance) for distance in distances])
        ranks = random_scores.argsort()
        return {1: prefList[ranks[0]], 2: prefList[ranks[1]], 3: prefList[ranks[2]]}


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = {}
        self.hotspots = self.hotspots()
        for x in range(size):
            self.grid[x] = {}
            for y in range(size):
                self.grid[x][y] = Voter(self, (x,y))

    def hotspots(self):
        min_distance = 3
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

    def distance(self, point1, point2):
        diff_x = abs(point1[0]-point2[0])
        diff_y = abs(point1[1]-point2[1])
        return math.sqrt(math.pow(min(diff_x, self.size - diff_x), 2) + math.pow(min(diff_y, self.size - diff_y), 2))

    def profile(self):
        profile = []
        for x in range(self.size):
            for y in range(self.size):
                profile.append(self.grid[x][y])
        return profile

    def to_text(self):
        for x in range(self.size):
            row = ""
            for y in range(self.size):
                row += self.grid[x][y].get(1) + "  "
            sys.stdout.write(row + "\n")   

    def divide_equal_districts(self, no_distrs):
        # Create a list of districts. The square that is nearest low to no_districts is used
        # We also assume the square root divides self.size
        sqrt_distrs = int(sqrt(no_distrs))
        div = self.size / sqrt_distrs

        self.districts = []

        # in x range
        for i in xrange(sqrt_distrs):
            for j in xrange(sqrt_distrs):
                # Initially the cartesian product of equally sized lists
                grid_points = list(product(xrange(div*i, div*(i+1)), xrange(div*j, div*(j+1))))

                self.districts.append(District(grid_points))

class District:
    def __init__(self, grid_points):
        # This is a list of grid points that belong to this district
        self.grid_points = grid_points

    def __str__(self):
        return str(self.grid_points)


def rule_plurality(profile):
    score = {};
    score['a'] = score['b'] = score['c'] = 0;
    for voter in profile:
    	score[voter.get(1)] += 1;

    # return max
    return score


def rule_borda(profile):
    score = {}
    score['a'] = score['b'] = score['c'] = 0
    for voter in profile:
        score[voter.preferences(1)] += 2
        score[voter.preferences(2)] += 1
    return score


def main():
    grid = Grid(12)
    score_plur = rule_plurality(grid.profile())

    # print('voter preferences:')
    # for voter in grid.profile():
    #     print voter.get(1)+voter.get(2)+voter.get(3)

    print('hotspots:')
    print grid.hotspots

    print('grid:')
    grid.to_text()

    print('plurality score:')
    print(score_plur)

    # print('districts:')
    # grid.divide_equal_districts(4)
    # for distr in grid.districts:
    #     print(distr)


if __name__ == "__main__":
    main()



# _____BIN_____
    # alternatives = ['a','b','c']
    # prefList = []
    # index = int(random.uniform(0, len(alternatives)))
    # prefList.append(alternatives.pop(index))
    # index = int(random.uniform(0, len(alternatives)))
    # prefList.append(alternatives.pop(index))
    # prefList.append(alternatives.pop(0)) 
