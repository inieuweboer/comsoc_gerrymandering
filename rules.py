
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
