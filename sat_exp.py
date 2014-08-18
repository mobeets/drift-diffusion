import numpy as np
from scipy.optimize import minimize

B = 0.5

def saturating_exp(x, A, T, B=0.5, x0=0):
    return A - (A-B)*np.exp(-(np.array(x)-x0)/T)

error_fcn = lambda xs, ys: (lambda (A, T): sum((ys - saturating_exp(xs, A, T))**2))

def fit(xs, ys, guess = (1.0, 10.0), maxtries=5, method='TNC'):
    APPROX_ZERO = 1e-5
    bounds = [(APPROX_ZERO + 0.5, APPROX_ZERO + 1.0), (APPROX_ZERO, None)]
    constraints = []
    soln = {'success': False}
    objf = error_fcn(xs, ys)
    c = 0
    while not soln['success'] and c < maxtries:
        if len(soln.keys()) > 1:
            print soln
        soln = minimize(objf, guess, method=method, bounds=bounds, constraints=constraints)
        c += 1
    return soln['x'] if soln['success'] else (None, None)

def fit_sat_exp(xs, pcor):
    T0, N0, ncohs = xs.shape
    xs0 = xrange(T0)
    res = {}
    for i in xrange(ncohs):
        ys0 = pcor[:, i]/100.0
        res[i] = fit(xs0, ys0)
    return res
