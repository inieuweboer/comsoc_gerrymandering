from math import sqrt
from itertools import product

class Voter:
    def __init__(self):
        self.preferences = {1: 'a', 2:'b', 3:'c'}

    def get(self, number):
        return self.preferences[number]


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

    print(score_plur)

    grid.divide_equal_districts(4)
    for distr in grid.districts:
        print(distr)


if __name__ == "__main__":
    main()
