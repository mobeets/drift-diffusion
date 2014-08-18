import numpy as np
import pandas as pd

from plot import plot, plot_res
from sat_exp import fit, saturating_exp

cohs = [0.03, 0.06, 0.12, 0.25, 0.5] # signal strengths--multiply by K to get mean drift rate
K = 8 # base mean drift rate
Ss = [12, 18] # sigma of random walk for two different conditions (e.g. 2D/3D)
LB, UB = -250, 250 # bounds of walk
N = 200 # number of trials per mean; more means smaller error bars
T = 100 # number of timesteps; has effect up until time where all particles have reached bound

def fit_sat_exp(xs, pcor):
    T0, N0, ncohs = xs.shape
    xs0 = xrange(T0)
    res = {}
    for i in xrange(ncohs):
        ys0 = pcor[:, i]/100.0
        res[i] = fit(xs0, ys0)
    return res

def pcorrect(xs):
    T0, N0, ncohs = xs.shape
    pcor = np.zeros([T0, ncohs])
    for i in xrange(ncohs):
        for t in xrange(T0):
            pcor[t, i] = (100*sum(xs[t, :, i] > 0)) / N0
        pcor[0, i] = 50.0
    return pcor

def absorb(xs, (lb, ub)):
    T0, N0, ncohs = xs.shape
    for i in xrange(ncohs):
        for j in xrange(N0):
            lta = np.where(xs[:, j, i] < lb)[0]
            gta = np.where(xs[:, j, i] > ub)[0]
            ind = None
            if len(lta) > 0 and len(gta) > 0:
                if lta[0] < gta[0]:
                    xs[lta[0]:, j, i] = lb
                else:
                    xs[gta[0]:, j, i] = ub
            elif len(lta) > 0:
                xs[lta[0]:, j, i] = lb
            elif len(gta) > 0:
                xs[gta[0]:, j, i] = ub
    return xs

def walk(cohs, (means, sigmas, S), T, N):
    ncohs = len(cohs)
    vs = sigmas*np.random.normal(1, S, [T, N, ncohs]) + means
    xs = np.zeros([T+1, N, ncohs])
    xs[0] = np.zeros([N, ncohs])
    for i in xrange(T):
        xs[i+1] = xs[i] + vs[i]
    return xs

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

def main(nboots=20):
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
            # plot(xs, pcor, res)
            out = collect_res(out, res, means, S)
    df = org_res(out)
    plot_res(df, 'mean', 'A', 'sig')
    plot_res(df, 'mean', 'T', 'sig')

if __name__ == '__main__':
    main()
