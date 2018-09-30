import os
import sys
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from hurst import compute_Hc

def hurst_t():
    np.random.seed(42)
    random_increments = np.random.randn(99999)
    series = np.cumsum(random_increments)  # create a random walk from random increments

    # Evaluate Hurst equation
    H, c, data = compute_Hc(series)
    print(H)
    assert H<0.6 and H>0.4

if __name__ == '__main__':
    hurst_t()