import random
from math import sqrt
from itertools import product
from random import shuffle

class Voter:
    def __init__(self):
        self.preferences = self.get_pref()

    def get(self, number):
        return self.preferences[number]

    def get_pref(self):
        prefList = ['a','b','c']
        shuffle(prefList)
        return {1: prefList[0], 2: prefList[1], 3: prefList[2]}

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = {}
        for x in range(size):
            self.grid[x] = {}
            for y in range(size):
                self.grid[x][y] = Voter()

    def profile(self):
        profile = []
        for x in range(self.size):
            for y in range(self.size):
                profile.append(self.grid[x][y])

        return profile

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

    score_plur = rule_plurality(grid.profile())
    print('voter preferences:')
    for voter in grid.profile():
        print voter.get(1)+voter.get(2)+voter.get(3)

    print(score_plur)

    print('districts:')
    grid.divide_equal_districts(4)
    for distr in grid.districts:
        print(distr)


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
