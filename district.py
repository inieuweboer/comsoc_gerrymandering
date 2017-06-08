import operator

from rules import *

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

