import random
from Player import Batter, Pitcher

def pa(bat, pit):
    """
    Generates two random numbers to determine the result of a simulated
    at-bat between Batter bat and Pitcher pit
    
    Returns a number that represents the outcome of the plate appearance:
        1 - single
        2 - double
        3 - triple
        4 - home run
        5 - walk
        6 - strikeout
        7 - ground out
        8 - fly out
    """
    # generate random numbers
    b_rand = random.random()*100
    p_rand = random.random()*100
    
    # determine outcome
    if b_rand < bat.walk_num() and p_rand < pit.walk_num():
        return 5
    elif b_rand >= bat.hit_num() and p_rand >= pit.hit_num():
        return hit(bat)
    else:
        return out(pit)

def hit(bat):
    """
    Generates a random number to determine the result of a simulated 
    hit by Batter bat

    Returns a number that represents the outcome of the hit:
        1 - single
        2 - double
        3 - triple
        4 - home run
    """
    # generate random number
    h_rand = random.random()*100

    # determine result
    if h_rand <= 50:
        return 1
    elif h_rand <= 80:
        return 2
    elif h_rand <= 81:
        return 3
    else:
        return 4

def out(pit):
    """
    Generates a random number to determine the result of a simulated 
    out by Pitcher pit

    Returns a number that represents the outcome of the out:
    6 - strikeout
    7 - ground out
    8 - fly out
    """
    # generate random number
    o_rand = random.random()*100

    # determine result
    if o_rand < 34:
        return 6
    elif o_rand < 68:
        return 7
    else:
        return 8
    
def sf():
    """
    On a fly out with a runner on 3rd and less than 2 outs, this function 
    will be called to generate a random number to determine if the out was
    a sacrifice fly or not

    Returns 1 if the out was a sacrifice fly, 0 otherwise.
    """
    # generate random number
    sf_rand = random.random()*100

    # determine result
    if sf_rand <= 25:
        return 1
    else:
        return 0
    
def gidp(scenario):
    """
    On a groundout with a runner on 1st and less than 2 outs, this function
    will be called to generate a random number to determine if the out was 
    a double play, fielder's choice, or ground out (out at 1st only)

    Inputs a number that represents the double play 'situation':
    1 - runner only on 1st, or runners on 1st and 3rd
    2 - runners on 1st and 2nd -- currently no implementation, uses 
    3 - bases loaded

    Returns a number that represents the generated outcome:
    1 - groundout (out at 1st)
    2 - FC (out at 2nd)
    3 - GIDP (out at 2nd and 1st)
    4 - FC (out at home)
    5 - GIDP (out at home and 1st)
    """
    # generate random number
    gidp_rand = random.random()*100

    # determine result based on scenario
    # bases loaded scenario
    if scenario == 3:
        if gidp_rand <= 5:
            return 5
        elif gidp_rand <= 15:
            return 4
        else:
            return gidp(1)
    
    # standard double play scenario (1st and 2nd)
    if scenario == 1 or scenario == 2:
        if gidp_rand <= 60:
            return 3
        elif gidp_rand <= 85:
            return 2
        else:
            return 1
        
batter = Batter('schlatr01', 'Tristin', 'Schlauch')
pitcher = Pitcher('clemekr01', 'Kris', 'Clements')
walks = 0
hits = 0
ab = 0

for i in range(1000000):
    res = pa(batter, pitcher)
    if res == 5:
        walks += 1
    else:
        ab += 1
        if res < 5:
            hits += 1

print(batter.walk_num())
print(pitcher.walk_num())
print(batter.hit_num())
print(pitcher.hit_num())
print(f"Hits: {hits}")
print(f"AVG = {hits/ab:.3}")
print(f"BB% = {walks/1000000:.3%}")