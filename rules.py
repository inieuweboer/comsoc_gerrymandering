import random

import numpy as np

class Rule:
    def __init__(self):
        self.text = 'Empty'

    def run_gerry(self, grid):
        print(self.text + ' score:')
        print self.calculate_score(grid.profile())
        self.gerry(grid) # returns districts

        return self.results(grid)

    @staticmethod
    def calculate_score(profile):
        score = {}
        score['a'] = score['b'] = score['c'] = 0
        return score

    def gerry(self, grid):
        pass

    def results(self, grid):
        pass



class Plurality(Rule):
    def __init__(self):
        self.text = 'Plurality'

    # returns the maximal number of districts that can be conquered under plurality with the current preference distribution
    def can_conquer(self, grid):
        points = self.calculate_score(grid.profile())['a']
        sq = grid.size * grid.size
        points_to_win_a_dist = int((sq / grid.districts) / 3) + 1
        plur_conquer = min(int(points / points_to_win_a_dist), grid.districts)
        return plur_conquer

    @staticmethod
    def calculate_score(profile):
        score = {}
        score['a'] = score['b'] = score['c'] = 0
        for voter in profile:
            score[voter.get(1)] += 1
        return score

    def decrease(self, grid, plur_conquer):
        scores_in_dists = np.array([dist.get_plurality('a') for dist in grid.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(grid.districts):
            grid.dist_list[i].set_conquer(False)
        for i in range(plur_conquer):
            grid.dist_list[ranks[i]].set_conquer(True)

    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process for plurality
    def gerry(self, grid):
        plur_conquer = self.can_conquer(grid)
        scores_in_dists = np.array([dist.get_plurality('a') for dist in grid.dist_list])
        ranks = scores_in_dists.argsort()[::-1]
        for i in range(plur_conquer):
            grid.dist_list[ranks[i]].set_conquer(True)
        first_dist = random.randint(0, len(grid.dist_list) - 1)
        found_neighbour, new_district, old_district, last_voter = self.step(grid, first_dist)
        max_iterations = 300
        iteration = 0
        while found_neighbour and (self.victory(grid, plur_conquer) == False) and (iteration < max_iterations):
            found_neighbour, new_district, old_district, last_voter = self.step(grid, new_district, old_district)
            iteration += 1
            if (iteration % 100) == 0 and (self.victory(grid, plur_conquer) == False):
                print "decreased the number of to-be-conquered districts"
                plur_conquer -= 1
                self.decrease(grid, plur_conquer)
            if (found_neighbour == False):
                print "no neighbour found"

    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if one of the voters can be acquired
    def step(self, grid, dist_no, last_dist_no=-1):
        dist = grid.dist_list[dist_no]

        # the neighbours considered must not belong to the previous active district that took a voter from the current one
        neighbours = [neighbour for neighbour in grid.dist_neighbours(dist) if neighbour.get_district() != last_dist_no]
        found_neighbour = False
        neighbours_by_type = []
        # the following division in groups is based on three conditions. 1) The preference of the neighbour being 'a'. 2) The neighbour's district being to-be-conquered or not. 3) the neighbour's first preference is not a and is the one that's winning in the acquiring district
        if dist.get_conquer():
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (grid.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and grid.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != dist.plur_first()
                and grid.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != dist.plur_first()
                and (grid.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == dist.plur_first()
                and grid.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == dist.plur_first()
                and (grid.dist_list[neighbour.get_district()].get_conquer() == False)])
        else:
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and grid.dist_list[neighbour.get_district()].plur_first() == neighbour.get(1)
                and grid.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and grid.dist_list[neighbour.get_district()].plur_first() != neighbour.get(1)
                and grid.dist_list[neighbour.get_district()].get_conquer()])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
                and (grid.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and (grid.dist_list[neighbour.get_district()].get_conquer() == False)])
            neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
                and grid.dist_list[neighbour.get_district()].get_conquer()])
        all_neighbours = []
        for neighbour_group in neighbours_by_type:
            all_neighbours += neighbour_group
        for neighbour in all_neighbours:
            neighbour_dist_no = neighbour.get_district()
            neighbour_dist = grid.dist_list[neighbour_dist_no]
            # ask permission to acquire the neighbour both to her district and to the grid
            if neighbour_dist.plur_ask(neighbour) and grid.ask(neighbour):
                found_neighbour = True
                dist.add_voter(neighbour)
                neighbour_dist.remove_voter(neighbour)
                break;

        return found_neighbour, neighbour_dist_no, dist.get_number(), neighbour

    # prints the results of the plurality run
    def results(self, grid):
        conquered_districts = [dist for dist in grid.dist_list if dist.plur_victory()]
        dist_percentage = round(len(conquered_districts) / float(grid.districts), 2)
        sq = grid.size * grid.size
        percentage = round(self.calculate_score(grid.profile())['a'] / float(sq), 2)
        print('the gerrimanderer has conquered ' + str(len(conquered_districts)) + ' districts out of ' + str(grid.districts) 
                    + ' when ' + str(self.can_conquer(grid)) + ' were possible')
        print('the gerrimanderer has achieved a percentage of ' + str(dist_percentage) + ' instead of ' + str(percentage))

        return (percentage, dist_percentage)

    # returns if the number of conquered district is maximal under plurality
    def victory(self, grid, plur_conquer):
        victory = False
        victories = [dist for dist in grid.dist_list if dist.plur_victory()]
        if len(victories) == plur_conquer:
            victory = True
        return victory


#class Borda(Rule):


def run_borda(grid):
    print('borda score:')
    print rule_borda(grid.profile())
    grid.borda_gerry()
    return grid.borda_results()

def run_copeland(grid):
    print('copeland score:')
    print rule_copeland(grid.profile())
    grid.cope_gerry()
    return grid.cope_results()



# calculates borda on the entire profile
def rule_borda(profile):
    score = {}
    score['a'] = score['b'] = score['c'] = 0
    for voter in profile:
        score[voter.get(1)] += 2
        score[voter.get(2)] += 1
    return score

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
