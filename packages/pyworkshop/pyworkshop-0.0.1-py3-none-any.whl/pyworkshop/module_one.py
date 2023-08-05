import numpy as np

def throw_dice(sides=6):
    return np.random.randint(1,sides+1)
