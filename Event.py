import random

def ab(bat, pit):
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
    if b_rand < 23 and p_rand < 23:
        return 5
    elif b_rand >= 50 and p_rand >= 50:
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