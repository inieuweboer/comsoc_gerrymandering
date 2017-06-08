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

    # returns the alternative that is more likely to win the district under copeland
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
        if self.conquer and voter.get(1) == 'a' and (self.get_cope('ab') <= 1 or self.get_cope('ac') <= 1):
            permission = False
        # this second condition ensures that if the voter ranks the non-a alternative that is winning the district last he does not get removed from the district
        if self.conquer and voter.get(3) != 'a' and voter.get(3) == self.cope_first() and (self.get_cope('ab') <= 1 or self.get_cope('ac') <= 1):
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
