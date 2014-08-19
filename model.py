import numpy as np

def pcorrect(xs):
    """
    calculate percent correct at each coherence and duration by finding the proportion of particles above 0
    """
    return np.mean(xs > 0, 1)

def absorb(xs, (lb, ub)):
    """
    fix random walks so they stick at bounds
    """
    T, N, ncohs = xs.shape
    for i in xrange(ncohs):
        for j in xrange(N):
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

def walk(cohs, (drift, sigma), T, N, TND=0):
    """
    generate random walks
    TND is delay before any non-zero drift rates kick in
    """
    xs = np.zeros([T+1, N, len(cohs)])
    diffuse = sigma*np.random.normal(0, 1, [T, N, len(cohs)])
    for i in xrange(T):
        xs[i+1] = xs[i] + diffuse[i] + (drift if i >= TND else 0)
    return xs
