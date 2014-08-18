import numpy as np
import matplotlib.pyplot as plt
from sat_exp import saturating_exp

def color_list(n, cmap=None):
    cm = plt.get_cmap("RdYlGn" if cmap is None else cmap)
    colors = [cm(i) for i in np.linspace(0, 1, n)]
    return colors*(n/len(colors)) + colors[:n%len(colors)]

def plot_vs_coh(xs, pcor, cohs):
    T0, N0, ncohs = xs.shape
    cmap = color_list(T0+2)
    for i in xrange(T0):
        plt.plot(cohs, pcor[i, :]/100.0, label=i, color=cmap[i])
    # plt.xscale('log')
    plt.show()

def plot_vs_dur(xs, pcor, res, cohs):
    T0, N0, ncohs = xs.shape
    xs0 = xrange(T0)
    cmap = color_list(len(cohs)+2)
    for i in xrange(ncohs):
        label = cohs[i]
        sol = res[i]
        plt.subplot(212)
        plt.plot(xs0, pcor[:, i]/100.0, label=label, color=cmap[i])
        plt.plot(xs0, saturating_exp(xs0, sol[0], sol[1]), linestyle='-', color=cmap[i])
        plt.subplot(211)
        for j in xrange(N0):
            label = label if j == 0 else None
            plt.plot(xs0, xs[:, j, i], label=label, color=cmap[i])
    plt.subplot(212)
    plt.ylim([50, 100])
    plt.legend()
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
