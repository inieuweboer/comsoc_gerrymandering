import random

class Voter:
    def __init__(self):
        self.preferences = self.get_pref()

    def get(self, number):
        return self.preferences[number]

    def get_pref(self):
    	prefList = []
    	alternatives = ['a','b','c']
    	index = int(random.uniform(0, len(alternatives)))
    	prefList.append(alternatives.pop(index))
    	index = int(random.uniform(0, len(alternatives)))
    	prefList.append(alternatives.pop(index))
    	prefList.append(alternatives.pop(0))   	
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


def rule_plurality(profile):
    score = {};
    score['a'] = score['b'] = score['c'] = 0;
    for voter in profile:
        score[voter.get(1)] += 1;

    # return max
    return score


def main():
    grid = Grid(5)
    score_plur = rule_plurality(grid.profile())
    for voter in grid.profile():
    	print voter.get(1)+voter.get(2)+voter.get(3)
    print(score_plur)


if __name__ == "__main__":
    main()
