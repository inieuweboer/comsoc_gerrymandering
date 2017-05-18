import random
import matplotlib.pyplot as plt
import numpy as np


class Voter:
    def __init__(self, x, y):
        self.preferences = {1: 'a', 2:'b', 3:'c'}
        self.district = 0
        self.x = x
        self.y = y

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
        self.districts = districts
        for x in range(size):
            self.grid[x] = {} 
            for y in range(size):
                self.grid[x][y] = Voter(x, y)

    def profile(self):
        profile = []
        for x in range(self.size):
            for y in range(self.size):
                profile.append(self.grid[x][y])
        return profile

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

            print("Assigned: " + str(num_assigned))

            if self.grid[x][y].getDistrict() == 0:
                dis = self.get_district_from_neighbors(x, y)
                if dis != 0:
                    self.grid[x][y].setDistrict(dis)
                    num_assigned += 1

            index += 1
            print("Index: " + str(index))
            index %= self.size * self.size

    def get_district_from_neighbors(self, x, y):
        print("Checking for " + str(x) + " " + str(y))
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


        # image[::2] = np.random.random(self.size*self.size //2 + 1)
        image = image.reshape((self.size, self.size))
        plt.matshow(image)
        plt.show()



def rule_plurality(profile):
    score = {};
    score['a'] = score['b'] = score['c'] = 0;
    for voter in profile:
        score[voter.get(1)] += 1;

    # return max
    print(score)

def main():
    grid = Grid(25, 6)
    grid.create_districts()
    grid.print_map()
    # rule_plurality(grid.profile())

if __name__ == "__main__":
    main()