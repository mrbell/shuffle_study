import numpy as np
from matplotlib import pyplot as pl
from stats import get_sim_stats


def plot_histograms(distances, true_x=None, true_dist=None, keys=None):

    if keys is None:
        keys=[1, 2, 3, 5, 8, 13]
    
    f = pl.figure(figsize=(9, 9))
    for i,k in enumerate(keys):
        pl.subplot(320 + i + 1) 
        pl.hist(distances[k], bins=np.arange(1, 60), label="Simulated")
        pl.title(f"{k} Shuffles")
        if true_x is not None:
            pl.plot(true_x, true_dist * len(distances[k]), '--k', alpha=0.5, label='Ideal')
        if i == 0:
            pl.legend(loc=0)
        if i >= len(keys) - 2:
            pl.xlabel("Card separation")
    pl.tight_layout();


def plot_sim_summary(sim_results, ideal_sim_stats=None):

    stats = get_sim_stats(sim_results)
    n_shuffles = sorted(sim_results.keys())

    pl.figure(figsize=(9, 6))
    pl.plot(n_shuffles, stats["mean"], "r", alpha=0.7, label='Sim Mean')
    pl.plot(n_shuffles, stats["5th"], ":r", alpha=0.7, label='Sim 5th & 95th')
    pl.plot(n_shuffles, stats["25th"], "--r", alpha=0.7, label='Sim 25th & 75th')
    pl.plot(n_shuffles, stats["75th"], "--r", alpha=0.7)
    pl.plot(n_shuffles, stats["95th"], ":r", alpha=0.7)
    
    pl.xlabel("Number of shuffles")
    pl.ylabel("Distance between adjacent cards")
    
    if ideal_sim_stats is not None:
        pl.axhline(ideal_sim_stats["mean"], c='k', alpha=0.7, label='Ideal Mean')
        pl.axhline(ideal_sim_stats["25th"], ls='--', c='k', alpha=0.7)
        pl.axhline(ideal_sim_stats["75th"], ls='--', c='k', alpha=0.7, label='Ideal 25th & 75th')
        pl.axhline(ideal_sim_stats["5th"], ls=':', c='k', alpha=0.7, label='Ideal 5th & 95th')
        pl.axhline(ideal_sim_stats["95th"], ls=':', c='k', alpha=0.7)
    pl.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
    pl.tight_layout();
    
    return stats