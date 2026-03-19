import numpy as np

def kelly_criterion(wins,losses):
    p = len(wins)/(len(wins) + len(losses))
    q = 1-p
    b = np.array(wins).mean() / np.array(losses).mean()
    f = ((b*p) - q)/b
    return max(0,f)
