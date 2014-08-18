import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import logistic
from sat_exp import saturating_exp

F = lambda x, (a,b,l): 0.5 + (1-0.5-l)*logistic.cdf(x, loc=a, scale=b)
Finv = lambda thresh_val, (a,b,l): logistic.ppf((thresh_val - 0.5)/(1-0.5-l), loc=a, scale=b)

def color_list(n, cmap=None):
    cm = plt.get_cmap("RdYlGn" if cmap is None else cmap)
    colors = [cm(i) for i in np.linspace(0, 1, n)]
    return colors*(n/len(colors)) + colors[:n%len(colors)]

def plot_pmf(cohs, pcor, res):
    cmap = color_list(len(res)+1, 'cool')
    xs = np.array(cohs)
    xsf = np.linspace(min(xs), max(xs), 50)
    for i, (theta, thresh) in enumerate(res):
        plt.scatter(cohs, pcor[i, :]/100.0, color=cmap[i])
        plt.plot(xsf, F(xsf, theta), color=cmap[i], linestyle='-')
    plt.xlim([0.01, None])
    plt.ylim([0.45, 1.05])
    plt.xscale('log')
    plt.xlabel('signal strength')
    plt.ylabel('accuracy')
    plt.show()

def plot_pmf_thresh(reses):
    cmap = color_list(len(reses)+5, 'Greens')
    for i, res in enumerate(reses):
        durs = np.arange(1, len(res)+1)
        ts = np.array([thresh for theta, thresh in res])
        plt.scatter(1000*durs, 100*ts, color=cmap[i])
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('duration (ms)')
    plt.ylabel('75% threshold (coh)')
    plt.show()

def plot_particles(xs, cohs):
    T0, N0, ncohs = xs.shape
    xs0 = xrange(T0)
    cmap = color_list(len(cohs)+2)
    for i in xrange(ncohs):
        label = cohs[i]
        for j in xrange(N0):
            label = label if j == 0 else None
            plt.plot(xs0, xs[:, j, i], label=label, color=cmap[i])
    plt.xlabel('duration')
    plt.ylabel('particle position')
    plt.show()

def plot_vs_dur(xs, pcor, res, cohs):
    T0, N0, ncohs = xs.shape
    xs0 = xrange(T0)
    cmap = color_list(len(cohs)+2)
    for i in xrange(ncohs):
        label = cohs[i]
        sol = res[i]
        plt.scatter(xs0, pcor[:, i]/100.0, label=label, color=cmap[i])
        plt.plot(xs0, saturating_exp(xs0, sol[0], sol[1]), linestyle='-', color=cmap[i])
    plt.xlim([0, None])
    plt.ylim([0.45, 1.05])
    plt.xlabel('duration')
    plt.ylabel('accuracy (i.e. \% of particle positions > 0)')
    plt.legend(loc='lower right')
    plt.show()

def plot_res(df, xkey, ykey, gkey, agg=True):
    grps = df[gkey].unique()
    cmap = dict(zip(grps, color_list(len(grps)+4)))
    for grp, dfc in df.groupby(gkey):
        if agg:
            dfc = dfc.groupby(xkey, as_index=False).agg([np.median, np.std]).reset_index()
            ypts = dfc[ykey, 'median'].values
            xpts = dfc[xkey].values
            pts = xpts, ypts
        else:
            pts = zip(*dfc[[xkey, ykey]].values)
        plt.errorbar(*pts, yerr=dfc[ykey, 'std'].values if (ykey, 'std') in dfc else None, label="%0.1f" % grp, color=cmap[grp])

    if ykey == 'A':
        plt.ylim([0.45, 1.05])
    # elif ykey == 'T':
    #     plt.ylim([0, 20])
    plt.xscale('log')
    plt.xlabel(xkey)
    plt.ylabel(ykey)
    plt.title('{0}-{1}'.format(xkey, ykey))
    plt.legend()
    plt.show()
