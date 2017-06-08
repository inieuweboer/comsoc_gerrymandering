import random
import operator

import numpy as np

class Rule:
    def __init__(self, grid):
        self.text = 'Empty'
        self.grid = grid

    def run_gerry(self):
        print(self.text + ' score:')
        print self.calc_score(self.grid.profile())
        self.gerry() # returns districts

        return self.results()

    # returns the maximal number of districts that can be conquered under plurality with the current preference distribution
    def can_conquer(self):
        points = self.calc_score(self.grid.profile())['a']
        sq = self.grid.size * self.grid.size
        points_to_win_a_dist = int((sq / self.grid.districts) / 3) + 1
        plur_conquer = min(int(points / points_to_win_a_dist), self.grid.districts)
        return plur_conquer

    @staticmethod
    def calc_score(profile):
        score = {}
        score['a'] = score['b'] = score['c'] = 0
        return score

    # decreases by one the number of districts to be conquered if the algorithm can't conquer all of those possible
    def decrease(self, n_conquerable):
        scores_in_dists = np.array([self.calc_score_dist(dist, 'a') for dist in self.grid.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(self.grid.districts):
            self.grid.dist_list[i].set_conquer(False)
        for i in range(n_conquerable):
            self.grid.dist_list[ranks[i]].set_conquer(True)

    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process
    def gerry(self):
        conquer = self.can_conquer()
        scores_in_dists = np.array([self.calc_score_dist(dist, 'a') for dist in self.grid.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(conquer):
            self.grid.dist_list[ranks[i]].set_conquer(True)
        first_dist = random.randint(0, len(self.grid.dist_list) - 1)
        found_neighbour, new_district, old_district, last_voter = self.step(first_dist)
        max_iterations = 300
        iteration = 0
        while found_neighbour and (self.victory(conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.step(new_district, old_district)
            iteration += 1
            if (iteration % 100) == 0 and (self.victory(conquer) == False):
                print "decreased the number of to-be-conquered districts"
                conquer -= 1
                self.decrease(conquer)
            if (found_neighbour == False):
                print "no neighbour found"

    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if one of the voters can be acquired
    def step(self, dist_no, last_dist_no=-1):
        dist = self.grid.dist_list[dist_no]

        # the neighbours considered must not belong to the previous active district that took a voter from the current one
        found_neighbour = False

        neighbours = [neighbour for neighbour in self.grid.dist_neighbours(dist) if neighbour.get_district() != last_dist_no]

        neighbours_by_type = self.get_neighbours_by_type(neighbours, dist_no, last_dist_no)

        all_neighbours = []
        for neighbour_group in neighbours_by_type:
            all_neighbours += neighbour_group
        for neighbour in all_neighbours:
            neighbour_dist_no = neighbour.get_district()
            neighbour_dist = self.grid.dist_list[neighbour_dist_no]
            # ask permission to acquire the neighbour both to her district and to the grid
            if self.ask_dist(neighbour_dist, neighbour) and self.grid.ask(neighbour):
                found_neighbour = True
                dist.add_voter(neighbour)
                neighbour_dist.remove_voter(neighbour)
                break;

        return found_neighbour, neighbour_dist_no, dist.get_number(), neighbour

    def get_neighbours_by_type(self, neighbours, dist_no, last_dist_no):
        dist = self.grid.dist_list[dist_no]
        neighbours_by_type = []

        # ...

        return neighbours_by_type

    # prints the results of the run
    def results(self):
        conquered_districts = [dist for dist in self.grid.dist_list if self.victory_dist(dist)]
        dist_percentage = round(len(conquered_districts) / float(self.grid.districts), 2)
        sq = self.grid.size * self.grid.size
        percentage = round(self.calc_score(self.grid.profile())['a'] / float(sq), 2)
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(self.grid.districts) 
                    + ' when ' + str(self.can_conquer()) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

        return (percentage, dist_percentage)

    # returns if the number of conquered district is maximal under the rule
    def victory(self, n_conquerable):
        victory = False
        victories = [dist for dist in self.grid.dist_list if self.victory_dist(dist)]
        if len(victories) == n_conquerable:
            victory = True
        return victory

    # District methods

    # runs the plurality rule restricted to the voters belonging to the district
    def calc_score_dist(self, dist, alternative):
        return self.calc_score(dist.voters)[alternative]

    # returns the winner of the district
    def get_max_score_dist(self, dist):
        score_vect = self.calc_score(dist.voters)
        return max(score_vect.iteritems(), key=operator.itemgetter(1))[0]

    # checks if the district has been conquered
    def victory_dist(self, dist):
        victory = False
        if self.calc_score_dist(dist, 'a') > self.calc_score_dist(dist, 'b') and \
            self.calc_score_dist(dist, 'a') > self.calc_score_dist(dist, 'c'):
            victory = True
        return victory

    # Help function
    def to_be_conquered(self, neighbour):
        return self.grid.dist_list[neighbour.get_district()].get_conquer()




class Plurality(Rule):
    def __init__(self, grid):
        self.text = 'Plurality'
        self.grid = grid

    @staticmethod
    def calc_score(profile):
        score = {}
        score['a'] = score['b'] = score['c'] = 0
        for voter in profile:
            score[voter.get(1)] += 1
        return score

    def get_neighbours_by_type(self, neighbours, dist_no, last_dist_no):
        dist = self.grid.dist_list[dist_no]
        neighbours_by_type = []
        # the following division in groups is based on three conditions. 1) The preference of the neighbour being 'a'. 2) The neighbour's district being to-be-conquered or not. 3) the neighbour's first preference is not a and is the one that's winning in the acquiring district
        if dist.get_conquer():
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != self.get_max_score_dist(dist)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != self.get_max_score_dist(dist)
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == self.get_max_score_dist(dist)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == self.get_max_score_dist(dist)
                and not self.to_be_conquered(neighbour)])
        else:
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) == neighbour.get(1)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) != neighbour.get(1)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.to_be_conquered(neighbour)])

        return neighbours_by_type

    # District methods

    # gives the permission to remove a voter if his vote is not necessary to conquer the district under plurality
    def ask_dist(self, dist, voter):
        permission = True
        if dist.conquer and voter.get(1) == 'a' and (self.calc_score_dist(dist, 'a') <= (self.calc_score_dist(dist, 'b')+1) or self.calc_score_dist(dist, 'a') <= (self.calc_score_dist(dist, 'c')+1)):
            permission = False
        return permission



class Borda(Rule):

    def __init__(self, grid):
        self.text = 'Borda'
        self.grid = grid

    # calculates borda on the entire profile
    @staticmethod
    def calc_score(profile):
        score = {}
        score['a'] = score['b'] = score['c'] = 0
        for voter in profile:
            score[voter.get(1)] += 2
            score[voter.get(2)] += 1
        return score

    def get_neighbours_by_type(self, neighbours, dist_no, last_dist_no):
        dist = self.grid.dist_list[dist_no]
        neighbours_by_type = []
        # the following division in groups is based on three conditions. 1) The position of alternative 'a' in the neighbour's preference order. 2) The neighbour's district being to-be-conquered or not. 3) the neighbour's first preference is not a and is the one that's winning in the acquiring district
        if dist.get_conquer():
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) != self.get_max_score_dist(dist)
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) != self.get_max_score_dist(dist)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) == self.get_max_score_dist(dist)
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) != self.get_max_score_dist(dist)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a' and neighbour.get(1) == self.get_max_score_dist(dist)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) != self.get_max_score_dist(dist)
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) == self.get_max_score_dist(dist)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a' and neighbour.get(1) == self.get_max_score_dist(dist)
                and not self.to_be_conquered(neighbour)])
        else:
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) == neighbour.get(1)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) != neighbour.get(1)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(3) == 'a'
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and not self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) == neighbour.get(1)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(2) == 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) != neighbour.get(1)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) == neighbour.get(2)
                and self.to_be_conquered(neighbour)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a'
                and self.get_max_score_dist(self.grid.dist_list[neighbour.get_district()]) != neighbour.get(2)
                and self.to_be_conquered(neighbour)])

        return neighbours_by_type

    # gives the permission to remove a voter if his vote is not necessary to conquer the district under borda
    def ask_dist(self, dist, voter):
        permission = True
        if dist.conquer and voter.get(1) == 'a' and (self.calc_score_dist(dist, 'a') <= (self.calc_score_dist(dist, 'b')+2) or self.calc_score_dist(dist, 'a') <= (self.calc_score_dist(dist, 'c')+2)):
            permission = False
        # this second condition ensures that if the voter ranks the non-a alternative that is winning the district last he does not get removed from the district
        if dist.conquer and voter.get(3) != 'a' and voter.get(3) == self.get_max_score_dist(dist) and (self.calc_score_dist(dist, 'a') <= (self.calc_score_dist(dist, 'b')+2) or self.calc_score_dist(dist, 'a') <= (self.calc_score_dist(dist, 'c')+2)):
            permission = False
        return permission




def run_copeland(grid):
    print('copeland score:')
    print rule_copeland(grid.profile())
    grid.cope_gerry()
    return grid.cope_results()



# calculates copeland on the entire profile
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
