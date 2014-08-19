import numpy as np
import pandas as pd
import pypsignifit as psi

from model import walk, absorb, pcorrect
from plot import Finv, plot_pmf, plot_pmf_thresh

def find_theta_and_thresh(xs, ys, zs, thresh_val=0.75):
    a = "Gauss(0,5)"
    b = "Gauss(1,3)"
    l = "Beta(1.5,12)"
    data = np.array(zip(xs, ys, zs))
    B = psi.BootstrapInference(data, priors=[a, b, l], nafc=2)
    return B.estimate, Finv(thresh_val, B.estimate)

def fit(cohs, pcor, n):
    """
    fits psychometric function for accuracy at each time slice
    """
    return [find_theta_and_thresh(cohs, pc, n*np.ones(len(cohs))) for pc in pcor]

def one_condition((T, N, TND), cohs, mu, sigma, (lb, ub)):
    print 'Walking for {0} timesteps with drifts {1}, sigma {2}, bound {3}'.format(T, mu, sigma, (lb, ub))
    print '{0} trials per mean.'.format(N)
    xs = walk(cohs, (mu, sigma), T, N, TND)
    xs = absorb(xs, (lb, ub))
    pcor = pcorrect(xs)
    res = fit(cohs, pcor, N)
    plot_pmf(cohs, pcor, res)
    return res

def main():
    TND = 2 # delay before K kicks in
    cohs = [0.03, 0.06, 0.12, 0.25, 0.5] # signal strengths--multiply by K to get mean drift rate
    S = 40 # sigma of random walk
    K = 10 # base mean drift rate
    A = 150 # abs(lower/upper bounds of walk), i.e. no bias
    N = 500 # number of trials per mean; more means smaller error bars
    T = 50 # number of timesteps; has effect up until time where all particles have reached bound

    drifts = np.array(cohs)*K
    res1 = one_condition((T, N, TND), cohs, drifts, S, (-A, A))
    plot_pmf_thresh([res1])
    # res2 = one_condition((T, N, TND), cohs, drifts*2, S, (-A, A))    
    # plot_pmf_thresh([res1, res2])

if __name__ == '__main__':
    main()
