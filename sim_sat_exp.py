import numpy as np
import pandas as pd

from sat_exp import fit_sat_exp
from plot import plot_vs_dur, plot_res, plot_particles
from model import walk, absorb, pcorrect

cohs = [0.03, 0.06, 0.12, 0.25, 0.5] # signal strengths--multiply by K to get mean drift rate
K = 8 # base mean drift rate
Ss = [12, 18] # sigma of random walk for two different conditions (e.g. 2D/3D)
LB, UB = -250, 250 # bounds of walk
N = 200 # number of trials per mean; more means smaller error bars
T = 100 # number of timesteps; has effect up until time where all particles have reached bound

def collect_res(out, res, means, sig):
    for i, sol in res.iteritems():
        m = means[i]
        s = sig[i] if hasattr(sig, '__iter__') else sig
        # print 'm={0}, s={1}, th={2}'.format(m, s, sol)
        if (m, s) not in out:
            out[(m, s)] = []
        out[(m, s)].append(sol)
    return out

def org_res(out):
    pts = []
    for k, r in out.iteritems():
        pt = [k + tuple(v) for v in r]
        pts.extend(pt)
    return pd.DataFrame(pts, columns=['mean', 'sig', 'A', 'T'])

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
            res = fit_sat_exp(xs, pcor)
            # plot_particles(xs, cohs)
            plot_vs_dur(xs, pcor, res, cohs)
            out = collect_res(out, res, means, S)
    df = org_res(out)
    plot_res(df, 'mean', 'A', 'sig')
    plot_res(df, 'mean', 'T', 'sig')

if __name__ == '__main__':
    main()
