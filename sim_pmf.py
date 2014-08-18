import numpy as np
import pandas as pd
import pypsignifit as psi

from model import walk, absorb, pcorrect
from plot import Finv, plot_pmf, plot_pmf_thresh

cohs = [0, 0.03, 0.06, 0.12, 0.25, 0.5] # signal strengths--multiply by K to get mean drift rate
K = 40 # base mean drift rate
Ss = [40, 60] # sigma of random walk for two different conditions (e.g. 2D/3D)
LB, UB = -400, 400 # bounds of walk
N = 500 # number of trials per mean; more means smaller error bars
T = 100 # number of timesteps; has effect up until time where all particles have reached bound

def find_theta_and_thresh(xs, ys, zs, thresh_val=0.75):
    data = np.array(zip(xs, ys, zs))
    a = "Gauss(0,5)"
    b = "Gauss(1,3)"
    l = "Beta(1.5,12)"
    B = psi.BootstrapInference(data, priors=[a, b, l], nafc=2)
    return B.estimate, Finv(thresh_val, B.estimate)

def fit(cohs, pcor, n):
    T0, ncohs = pcor.shape
    zs = np.array([n]*ncohs)
    xs = np.array(cohs)
    res = []
    for i in xrange(T0):
        ys = pcor[i, :]/100.0
        theta, thresh = find_theta_and_thresh(xs, ys, zs)
        res.append((theta, thresh))
    return res

def main(nboots=1):
    means = np.array(cohs)*K
    # sigmas = 1/np.sqrt(K*np.array(cohs))
    reses = []
    for i, S in enumerate(Ss):
        mu = means#*(i+1)/2.0
        sigma = Ss[0]
        lb, ub = (LB, UB) if i == 0 else (LB+200, UB-200)
        print 'Walking for {0} timesteps with means {1}, sigmas {2}'.format(T, mu, sigma)
        print '{0} trials per mean.'.format(N)
        for _ in xrange(nboots):

            xs = walk(cohs, (mu, 1, sigma), T, N)
            xs = absorb(xs, (lb, ub))
            pcor = pcorrect(xs)
            # plot_vs_coh(xs, pcor, cohs)
            res = fit(cohs, pcor, N)
            plot_pmf(cohs, pcor, res)
            reses.append(res)
    plot_pmf_thresh(reses)

if __name__ == '__main__':
    main()
