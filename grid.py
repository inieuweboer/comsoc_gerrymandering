import random
import math

import numpy as np
import matplotlib.pyplot as plt

from district import *
from rules import *
from voter import *


class Grid:
    def __init__(self, size, districts, percentages, hot_on, prop_lim, hotspots=[]):
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
        if len(hotspots) > 0:
            self.hotspots = hotspots
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

    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process for borda
    def borda_gerry(self):
        self.rule = 'borda'
        borda_conquer = self.borda_conquer()
        scores_in_dists = np.array([dist.get_borda('a') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(min(borda_conquer, self.districts)):
            self.dist_list[ranks[i]].set_conquer(True)
        first_dist = random.choice(self.dist_list)
        found_neighbour, new_district, old_district, last_voter = self.borda_step(first_dist)
        max_iterations = 300
        iteration = 0
        while found_neighbour and (self.borda_victory(borda_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.borda_step(new_district, old_district)
            iteration += 1
            if (iteration % 100) == 0 and (self.borda_victory(borda_conquer) == False):
                print "decreased the number of to-be-conquered districts"
                borda_conquer -= 1
                self.borda_decrease(borda_conquer)
            if (found_neighbour == False):
                print "no neighbour found"

    # decreases by one the number of districts to be conquered if the algorithm can't conquer all of those possible
    def borda_decrease(self, borda_conquer):
        scores_in_dists = np.array([dist.get_borda('a') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(self.districts):
            self.dist_list[i].set_conquer(False)
        for i in range(borda_conquer):
            self.dist_list[ranks[i]].set_conquer(True)

    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if any of the voters can be exchanged
    def borda_step(self, dist, last_dist=-1):
        # the neighbours considered must not belong to the previous active district that took a voter from the current one
        neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.get_district() != last_dist]
        found_neighbour = False
        neighbours_by_type = []
        # the following division in groups is based on three conditions. 1) The position of alternative 'a' in the neighbour's preference order. 2) The neighbour's district being to-be-conquered or not. 3) the neighbour's first preference is not a and is the one that's winning in the acquiring district
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
            # ask permission to acquire the neighbour both to her district and to the grid
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
        borda_conquer = min(int(points / points_to_win_a_dist), self.districts)
        return borda_conquer

    # prints the results of the borda run
    def borda_results(self):
        conquered_districts = [dist for dist in self.dist_list if dist.borda_victory()]
        dist_percentage = round(len(conquered_districts) / float(self.districts), 2)
        percentage = round(rule_borda(self.profile())['a'] / float(self.size * self.size * 2), 2)
        borda_conquer = self.borda_conquer()
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.districts) 
                    + ' when ' + str(borda_conquer) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

        return (percentage, dist_percentage)

    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process for copeland
    def cope_gerry(self):
        self.rule = 'copeland'
        cope_conquer = self.cope_conquer()
        scores_in_dists = np.array([dist.get_cope('ab') + dist.get_cope('ac') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(min(cope_conquer, self.districts)):
            self.dist_list[ranks[i]].set_conquer(True)
        first_dist = random.choice(self.dist_list)
        found_neighbour, new_district, old_district, last_voter = self.cope_step(first_dist)
        max_iterations = 300
        iteration = 0
        while found_neighbour and (self.cope_victory(cope_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.cope_step(new_district, old_district)
            iteration += 1
            if (iteration % 100) == 0 and (self.cope_victory(cope_conquer) == False):
                print "decreased the number of to-be-conquered districts"
                cope_conquer -= 1
                self.cope_decrease(cope_conquer)
            if (found_neighbour == False):
                print "no neighbour found"

    # decreases by one the number of districts to be conquered if the algorithm can't conquer all of those possible
    def cope_decrease(self, cope_conquer):
        scores_in_dists = np.array([dist.get_cope('ab') + dist.get_cope('ac') for dist in self.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(self.districts):
            self.dist_list[i].set_conquer(False)
        for i in range(cope_conquer):
            self.dist_list[ranks[i]].set_conquer(True)

    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if any of the voters can be exchanged
    def cope_step(self, dist, last_dist=-1):
        # the neighbours considered must not belong to the previous active district that took a voter from the current one
        neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.get_district() != last_dist]
        found_neighbour = False
        neighbours_by_type = []
        # the following division in groups is based on three conditions. 1) The position of alternative 'a' in the neighbour's preference order. 2) The neighbour's district being to-be-conquered or not. 3) the neighbour's first preference is not a and is the one that's winning in the acquiring district
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
            # ask permission to acquire the neighbour both to her district and to the grid
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
        cope_conquer = min(int(points / points_to_win_a_dist), self.districts)
        return cope_conquer

    # prints the results of the copeland run
    def cope_results(self):
        conquered_districts = [dist for dist in self.dist_list if dist.cope_victory()]
        dist_percentage = round(len(conquered_districts) / float(self.districts), 2)
        percentage = round(rule_borda(self.profile())['a'] / float(self.size * self.size * 2), 2)
        cope_conquer = self.cope_conquer()
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.districts) 
                    + ' when ' + str(cope_conquer) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

        return (percentage, dist_percentage)

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
        if len(inner_voters) < int(len(voters) / 3):
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
    def prepare_map(self):
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
                # if self.dist_list[self.grid[x][y].get_district()].get_conquer():
                #     color = 'green'
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

    def set_districts(self, districts):
        self.dist_list = districts
        for dist in self.dist_list:
            voters = dist.get_voter()[:]
            for voter in voters:
                dist.add_voter(self.grid[voter.get_x()][voter.get_y()])
                dist.remove_voter(voter)

    def set_rule(self, rule):
        self.rule = rule
