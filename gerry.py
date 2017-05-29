import random
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
import operator

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

    # preferences are generated randomly according to the percentages using a uniform distribution
    def get_random_pref(self, percentages):
        prefList = ['a','b','c']
        random_scores = np.array([random.uniform(0, percentage) for percentage in percentages]) 
        ranks = random_scores.argsort()
        return {1: prefList[ranks[2]], 2: prefList[ranks[1]], 3: prefList[ranks[0]]}

    # preferences depend on the distance from the hotspots, one for each alternative, and on the precentages
    def get_hotspot_pref(self, power, percentages):
        prefList = ['a','b','c']
        distances = [pow(self.grid.distance((self.x, self.y), hotspot), power) for hotspot in self.grid.hotspots]
        random_scores = np.array([random.uniform(0, distance * 100 / (1 + percentages[i])) for i, distance in enumerate(distances)])
        ranks = random_scores.argsort()
        return {1: prefList[ranks[0]], 2: prefList[ranks[1]], 3: prefList[ranks[2]]}

    def get(self, number):
        return self.preferences[number]

    def get_district(self):
        return self.district

    def set_district(self, district):
        self.district = district

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class District:
    def __init__(self, number):
        self.number = number
        self.voters = []
        # it defines if the district is to be conquered by the gerrymandarer or left to another variable
        self.conquer = False

    def add_voter(self, voter):
        self.voters.append(voter)
        voter.set_district(self.number)

    def remove_voter(self, voter):
        self.voters.remove(voter)

    def get_voter(self):
        return self.voters

    def get_size(self):
        return len(self.voters)

    def get_number(self):
        return self.number

    def set_conquer(self, conquer):
        self.conquer = conquer

    def get_conquer(self):
        return self.conquer

    # returns the plurality winner of the district
    def plur_first(self):
        plurality = rule_plurality(self.voters)
        return max(plurality.iteritems(), key=operator.itemgetter(1))[0]

    # gives the permission to remove a voter if his vote is not necessary to conquer the district under plurality
    def plur_ask(self, voter):
        permission = True
        if self.conquer and voter.get(1) == 'a' and (self.get_plurality('a') <= self.get_plurality('b') or self.get_plurality('a') <= self.get_plurality('c')):
            permission = False
        return permission

    # checks if the district has been conquered under plurality
    def plur_victory(self):
        victory = False
        if self.get_plurality('a') > self.get_plurality('b') and self.get_plurality('a') > self.get_plurality('c'):
            victory = True
        return victory

    # runs the plurality rule restricted to the voters belonging to the district
    def get_plurality(self, alternative):
        return rule_plurality(self.voters)[alternative]

    # returns the borda winner of the district
    def borda_first(self):
        borda = rule_borda(self.voters)
        return max(borda.iteritems(), key=operator.itemgetter(1))[0]

    # gives the permission to remove a voter if his vote is not necessary to conquer the district under borda
    def borda_ask(self, voter):
        permission = True
        if self.conquer and voter.get(1) == 'a' and (self.get_borda('a') <= self.get_borda('b') or self.get_borda('a') <= self.get_borda('c')):
            permission = False
        if self.conquer and voter.get(3) != 'a' and voter.get(3) == self.borda_first() and (self.get_borda('a') <= self.get_borda('b') or self.get_borda('a') <= self.get_borda('c')):
            permission = False
        return permission

    # checks if the district has been conquered under borda
    def borda_victory(self):
        victory = False
        if self.get_borda('a') > self.get_borda('b') and self.get_borda('a') > self.get_borda('c'):
            victory = True
        return victory

    # runs the borda rule restricted to the voters belonging to the district
    def get_borda(self, alternative):
        return rule_borda(self.voters)[alternative]

    # returns the copeland winner of the district
    def cope_first(self):
        copeland = rule_copeland(self.voters)
        alt_scores = {}
        alt_scores['a'] = copeland['ab'] + copeland['ac']
        alt_scores['b'] = copeland['ba'] + copeland['bc']
        alt_scores['c'] = copeland['ca'] + copeland['cb']
        return max(alt_scores.iteritems(), key=operator.itemgetter(1))[0]

    # gives the permission to remove a voter if his vote is not necessary to conquer the district under copeland
    def cope_ask(self, voter):
        permission = True
        if self.conquer and voter.get(1) == 'a' and (self.get_cope('ab') <= 0 or self.get_cope('ac') <= 0):
            permission = False
        if self.conquer and voter.get(3) != 'a' and voter.get(3) == self.cope_first() and (self.get_cope('ab') <= 0 or self.get_cope('ac') <= 0):
            permission = False
        return permission

    # checks if the district has been conquered under copeland
    def cope_victory(self):
        victory = False
        if self.get_cope('ab') > 0 and self.get_cope('ac') > 0:
            victory = True
        return victory

    # runs the copeland rule restricted to the voters belonging to the district
    def get_cope(self, alternatives):
        return rule_copeland(self.voters)[alternatives]


class Grid:
    def __init__(self, size, districts, percentages, hot_on, prop_lim):
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

    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process for plurality
    def plur_gerry(self):
        self.rule = 'plurality'
        plur_conquer = self.plur_conquer()
        scores_in_dists = np.array([dist.get_plurality('a') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        # if plur_conquer / float(self.districts) > 0.5:
        #     plur_conquer -= 1
        for i in range(min(plur_conquer, self.districts)):
            self.dist_list[ranks[i]].set_conquer(True)
        first_dist = random.choice(self.dist_list)
        found_neighbour, new_district, old_district, last_voter = self.plur_step(first_dist)
        max_iterations = 300
        iteration = 0
        while found_neighbour and (self.plur_victory(plur_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.plur_step(new_district, old_district)
            iteration += 1
            # one district gets one too many voters and another gets one less correction - work in progress
            # if (found_neighbour == False):
            #     self.dist_list[old_district].add_voter(save_last_voter)
            #     self.dist_list[save_last_voter.get_district()].remove_voter(save_last_voter)
            # elif (self.plur_victory(plur_conquer)) or (iteration >= max_iterations):
            #     new_district.add_voter(last_voter)
            #     self.dist_list[old_district].remove_voter(last_voter)
            # save_last_voter = last_voter

    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if one of the voters can be acquired
    def plur_step(self, dist, last_dist=-1):
        neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.get_district() != last_dist]
        found_neighbour = False
        neighbours_by_type = []
        if dist.get_conquer():
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != dist.plur_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != dist.plur_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == dist.plur_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == dist.plur_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
        else:
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and self.dist_list[neighbour.get_district()].plur_first() == neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and self.dist_list[neighbour.get_district()].plur_first() != neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.dist_list[neighbour.get_district()].get_conquer()])
        all_neighbours = []
        for neighbour_group in neighbours_by_type:
            all_neighbours += neighbour_group
        for neighbour in all_neighbours:
            neighbour_dist = self.dist_list[neighbour.get_district()]
            if neighbour_dist.plur_ask(neighbour) and self.ask(neighbour):
                found_neighbour = True
                dist.add_voter(neighbour)
                neighbour_dist.remove_voter(neighbour)
                break;
        return found_neighbour, neighbour_dist, dist.get_number(), neighbour

    # returns if the number of conquered district is maximal under plurality
    def plur_victory(self, plur_conquer):
        victory = False
        victories = [dist for dist in self.dist_list if dist.plur_victory()]
        if len(victories) == plur_conquer:
            victory = True
        return victory

    # returns the maximal number of districts that can be conquered under plurality with the current preference distribution
    def plur_conquer(self):
        points = rule_plurality(self.profile())['a']
        points_to_win_a_dist = int(((self.size * self.size) / self.districts) / 3) + 1
        plur_conquer = int(points / points_to_win_a_dist)
        return plur_conquer

    # prints the results of the plurality run
    def plur_results(self):
        conquered_districts = [dist for dist in self.dist_list if dist.plur_victory()]
        dist_percentage = round(len(conquered_districts) / float(self.districts), 2)
        percentage = round(rule_plurality(self.profile())['a'] / float(self.size * self.size), 2)
        plur_conquer = self.plur_conquer()
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.districts) 
                    + ' when ' + str(plur_conquer) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process for borda
    def borda_gerry(self):
        self.rule = 'borda'
        borda_conquer = self.borda_conquer()
        scores_in_dists = np.array([dist.get_borda('a') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        # if borda_conquer / float(self.districts) > 0.5:
        #     borda_conquer -= 1
        for i in range(min(borda_conquer, self.districts)):
            self.dist_list[ranks[i]].set_conquer(True)
        first_dist = random.choice(self.dist_list)
        found_neighbour, new_district, old_district, last_voter = self.borda_step(first_dist)
        max_iterations = 300
        iteration = 0
        while found_neighbour and (self.borda_victory(borda_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.borda_step(new_district, old_district)
            iteration += 1

    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if any of the voters can be exchanged
    def borda_step(self, dist, last_dist=-1):
        neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.get_district() != last_dist]
        found_neighbour = False
        neighbours_by_type = []
        if dist.get_conquer():
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) != dist.borda_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) != dist.borda_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) == dist.borda_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) != dist.borda_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) == dist.borda_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) != dist.borda_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) == dist.borda_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) == dist.borda_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
        else:
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and self.dist_list[neighbour.get_district()].borda_first() == neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and self.dist_list[neighbour.get_district()].borda_first() != neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and self.dist_list[neighbour.get_district()].borda_first() == neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and self.dist_list[neighbour.get_district()].borda_first() != neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and self.dist_list[neighbour.get_district()].borda_first() == neighbour.get(2)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and self.dist_list[neighbour.get_district()].borda_first() != neighbour.get(2)
                and self.dist_list[neighbour.get_district()].get_conquer()])
        all_neighbours = []
        for neighbour_group in neighbours_by_type:
            all_neighbours += neighbour_group
        for neighbour in all_neighbours:
            neighbour_dist = self.dist_list[neighbour.get_district()]
            if neighbour_dist.borda_ask(neighbour) and self.ask(neighbour):
                found_neighbour = True
                dist.add_voter(neighbour)
                neighbour_dist.remove_voter(neighbour)
                break;
        return found_neighbour, neighbour_dist, dist.get_number(), neighbour

    # returns if the number of conquered district is maximal under borda
    def borda_victory(self, borda_conquer):
        victory = False
        victories = [dist for dist in self.dist_list if dist.borda_victory()]
        if len(victories) == borda_conquer:
            victory = True
        return victory

    # returns the maximal number of districts that can be conquered under borda with the current preference distribution
    def borda_conquer(self):
        points = rule_borda(self.profile())['a']
        points_to_win_a_dist = int(((self.size * self.size * 3) / self.districts) / 3) + 1
        borda_conquer = int(points / points_to_win_a_dist)
        return borda_conquer

    # prints the results of the borda run
    def borda_results(self):
        conquered_districts = [dist for dist in self.dist_list if dist.borda_victory()]
        dist_percentage = round(len(conquered_districts) / float(self.districts), 2)
        percentage = round(rule_borda(self.profile())['a'] / float(self.size * self.size * 3), 2)
        borda_conquer = self.borda_conquer()
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.districts) 
                    + ' when ' + str(borda_conquer) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process for copeland
    def cope_gerry(self):
        self.rule = 'copeland'
        cope_conquer = self.cope_conquer()
        scores_in_dists = np.array([dist.get_cope('ab') + dist.get_cope('ac') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        # if cope_conquer / float(self.districts) > 0.5:
        #     cope_conquer -= 1
        for i in range(min(cope_conquer, self.districts)):
            self.dist_list[ranks[i]].set_conquer(True)
        first_dist = random.choice(self.dist_list)
        found_neighbour, new_district, old_district, last_voter = self.cope_step(first_dist)
        max_iterations = 300
        iteration = 0
        while found_neighbour and (self.cope_victory(cope_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.cope_step(new_district, old_district)
            iteration += 1

    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if any of the voters can be exchanged
    def cope_step(self, dist, last_dist=-1):
        neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.get_district() != last_dist]
        found_neighbour = False
        neighbours_by_type = []
        if dist.get_conquer():
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) != dist.cope_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) != dist.cope_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) == dist.cope_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) != dist.cope_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) == dist.cope_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) != dist.cope_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) == dist.cope_first()
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) == dist.cope_first()
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
        else:
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and self.dist_list[neighbour.get_district()].cope_first() == neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and self.dist_list[neighbour.get_district()].cope_first() != neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and self.dist_list[neighbour.get_district()].cope_first() == neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and self.dist_list[neighbour.get_district()].cope_first() != neighbour.get(1)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and self.dist_list[neighbour.get_district()].cope_first() == neighbour.get(2)
                and self.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and self.dist_list[neighbour.get_district()].cope_first() != neighbour.get(2)
                and self.dist_list[neighbour.get_district()].get_conquer()])
        all_neighbours = []
        for neighbour_group in neighbours_by_type:
            all_neighbours += neighbour_group
        for neighbour in all_neighbours:
            neighbour_dist = self.dist_list[neighbour.get_district()]
            if neighbour_dist.cope_ask(neighbour) and self.ask(neighbour):
                found_neighbour = True
                dist.add_voter(neighbour)
                neighbour_dist.remove_voter(neighbour)
                break;
        return found_neighbour, neighbour_dist, dist.get_number(), neighbour

    # returns if the number of conquered district is maximal under copeland
    def cope_victory(self, cope_conquer):
        victory = False
        victories = [dist for dist in self.dist_list if dist.cope_victory()]
        if len(victories) == cope_conquer:
            victory = True
        return victory

    # returns the maximal number of districts that can be conquered under copeland with the current preference distribution
    def cope_conquer(self):
        points = rule_borda(self.profile())['a']
        points_to_win_a_dist = int(((self.size * self.size * 3) / self.districts) / 3) + 1
        borda_conquer = int(points / points_to_win_a_dist)
        return borda_conquer

    # prints the results of the copeland run
    def cope_results(self):
        conquered_districts = [dist for dist in self.dist_list if dist.cope_victory()]
        dist_percentage = round(len(conquered_districts) / float(self.districts), 2)
        percentage = round(rule_borda(self.profile())['a'] / float(self.size * self.size * 3), 2)
        cope_conquer = self.cope_conquer()
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.districts) 
                    + ' when ' + str(cope_conquer) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

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
        if len(inner_voters) < int(len(voters) / 4):
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
    def print_map(self):
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
        plt.show()

# calculates plurality on the entire profile
def rule_plurality(profile):
    score = {}
    score['a'] = score['b'] = score['c'] = 0
    for voter in profile:
        score[voter.get(1)] += 1
    return score

# calculates borda on the entire profile
def rule_borda(profile):
    score = {}
    score['a'] = score['b'] = score['c'] = 0
    for voter in profile:
        score[voter.get(1)] += 2
        score[voter.get(2)] += 1
    return score

# calculates borda on the entire profile
def rule_copeland(profile):
    score = {}
    score['ab'] = score['ac'] = score['ba'] = score['bc'] = score['ca'] = score['cb'] = 0
    for voter in profile:
        score[voter.get(1) + voter.get(2)] += 1
        score[voter.get(2) + voter.get(1)] -= 1
        score[voter.get(1) + voter.get(3)] += 1
        score[voter.get(3) + voter.get(1)] -= 1
        score[voter.get(2) + voter.get(3)] += 1
        score[voter.get(3) + voter.get(2)] -= 1
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

def run_copeland(grid):
    print('copeland score:')
    print rule_copeland(grid.profile())
    grid.cope_gerry()
    grid.cope_results()

def main():
    size = 12
    districts = 6
    # percentages=[30,35,35]
    percentages=[33,33,33]
    hotspots_on = False
    proportion_limit = False
    grid = Grid(size, districts, percentages, hotspots_on, proportion_limit)
    if hotspots_on:
        print('hotspots:')
        print grid.hotspots

    # run_plurality(grid)
    # run_borda(grid)
    run_copeland(grid)

    # for dist in grid.dist_list:
    #     print dist.get_size()

    grid.print_map()

if __name__ == "__main__":
    main()


# ___BIN___

    # ___OLD VICTORY___
    # gives the permission to remove a voter if his vote is not necessary to conquer the district under plurality
    # def plur_ask(self, voter):
    #     permission = True
    #     min_voters = int(self.get_size() / 3) + 1
    #     if self.conquer and voter.get(1) == 'a' and self.get_plurality('a') <= min_voters:
    #         permission = False
    #     return permission
    # # checks if the district has been conquered under plurality
    # def plur_victory(self):
    #     victory = False
    #     min_voters = int(self.get_size() / 3) + 1
    #     if self.get_plurality('a') >= min_voters:
    #         victory = True
    #     return victory
    # # gives the permission to remove a voter if his vote is not necessary to conquer the district under borda
    # def borda_ask(self, voter):
    #     permission = True
    #     min_points = int(self.get_size() * 3 / 3) + 1
    #     if self.conquer and voter.get(3) != 'a' and self.get_borda('a') <= min_points:
    #         permission = False
    #     return permission
    # # checks if the district has been conquered under borda
    # def borda_victory(self):
    #     victory = False
    #     min_points = int(self.get_size() * 3 / 3) + 1
    #     if self.get_borda('a') >= min_points:
    #         victory = True
    #     return victory
    # ___OLD ASK___
    # def ask(self, x, y):
    #     voter = self.grid[x][y]
    #     dist = voter.get_district()
    #     left = self.grid[(x-1) % self.size][y]
    #     right = self.grid[(x+1) % self.size][y]
    #     up = self.grid[x][(y-1) % self.size]
    #     down = self.grid[x][(y+1) % self.size]
    #     permission = False
    #     if self.check_voter(dist, voter) and self.check_voter(dist, left) and self.check_voter(dist, right) and self.check_voter(dist, up) and self.check_voter(dist, down):
    #         permission = True
    #     return permission
    # def check_voter(self, district, voter):
    #     x = voter.get_x()
    #     y = voter.get_y()
    #     center = self.grid[x][y].get_district()
    #     left = self.grid[(x-1) % self.size][y].get_district()
    #     right = self.grid[(x+1) % self.size][y].get_district()
    #     up = self.grid[x][(y-1) % self.size].get_district()
    #     down = self.grid[x][(y+1) % self.size].get_district()
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
    #         x = voters[i].get_x()
    #         y = voters[i].get_y()
    #         self.grid[x][y].set_district(i + 1)
    #         num_assigned += 1
    #     index = num_assigned
    #     while (num_assigned < self.size * self.size):
    #         x = voters[index].get_x()
    #         y = voters[index].get_y()
    #         # print("Assigned: " + str(num_assigned))
    #         if self.grid[x][y].get_district() == 0:
    #             dis = self.get_district_from_neighbors(x, y)
    #             if dis != 0:
    #                 self.grid[x][y].set_district(dis)
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
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].get_district() != 0:
    #         return self.grid[x2][y2].get_district()
    #     option = options[1]
    #     x2 = x + option[0]
    #     y2 = y + option[1]
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].get_district() != 0:
    #         return self.grid[x2][y2].get_district()
    #     option = options[2]
    #     x2 = x + option[0]
    #     y2 = y + option[1]
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].get_district() != 0:
    #         return self.grid[x2][y2].get_district()
    #     option = options[3]
    #     x2 = x + option[0]
    #     y2 = y + option[1]
    #     if x2 >= 0 and y2 >= 0 and x2 < self.size and y2 < self.size and self.grid[x2][y2].get_district() != 0:
    #         return self.grid[x2][y2].get_district()
    #     return 0