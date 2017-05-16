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
    grid = Grid(5)
    score_plur = rule_plurality(grid.profile())

    print(score_plur)


if __name__ == "__main__":
    main()
