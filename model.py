import numpy as np

def pcorrect(xs):
    """
    calculate percent correct at each coherence and duration by finding the proportion of particles above 0
    """
    T0, N0, ncohs = xs.shape
    pcor = np.zeros([T0, ncohs])
    for i in xrange(ncohs):
        for t in xrange(T0):
            pcor[t, i] = (100.0*sum(xs[t, :, i] > 0)) / N0
        pcor[0, i] = 50.0
    return pcor

def absorb(xs, (lb, ub)):
    """
    fix random walks so they stick at bounds
    """
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
    """
    generate random walks
    """
    ncohs = len(cohs)
    vs = sigmas*np.random.normal(1, S, [T, N, ncohs]) + means
    xs = np.zeros([T+1, N, ncohs])
    xs[0] = np.zeros([N, ncohs])
    for i in xrange(T):
        xs[i+1] = xs[i] + vs[i]
    return xs
