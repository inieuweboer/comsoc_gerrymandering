import random

import numpy as np


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
    # the higher the distance from an hotspot, the more unlikely the associated alternative will have a high spot in the voter preference order
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
