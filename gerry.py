import random
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle


class Voter:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.district = 0
        self.x = x
        self.y = y
        # self.preferences = {1: 'a', 2:'b', 3:'c'}
        self.preferences = self.get_hotspot_pref(2)
        # self.preferences = self.get_random_pref()

    def get_random_pref(self):
        prefList = ['a','b','c']
        shuffle(prefList)   
        return {1: prefList[0], 2: prefList[1], 3: prefList[2]}

    def get_hotspot_pref(self, power):
        prefList = ['a','b','c']
        distances = [pow(self.grid.distance((self.x, self.y), hotspot), power) for hotspot in self.grid.hotspots]
        random_scores = np.array([random.uniform(0, distance) for distance in distances])
        ranks = random_scores.argsort()
        return {1: prefList[ranks[0]], 2: prefList[ranks[1]], 3: prefList[ranks[2]]}

    def get(self, number):
        return self.preferences[number]

    def getDistrict(self):
        return self.district

    def setDistrict(self, district):
        self.district = district

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class Grid:
    def __init__(self, size, districts):
        self.size = size
        self.grid = {}
        self.hotspots = self.hotspots()
        self.districts = districts
        for x in range(size):
            self.grid[x] = {} 
            for y in range(size):
                self.grid[x][y] = Voter(self, x, y)

    def profile(self):
        profile = []
        for x in range(self.size):
            for y in range(self.size):
                profile.append(self.grid[x][y])
        return profile

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

    def to_text(self):
        for x in range(self.size):
            row = ""
            for y in range(self.size):
                row += self.grid[x][y].get(1) + "  "
            sys.stdout.write(row + "\n")

    def distance(self, point1, point2):
        diff_x = abs(point1[0]-point2[0])
        diff_y = abs(point1[1]-point2[1])
        return math.sqrt(math.pow(min(diff_x, self.size - diff_x), 2) + math.pow(min(diff_y, self.size - diff_y), 2))

    def get_voter(self, x, y):
        return self.grid[x][y]

    def random_order(self):
        voters = self.profile()
        random.shuffle(voters)
        return voters

    def create_districts(self):
        num_assigned = 0
        voters = self.random_order()
        for i in range(self.districts):
            x = voters[i].getX()
            y = voters[i].getY()
            self.grid[x][y].setDistrict(i + 1)
            num_assigned += 1

        index = num_assigned

        while (num_assigned < self.size * self.size):
            x = voters[index].getX()
            y = voters[index].getY()

            # print("Assigned: " + str(num_assigned))

            if self.grid[x][y].getDistrict() == 0:
                dis = self.get_district_from_neighbors(x, y)
                if dis != 0:
                    self.grid[x][y].setDistrict(dis)
                    num_assigned += 1

            index += 1
            # print("Index: " + str(index))
            index %= self.size * self.size

    def get_district_from_neighbors(self, x, y):
        # print("Checking for " + str(x) + " " + str(y))
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        random.shuffle(options)
        option = options[0]
        x2 = x + option[0]
        y2 = y + option[1]

        if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
            return self.grid[x2][y2].getDistrict()

        option = options[1]
        x2 = x + option[0]
        y2 = y + option[1]

        if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
            return self.grid[x2][y2].getDistrict()

        option = options[2]
        x2 = x + option[0]
        y2 = y + option[1]

        if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
            return self.grid[x2][y2].getDistrict()

        option = options[3]
        x2 = x + option[0]
        y2 = y + option[1]

        if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
            return self.grid[x2][y2].getDistrict()

        return 0

    def print_map(self):
        image = np.zeros(self.size*self.size)
        items = 0

        for x in range(self.size):
            for y in range(self.size):
                image[items] = self.grid[x][y].getDistrict()
                items += 1

        # ___OLD PRINT___
        # image[::2] = np.random.random(self.size*self.size //2 + 1)
        # image = image.reshape((self.size, self.size))
        # plt.matshow(image)
        # plt.show()

        image = image.reshape((self.size, self.size))
        fig, ax = plt.subplots(1)
        for x in range(self.size):
            for y in range(self.size):
                if (x,y) in self.hotspots:
                    color = 'white'
                else:
                    color = 'black'
                # ax.text(x, y, self.grid[x][y].get(1)+self.grid[x][y].get(2)+self.grid[x][y].get(3), va='center', ha='center', color=color)
                ax.text(x, y, self.grid[x][y].get(1), va='center', ha='center', color=color)
        ax.xaxis.tick_top()
        ax.imshow(image, interpolation ='none', aspect = 'auto')
        plt.show()



def rule_plurality(profile):
    score = {};
    score['a'] = score['b'] = score['c'] = 0;
    for voter in profile:
        score[voter.get(1)] += 1;

    # return max
    print(score)

def main():
    grid = Grid(12, 4)
    grid.create_districts()

    print('hotspots:')
    print grid.hotspots

    print('plurality score:')
    rule_plurality(grid.profile())

    grid.print_map()

if __name__ == "__main__":
    main()