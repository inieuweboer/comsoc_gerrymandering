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
        # self.preferences = self.get_hotspot_pref(2)
        self.preferences = self.get_random_pref([33,33,33])

    def get_random_pref(self, percentages=[33,33,33]):
        prefList = ['a','b','c']
        random_scores = np.array([random.uniform(0, percentage) for percentage in percentages]) 
        ranks = random_scores.argsort()
        return {1: prefList[ranks[2]], 2: prefList[ranks[1]], 3: prefList[ranks[0]]}

    def get_hotspot_pref(self, power, percentages=[33,33,33]):
        prefList = ['a','b','c']
        distances = [pow(self.grid.distance((self.x, self.y), hotspot), power) for hotspot in self.grid.hotspots]
        random_scores = np.array([random.uniform(0, distance * percentages[i]) for i, distance in enumerate(distances)])
        ranks = random_scores.argsort()
        return {1: prefList[ranks[2]], 2: prefList[ranks[1]], 3: prefList[ranks[0]]}

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

class District:
    def __init__(self, number):
        self.number = number
        self.voters = []
        self.conquer = False

    def addVoter(self, voter):
        self.voters.append(voter)

    def getVoters(self):
        return self.voters

    def getNumber(self):
        return self.number

    def setConquer(self, conquer):
        self.conquer = conquer

    def getPlurality(self, alternative):
        return rule_plurality(self.voters)[alternative]

class Grid:
    def __init__(self, size, districts):
        self.size = size
        self.grid = {}
        self.hotspots = self.hotspots()
        self.districts = districts
        self.dist_list = []
        for i in range(districts):
            self.dist_list.append(District(i))
        for x in range(size):
            self.grid[x] = {} 
            for y in range(size):
                self.grid[x][y] = Voter(self, x, y)
        self.init_districts()
        self.plur_gerry()

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

    def init_districts(self):
        div1, div2 = self.get_divisors()
        x_dist = self.size / div2
        y_dist = self.size / div1
        for y in range(self.size):
            for x in range(self.size):
                dist = int(int(y / y_dist) * div2 + int(x / x_dist))
                self.grid[x][y].setDistrict(dist)
                self.dist_list[dist].addVoter(self.grid[x][y])

    def get_divisors(self):
        divisor = math.floor(math.sqrt(self.districts))
        while self.districts % divisor != 0:
            divisor -= 1
        return divisor, self.districts / divisor

    def plur_gerry(self):
        points = rule_plurality(self.profile())['a']
        points_to_win_a_dist = int(((self.size * self.size) / self.districts) / 3) + 1
        dist_to_conquer = int(points / points_to_win_a_dist)
        scores_in_dists = np.array([dist.getPlurality('a') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(dist_to_conquer):
            self.dist_list[ranks[i]].setConquer(True)
        # for voter in self.dist_neighbours(self.dist_list[0]):
        #     print voter.getX(), voter.getY()

    def dist_neighbours(self, dist):
        neighbours = []
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        for voter in dist.getVoters():
            for option in options:
                maybe_neighbour = self.grid[(voter.getX()+option[0]) % self.size][(voter.getY()+option[1]) % self.size]
                if maybe_neighbour.getDistrict() != dist.getNumber() and maybe_neighbour not in neighbours:
                    neighbours.append(maybe_neighbour)
        return neighbours

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

        image = image.reshape((self.size, self.size)).swapaxes(0,1)
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
    return score

def main():
    grid = Grid(12, 6)
    # grid.create_districts()

    print('hotspots:')
    print grid.hotspots

    print('plurality score:')
    print rule_plurality(grid.profile())

    grid.print_map()

if __name__ == "__main__":
    main()