import random
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle


class Voter:
    def __init__(self, grid, x, y, percentages, hot_on):
        self.grid = grid
        self.district = 0
        self.x = x
        self.y = y
        self.percentages = percentages
        self.hot_on = hot_on
        if hot_on:
            self.preferences = self.get_hotspot_pref(1, percentages)
        else:
            self.preferences = self.get_random_pref(percentages)

    def get_random_pref(self, percentages):
        prefList = ['a','b','c']
        random_scores = np.array([random.uniform(0, percentage) for percentage in percentages]) 
        ranks = random_scores.argsort()
        return {1: prefList[ranks[2]], 2: prefList[ranks[1]], 3: prefList[ranks[0]]}

    def get_hotspot_pref(self, power, percentages):
        prefList = ['a','b','c']
        distances = [pow(self.grid.distance((self.x, self.y), hotspot), power) for hotspot in self.grid.hotspots]
        random_scores = np.array([random.uniform(0, distance * 100 / (1 + percentages[i])) for i, distance in enumerate(distances)])
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

class District:
    def __init__(self, number):
        self.number = number
        self.voters = []
        self.conquer = False

    def addVoter(self, voter):
        self.voters.append(voter)
        voter.setDistrict(self.number)

    def removeVoter(self, voter):
        self.voters.remove(voter)

    def getVoters(self):
        return self.voters

    def getSize(self):
        return len(self.voters)

    def getNumber(self):
        return self.number

    def setConquer(self, conquer):
        self.conquer = conquer

    def getConquer(self):
        return self.conquer

    def plur_ask(self, voter):
        permission = True
        min_voters = int(self.getSize() / 3) + 1
        if self.conquer and voter.get(1) == 'a' and self.getPlurality('a') <= min_voters:
            permission = False
        return permission

    def plur_victory(self):
        victory = False
        min_voters = int(self.getSize() / 3) + 1
        if self.getPlurality('a') >= min_voters:
            victory = True
        return victory

    def getPlurality(self, alternative):
        return rule_plurality(self.voters)[alternative]

    def borda_ask(self, voter):
        permission = True
        min_points = int(self.getSize() * 3 / 3) + 1
        if self.conquer and voter.get(3) != 'a' and self.getBorda('a') <= min_points:
            permission = False
        return permission

    def borda_victory(self):
        victory = False
        min_points = int(self.getSize() * 3 / 3) + 1
        if self.getBorda('a') >= min_points:
            victory = True
        return victory

    def getBorda(self, alternative):
        return rule_borda(self.voters)[alternative]


class Grid:
    def __init__(self, size, districts, percentages, hot_on, prop_lim):
        self.size = size
        self.grid = {}
        self.percentages = percentages
        self.hot_on = hot_on
        self.prop_lim = prop_lim
        if hot_on:
            self.hotspots = self.hotspots()
        self.districts = districts
        self.dist_list = []
        for i in range(districts):
            self.dist_list.append(District(i))
        for x in range(size):
            self.grid[x] = {} 
            for y in range(size):
                self.grid[x][y] = Voter(self, x, y, percentages, hot_on)
        self.init_districts()

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
                self.dist_list[dist].addVoter(self.grid[x][y])

    def get_divisors(self):
        divisor = math.floor(math.sqrt(self.districts))
        while self.districts % divisor != 0:
            divisor -= 1
        return divisor, self.districts / divisor

    def plur_gerry(self):
        self.rule = 'plurality'
        plur_conquer = self.plur_conquer()
        scores_in_dists = np.array([dist.getPlurality('a') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(min(plur_conquer, self.districts)):
            self.dist_list[ranks[i]].setConquer(True)
        first_dist = random.choice(self.dist_list)
        found_neighbour, new_district, old_district, last_voter = self.plur_step(first_dist)
        max_iterations = 200
        iteration = 0
        while found_neighbour and (self.plur_victory(plur_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.plur_step(new_district, old_district)
            iteration += 1
            # one district gets one too many voters and another gets one less correction - work in progress
            # if (found_neighbour == False):
            #     self.dist_list[old_district].addVoter(save_last_voter)
            #     self.dist_list[save_last_voter.getDistrict()].removeVoter(save_last_voter)
            # elif (self.plur_victory(plur_conquer)) or (iteration >= max_iterations):
            #     new_district.addVoter(last_voter)
            #     self.dist_list[old_district].removeVoter(last_voter)
            # save_last_voter = last_voter

    def plur_step(self, dist, last_dist=-1):
        neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.getDistrict() != last_dist]
        found_neighbour = False
        if dist.getConquer():
            good_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)]
            ok_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.dist_list[neighbour.getDistrict()].getConquer()]
            bad_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) != 'a' 
                and self.dist_list[neighbour.getDistrict()].getConquer()]
            very_bad_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) != 'a' 
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)]
        else:
            good_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and self.dist_list[neighbour.getDistrict()].getConquer()]
            ok_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)]
            bad_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)]
            very_bad_neighbours = [neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.dist_list[neighbour.getDistrict()].getConquer()]
        all_neighbours = good_neighbours + ok_neighbours + bad_neighbours + very_bad_neighbours
        for neighbour in all_neighbours:
            neighbour_dist = self.dist_list[neighbour.getDistrict()]
            if neighbour_dist.plur_ask(neighbour) and self.ask(neighbour):
                found_neighbour = True
                dist.addVoter(neighbour)
                neighbour_dist.removeVoter(neighbour)
                break;
        return found_neighbour, neighbour_dist, dist.getNumber(), neighbour

    def plur_victory(self, plur_conquer):
        victory = False
        victories = [dist for dist in self.dist_list if dist.plur_victory()]
        if len(victories) == plur_conquer:
            victory = True
        return victory

    def plur_conquer(self):
        points = rule_plurality(self.profile())['a']
        points_to_win_a_dist = int(((self.size * self.size) / self.districts) / 3) + 1
        plur_conquer = int(points / points_to_win_a_dist)
        return plur_conquer

    def plur_results(self):
        conquered_districts = [dist for dist in self.dist_list if dist.plur_victory()]
        dist_percentage = round(len(conquered_districts) / float(self.districts), 2)
        percentage = round(rule_plurality(self.profile())['a'] / float(self.size * self.size), 2)
        plur_conquer = self.plur_conquer()
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.districts) 
                    + ' when ' + str(plur_conquer) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

    def borda_gerry(self):
        self.rule = 'borda'
        borda_conquer = self.borda_conquer()
        scores_in_dists = np.array([dist.getBorda('a') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(min(borda_conquer, self.districts)):
            self.dist_list[ranks[i]].setConquer(True)
        first_dist = random.choice(self.dist_list)
        found_neighbour, new_district, old_district, last_voter = self.borda_step(first_dist)
        max_iterations = 200
        iteration = 0
        while found_neighbour and (self.borda_victory(borda_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.borda_step(new_district, old_district)
            iteration += 1

    def borda_step(self, dist, last_dist=-1):
        neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.getDistrict() != last_dist]
        found_neighbour = False
        neighbours_by_type = []
        if dist.getConquer():
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' 
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.dist_list[neighbour.getDistrict()].getConquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' 
                and self.dist_list[neighbour.getDistrict()].getConquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' 
                and self.dist_list[neighbour.getDistrict()].getConquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' 
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)])
        else:
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and self.dist_list[neighbour.getDistrict()].getConquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and (self.dist_list[neighbour.getDistrict()].getConquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and self.dist_list[neighbour.getDistrict()].getConquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and self.dist_list[neighbour.getDistrict()].getConquer()])
        all_neighbours = []
        for neighbour_group in neighbours_by_type:
            all_neighbours += neighbour_group
        for neighbour in all_neighbours:
            neighbour_dist = self.dist_list[neighbour.getDistrict()]
            if neighbour_dist.borda_ask(neighbour) and self.ask(neighbour):
                found_neighbour = True
                dist.addVoter(neighbour)
                neighbour_dist.removeVoter(neighbour)
                break;
        return found_neighbour, neighbour_dist, dist.getNumber(), neighbour

    def borda_victory(self, borda_conquer):
        victory = False
        victories = [dist for dist in self.dist_list if dist.borda_victory()]
        if len(victories) == borda_conquer:
            victory = True
        return victory

    def borda_conquer(self):
        points = rule_borda(self.profile())['a']
        points_to_win_a_dist = int(((self.size * self.size * 3) / self.districts) / 3) + 1
        borda_conquer = int(points / points_to_win_a_dist)
        return borda_conquer

    def borda_results(self):
        conquered_districts = [dist for dist in self.dist_list if dist.borda_victory()]
        dist_percentage = round(len(conquered_districts) / float(self.districts), 2)
        percentage = round(rule_borda(self.profile())['a'] / float(self.size * self.size * 3), 2)
        borda_conquer = self.borda_conquer()
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.districts) 
                    + ' when ' + str(borda_conquer) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

    def ask(self, voter):
        district = self.dist_list[voter.getDistrict()]
        voters = district.getVoters()[:]
        voters.remove(voter)
        approve = False
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        connected_voters = [voters[0]]
        new_voters = connected_voters[:]
        difference = True
        while difference:
            for voter in connected_voters:
                for option in options:
                    maybe_neighbour = self.grid[(voter.getX()+option[0]) % self.size][(voter.getY()+option[1]) % self.size]
                    if maybe_neighbour in voters and maybe_neighbour not in new_voters:
                        new_voters.append(maybe_neighbour)
            if len(new_voters) == len(connected_voters):
                difference = False
            connected_voters = new_voters[:]
        if len(connected_voters) == len(voters):
            approve = True
        if self.prop_lim and (self.check_prop(district) == False):
            approve = False
        return approve

    def check_prop(self, dist):
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        inner_voters = []
        approve = True
        voters = dist.getVoters()
        for voter in voters:
            inner = True
            for option in options:
                neighbour = self.grid[(voter.getX()+option[0]) % self.size][(voter.getY()+option[1]) % self.size]
                if neighbour.getDistrict() != dist.getNumber():
                    inner = False
            if inner:
                inner_voters.append(voter)
        if len(inner_voters) < int(len(voters) / 4):
            approve = False
        return approve

    def dist_neighbours(self, dist):
        neighbours = []
        options = [[0,-1],[-1,0],[1,0],[0,1]]
        for voter in dist.getVoters():
            for option in options:
                maybe_neighbour = self.grid[(voter.getX()+option[0]) % self.size][(voter.getY()+option[1]) % self.size]
                if maybe_neighbour.getDistrict() != dist.getNumber() and maybe_neighbour not in neighbours:
                    neighbours.append(maybe_neighbour)
        return neighbours

    def print_map(self):
        image = np.zeros(self.size*self.size)
        items = 0
        for x in range(self.size):
            for y in range(self.size):
                image[items] = self.grid[x][y].getDistrict()
                items += 1
        image = image.reshape((self.size, self.size)).swapaxes(0,1)
        fig, ax = plt.subplots(1)
        for x in range(self.size):
            for y in range(self.size):
                color = 'black'
                if self.rule == 'plurality':
                    if self.dist_list[self.grid[x][y].getDistrict()].plur_victory():
                        color = 'red'
                if self.rule == 'borda':
                    if self.dist_list[self.grid[x][y].getDistrict()].borda_victory():
                        color = 'red'
                if self.hot_on and (x,y) in self.hotspots:
                    color = 'white'
                # ax.text(x, y, self.grid[x][y].get(1)+self.grid[x][y].get(2)+self.grid[x][y].get(3), va='center', ha='center', color=color)
                ax.text(x, y, self.grid[x][y].get(1), va='center', ha='center', color=color)
        ax.xaxis.tick_top()
        ax.imshow(image, interpolation ='none', aspect = 'auto')
        plt.show()

def rule_plurality(profile):
    score = {}
    score['a'] = score['b'] = score['c'] = 0
    for voter in profile:
        score[voter.get(1)] += 1
    return score

def rule_borda(profile):
    score = {}
    score['a'] = score['b'] = score['c'] = 0
    for voter in profile:
        score[voter.get(1)] += 2
        score[voter.get(2)] += 1
    return score

def run_plurality(grid):
    print('plurality score:')
    print rule_plurality(grid.profile())
    grid.plur_gerry()
    grid.plur_results()

def run_borda(grid):
    print('borda score:')
    print rule_borda(grid.profile())
    grid.borda_gerry()
    grid.borda_results()

def main():
    size = 12
    districts = 6
    percentages=[33,33,33]
    hotspots_on = True
    proportion_limit = True
    grid = Grid(size, districts, percentages, hotspots_on, proportion_limit)
    if hotspots_on:
        print('hotspots:')
        print grid.hotspots

    run_plurality(grid)
    # run_borda(grid)

    # for dist in grid.dist_list:
    #     print dist.getSize()

    grid.print_map()

if __name__ == "__main__":
    main()


# ___BIN___

    # ___OLD ASK___
    # def ask(self, x, y):
    #     voter = self.grid[x][y]
    #     dist = voter.getDistrict()
    #     left = self.grid[(x-1) % self.size][y]
    #     right = self.grid[(x+1) % self.size][y]
    #     up = self.grid[x][(y-1) % self.size]
    #     down = self.grid[x][(y+1) % self.size]
    #     permission = False
    #     if self.check_voter(dist, voter) and self.check_voter(dist, left) and self.check_voter(dist, right) and self.check_voter(dist, up) and self.check_voter(dist, down):
    #         permission = True
    #     return permission
    # def check_voter(self, district, voter):
    #     x = voter.getX()
    #     y = voter.getY()
    #     center = self.grid[x][y].getDistrict()
    #     left = self.grid[(x-1) % self.size][y].getDistrict()
    #     right = self.grid[(x+1) % self.size][y].getDistrict()
    #     up = self.grid[x][(y-1) % self.size].getDistrict()
    #     down = self.grid[x][(y+1) % self.size].getDistrict()
    #     permission = True
    #     if center == district and district != left and district != right:
    #         permission = False
    #     if center == district and district != up and district != down:
    #         permission = False
    #     return permission

    # ___OLD PRINT___
    # image[::2] = np.random.random(self.size*self.size //2 + 1)
    # image = image.reshape((self.size, self.size))
    # plt.matshow(image)
    # plt.show()

    # ___RANDOM DISTRICTS___
    # def create_districts(self):
    #     num_assigned = 0
    #     voters = self.random_order()
    #     for i in range(self.districts):
    #         x = voters[i].getX()
    #         y = voters[i].getY()
    #         self.grid[x][y].setDistrict(i + 1)
    #         num_assigned += 1
    #     index = num_assigned
    #     while (num_assigned < self.size * self.size):
    #         x = voters[index].getX()
    #         y = voters[index].getY()
    #         # print("Assigned: " + str(num_assigned))
    #         if self.grid[x][y].getDistrict() == 0:
    #             dis = self.get_district_from_neighbors(x, y)
    #             if dis != 0:
    #                 self.grid[x][y].setDistrict(dis)
    #                 num_assigned += 1
    #         index += 1
    #         # print("Index: " + str(index))
    #         index %= self.size * self.size
    # def get_district_from_neighbors(self, x, y):
    #     # print("Checking for " + str(x) + " " + str(y))
    #     options = [[0,-1],[-1,0],[1,0],[0,1]]
    #     random.shuffle(options)
    #     option = options[0]
    #     x2 = x + option[0]
    #     y2 = y + option[1]
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
    #         return self.grid[x2][y2].getDistrict()
    #     option = options[1]
    #     x2 = x + option[0]
    #     y2 = y + option[1]
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
    #         return self.grid[x2][y2].getDistrict()
    #     option = options[2]
    #     x2 = x + option[0]
    #     y2 = y + option[1]
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
    #         return self.grid[x2][y2].getDistrict()
    #     option = options[3]
    #     x2 = x + option[0]
    #     y2 = y + option[1]
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].getDistrict() != 0:
    #         return self.grid[x2][y2].getDistrict()
    #     return 0