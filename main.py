import sys, os
import matplotlib.pyplot as plt
import collections

from grid import *
from rules import *



def run_plurality(grid):
    print('plurality score:')
    print rule_plurality(grid.profile())
    districts = grid.plur_gerry()
    return grid.plur_results()

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

def plur_again(grid):
    districts = grid.dist_list[:]
    new_grid = Grid(12, 6, [33,33,33], True, False, grid.hotspots)
    new_grid.set_districts(districts)
    new_grid.set_rule('plurality')
    print('plurality score:')
    print rule_plurality(new_grid.profile())
    new_grid.plur_results()
    return new_grid


def main():
    show = True

    size = 12
    districts = 6
    percentages = [33,33,33]
    hotspot_on = True
    proportion_limit = False

    # ___ITERATED EXPERIMENTS___

    for i in range(5):
        grid = Grid(size, districts, percentages, hotspot_on, proportion_limit)
        run_plurality(grid)
        # run_borda(grid)
        # run_copeland(grid)

    # ___SINGLE EXPERIMENT___

    # # Create the grid
    # grid = Grid(size, districts, percentages, hotspot_on, proportion_limit)
    # if hotspot_on:
    #     print('hotspots:')
    #     print grid.hotspots

    # # Run the algorithm
    # run_plurality(grid)
    # # run_borda(grid)
    # # run_copeland(grid)

    # grid.prepare_map()

    # # Run again with same districts and same hotspots
    # # new_grid = plur_again(grid)
    # # new_grid.prepare_map()

    # if show:
    #     plt.show()
    # else:
    #     plt.savefig(destination)


    # ___MULTIPLE EXPERIMENTS___

    # percentages = range(1, 101)
    # districts = 6
    # runs = 5

    # results_hotspots = {}
    # results_hotspots_appeared = {x:0 for x in range(101)}
    # results_no_hotspots = {}
    # results_no_hotspots_appeared = {x:0 for x in range(101)}

    # # -------------------------------------------------------------------------
    # #                               PLURALITY
    # # -------------------------------------------------------------------------

    # for run in range(runs):
    #     for percentage in percentages:

    #         print("Run: " + str(run + 1) + "/" + str(runs) + ", percentage: " + str(percentage))

    #         remainder = 100 - percentage
    #         p_party_b = math.floor(remainder / 2.0)
    #         p_party_c = remainder - p_party_b

    #         perc = [percentage, p_party_b, p_party_c]

    #         grid = Grid(12, districts, perc, True, True)

    #         x = run_plurality(grid)

    #         round_true_perc = int(round(x[0] * 100))
    #         round_gerry_perc = int(round(x[1] * 100)) 
    #         avg_gerry_perc = round_gerry_perc
    #         if results_hotspots_appeared[round_true_perc] > 0:
    #             appears = results_hotspots_appeared[round_true_perc]
    #             avg_gerry_perc = ((results_hotspots[round_true_perc] * appears) + round_gerry_perc) / float(appears + 1)

    #         results_hotspots[round_true_perc] = avg_gerry_perc
    #         results_hotspots_appeared[round_true_perc] += 1

    #         grid = Grid(12, districts, perc, False, True)

    #         x = run_plurality(grid)

    #         round_true_perc = int(round(x[0] * 100))
    #         round_gerry_perc = int(round(x[1] * 100)) 
    #         avg_gerry_perc = round_gerry_perc
    #         if results_no_hotspots_appeared[round_true_perc] > 0:
    #             appears = results_no_hotspots_appeared[round_true_perc]
    #             avg_gerry_perc = ((results_no_hotspots[round_true_perc] * appears) + round_gerry_perc) / float(appears + 1)

    #         results_no_hotspots[round_true_perc] = avg_gerry_perc
    #         results_no_hotspots_appeared[round_true_perc] += 1

    # results_hotspots = collections.OrderedDict(sorted(results_hotspots.items()))
    # results_no_hotspots = collections.OrderedDict(sorted(results_no_hotspots.items()))

    # plt.figure()
    # plt.title('Gerrymandering results for the plurality rule with proportion restriction')
    # plt.plot(results_hotspots.keys(), results_hotspots.values(), 'r-o', label="with hotspots")
    # plt.plot(results_no_hotspots.keys(), results_no_hotspots.values(), 'b-o', label="without hotspots")
    # plt.xlabel('Actual percentage')
    # plt.ylabel('Gerrymandered percentage')
    # plt.legend(loc="upper left")
    # plt.savefig("results/graphs/plurality_proportion.png")

    # # -------------------------------------------------------------------------
    # #                                 BORDA
    # # -------------------------------------------------------------------------
    
    # results_hotspots = {}
    # results_hotspots_appeared = {x:0 for x in range(101)}
    # results_no_hotspots = {}
    # results_no_hotspots_appeared = {x:0 for x in range(101)}
    
    # for run in range(runs):
    #     for percentage in percentages:

    #         print("Run: " + str(run + 1) + "/" + str(runs) + ", percentage: " + str(percentage))

    #         remainder = 100 - percentage
    #         p_party_b = math.floor(remainder / 2.0)
    #         p_party_c = remainder - p_party_b

    #         perc = [percentage, p_party_b, p_party_c]

    #         grid = Grid(12, districts, perc, True, True)

    #         x = run_borda(grid)

    #         round_true_perc = int(round(x[0] * 100))
    #         round_gerry_perc = int(round(x[1] * 100)) 
    #         avg_gerry_perc = round_gerry_perc
    #         if results_hotspots_appeared[round_true_perc] > 0:
    #             appears = results_hotspots_appeared[round_true_perc]
    #             avg_gerry_perc = ((results_hotspots[round_true_perc] * appears) + round_gerry_perc) / float(appears + 1)

    #         results_hotspots[round_true_perc] = avg_gerry_perc
    #         results_hotspots_appeared[round_true_perc] += 1

    #         grid = Grid(12, districts, perc, False, True)

    #         x = run_borda(grid)

    #         round_true_perc = int(round(x[0] * 100))
    #         round_gerry_perc = int(round(x[1] * 100)) 
    #         avg_gerry_perc = round_gerry_perc
    #         if results_no_hotspots_appeared[round_true_perc] > 0:
    #             appears = results_no_hotspots_appeared[round_true_perc]
    #             avg_gerry_perc = ((results_no_hotspots[round_true_perc] * appears) + round_gerry_perc) / float(appears + 1)

    #         results_no_hotspots[round_true_perc] = avg_gerry_perc
    #         results_no_hotspots_appeared[round_true_perc] += 1

    # results_hotspots = collections.OrderedDict(sorted(results_hotspots.items()))
    # results_no_hotspots = collections.OrderedDict(sorted(results_no_hotspots.items()))

    # plt.figure()
    # plt.title('Gerrymandering results for the borda rule with proportion restriction')
    # plt.plot(results_hotspots.keys(), results_hotspots.values(), 'r-o', label="with hotspots")
    # plt.plot(results_no_hotspots.keys(), results_no_hotspots.values(), 'b-o', label="without hotspots")
    # plt.xlabel('Actual percentage')
    # plt.ylabel('Gerrymandered percentage')
    # plt.legend(loc="upper left")
    # plt.savefig("results/graphs/borda_proportion.png")

    # # -------------------------------------------------------------------------
    # #                               COPELAND
    # # -------------------------------------------------------------------------
    
    # results_hotspots = {}
    # results_hotspots_appeared = {x:0 for x in range(101)}
    # results_no_hotspots = {}
    # results_no_hotspots_appeared = {x:0 for x in range(101)}
    
    # for run in range(runs):
    #     for percentage in percentages:

    #         print("Run: " + str(run + 1) + "/" + str(runs) + ", percentage: " + str(percentage))

    #         remainder = 100 - percentage
    #         p_party_b = math.floor(remainder / 2.0)
    #         p_party_c = remainder - p_party_b

    #         perc = [percentage, p_party_b, p_party_c]

    #         grid = Grid(12, districts, perc, True, True)

    #         x = run_copeland(grid)

    #         round_true_perc = int(round(x[0] * 100))
    #         round_gerry_perc = int(round(x[1] * 100)) 
    #         avg_gerry_perc = round_gerry_perc
    #         if results_hotspots_appeared[round_true_perc] > 0:
    #             appears = results_hotspots_appeared[round_true_perc]
    #             avg_gerry_perc = ((results_hotspots[round_true_perc] * appears) + round_gerry_perc) / float(appears + 1)

    #         results_hotspots[round_true_perc] = avg_gerry_perc
    #         results_hotspots_appeared[round_true_perc] += 1

    #         grid = Grid(12, districts, perc, False, True)

    #         x = run_copeland(grid)

    #         round_true_perc = int(round(x[0] * 100))
    #         round_gerry_perc = int(round(x[1] * 100)) 
    #         avg_gerry_perc = round_gerry_perc
    #         if results_no_hotspots_appeared[round_true_perc] > 0:
    #             appears = results_no_hotspots_appeared[round_true_perc]
    #             avg_gerry_perc = ((results_no_hotspots[round_true_perc] * appears) + round_gerry_perc) / float(appears + 1)

    #         results_no_hotspots[round_true_perc] = avg_gerry_perc
    #         results_no_hotspots_appeared[round_true_perc] += 1

    # results_hotspots = collections.OrderedDict(sorted(results_hotspots.items()))
    # results_no_hotspots = collections.OrderedDict(sorted(results_no_hotspots.items()))

    # plt.figure()
    # plt.title('Gerrymandering results for the copeland rule with proportion restriction')
    # plt.plot(results_hotspots.keys(), results_hotspots.values(), 'r-o', label="with hotspots")
    # plt.plot(results_no_hotspots.keys(), results_no_hotspots.values(), 'b-o', label="without hotspots")
    # plt.xlabel('Actual percentage')
    # plt.ylabel('Gerrymandered percentage')
    # plt.legend(loc="upper left")
    # plt.savefig("results/graphs/copeland_proportion.png")

    # return

    # We want to catch all printed output to redirect it to a file,
    # but not lose track of the orginal stdout
    def_stdout = sys.stdout

    # All experiment options
    size_opt = [12]
    num_districts = range(4,13,2)
    hotspots_opt = [True, False]
    prop_lim_opt = [True, False]
    perc_opts = [[50,25,25],[33,33,33],[20,40,40],[10,45,45]]

    # The rule we are using
    # rule = "plurality"
    # rule = "borda"
    # rule = "copeland"

    # for size in size_opt:
    #     for dist in num_districts:
    #         for hot in hotspots_opt:
    #             for prop in prop_lim_opt:
    #                 for perc in perc_opts:
    #                     # Format description of this experiment
    #                     desc = ("S="+str(size)+"_D="+str(dist)+"_H="+str(hot)+"_P="+str(prop)+"_Pct="+str(perc))
                        
    #                     # Format path to save results
    #                     path = "results/"+rule+"/"+desc

    #                     # Create directory for results
    #                     if not os.path.exists(path):
    #                         os.makedirs(path)

    #                     # Format result locations
    #                     file = path+"/output.txt"
    #                     graph = path+"/grid.png"

    #                     # Redirect stdout to our output file
    #                     f = open(file, "w")
    #                     sys.stdout = f

    #                     # Create the grid
    #                     grid = Grid(size, dist, perc, hot, prop)
    #                     if hot:
    #                         print('hotspots:')
    #                         print grid.hotspots

    #                     # Run the algorithm
    #                     # run_plurality(grid)
    #                     # run_borda(grid)
    #                     run_copeland(grid)

    #                     # Output district sizes
    #                     for district in grid.dist_list:
    #                         print district.get_size()

    #                     # Reset stdout and close the file
    #                     sys.stdout = def_stdout
    #                     f.close()

    #                     # Save the grid
    #                     grid.save_map(graph)

    #                     # Output results to stdout for completeness
    #                     print(desc)
    #                     print("------------")
    #                     f = open(file, 'r')
    #                     print f.read()
    #                     f.close()
    #                     print("\n\n")

if __name__ == "__main__":
    main()


# ___BIN___

    # ___AVOID LAST TWO DISTS___
    # sets the districts where 'a' has more voters as to-be-conquered, then runs the iterative voter exchange process for plurality
    # def plur_gerry(self):
    #     self.rule = 'plurality'
    #     plur_conquer = self.plur_conquer()
    #     scores_in_dists = np.array([dist.get_plurality('a') for dist in self.dist_list])
    #     ranks = scores_in_dists.argsort()[::-1]
    #     # if plur_conquer / float(self.districts) > 0.5:
    #     #     plur_conquer -= 1
    #     for i in range(min(plur_conquer, self.districts)):
    #         self.dist_list[ranks[i]].set_conquer(True)
    #     first_dist = random.choice(self.dist_list)
    #     found_neighbour, new_district, old_dists, last_voter = self.plur_step(first_dist)
    #     max_iterations = 300
    #     iteration = 0
    #     while found_neighbour and (self.plur_victory(plur_conquer) == False) and (iteration < max_iterations):
    #         found_neighbour, new_district, old_dists, last_voter = self.plur_step(new_district, old_dists)
    #         iteration += 1
    # divides the neighbour voters of a district in groups from the best the district could get to the worst, then asks the neighbour's district
    # and the grid if one of the voters can be acquired
    # def plur_step(self, dist, last_dists=[-1,-1]):
    #     neighbours = [neighbour for neighbour in self.dist_neighbours(dist) if neighbour.get_district() not in last_dists]
    #     found_neighbour = False
    #     neighbours_by_type = []
    #     if dist.get_conquer():
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
    #             and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
    #             and self.dist_list[neighbour.get_district()].get_conquer()])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != dist.plur_first()
    #             and self.dist_list[neighbour.get_district()].get_conquer()])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) != dist.plur_first()
    #             and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == dist.plur_first()
    #             and self.dist_list[neighbour.get_district()].get_conquer()])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a' and neighbour.get(1) == dist.plur_first()
    #             and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
    #     else:
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
    #             and self.dist_list[neighbour.get_district()].plur_first() == neighbour.get(1)
    #             and self.dist_list[neighbour.get_district()].get_conquer()])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
    #             and self.dist_list[neighbour.get_district()].plur_first() != neighbour.get(1)
    #             and self.dist_list[neighbour.get_district()].get_conquer()])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) != 'a'
    #             and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
    #             and (self.dist_list[neighbour.get_district()].get_conquer() == False)])
    #         neighbours_by_type.append([neighbour for neighbour in neighbours if neighbour.get(1) == 'a' 
    #             and self.dist_list[neighbour.get_district()].get_conquer()])
    #     all_neighbours = []
    #     for neighbour_group in neighbours_by_type:
    #         all_neighbours += neighbour_group
    #     for neighbour in all_neighbours:
    #         neighbour_dist = self.dist_list[neighbour.get_district()]
    #         if neighbour_dist.plur_ask(neighbour) and self.ask(neighbour):
    #             found_neighbour = True
    #             dist.add_voter(neighbour)
    #             neighbour_dist.remove_voter(neighbour)
    #             break;
    #     last_dists.append(dist.get_number())
    #     del last_dists[0]
    #     return found_neighbour, neighbour_dist, last_dists, neighbour

    # HOW TO EVEN THE NUMBER OF VOTERS PER DISTRICT
    # one district gets one too many voters and another gets one less correction - work in progress
    # if (found_neighbour == False):
    #     self.dist_list[old_district].add_voter(save_last_voter)
    #     self.dist_list[save_last_voter.get_district()].remove_voter(save_last_voter)
    # elif (self.plur_victory(plur_conquer)) or (iteration >= max_iterations):
    #     new_district.add_voter(last_voter)
    #     self.dist_list[old_district].remove_voter(last_voter)
    # save_last_voter = last_voter

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
