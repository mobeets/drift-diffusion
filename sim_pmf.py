import numpy as np
import pandas as pd

from model import walk, absorb, pcorrect
from plot import plot_vs_coh

cohs = [0, 0.03, 0.06, 0.12, 0.25, 0.5] # signal strengths--multiply by K to get mean drift rate
K = 8 # base mean drift rate
Ss = [40, 60] # sigma of random walk for two different conditions (e.g. 2D/3D)
LB, UB = -250, 250 # bounds of walk
N = 500 # number of trials per mean; more means smaller error bars
T = 100 # number of timesteps; has effect up until time where all particles have reached bound

def main(nboots=1):
    means = np.array(cohs)*K
    # sigmas = 1/np.sqrt(K*np.array(cohs))
    out = {}
    for S in Ss:
        print 'Walking for {0} timesteps with means {1}, sigmas {2}'.format(T, means, S)
        print '{0} trials per mean.'.format(N)
        for _ in xrange(nboots):
            xs = walk(cohs, (means, 1, S), T, N)
            xs = absorb(xs, (LB, UB))
            pcor = pcorrect(xs)
            plot_vs_coh(xs, pcor, cohs)

if __name__ == '__main__':
    main()
