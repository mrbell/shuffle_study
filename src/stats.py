import numpy as np


def ideal_distro(deck):
    N = len(deck)
    d = np.arange(1, N)
    distro = 2 * (N - d)
    return d, distro / sum(distro)


def ideal_distro_stats(dists, distro):
    distro_stats = {}
    distro_stats['mean'] = sum(dists * distro)
    cdistro = np.cumsum(distro)
    distro_stats['5th'] = dists[np.where(cdistro > 0.05)[0][0]]
    distro_stats['25th'] = dists[np.where(cdistro > 0.25)[0][0]]
    distro_stats['75th'] = dists[np.where(cdistro > 0.75)[0][0]]
    distro_stats['95th'] = dists[np.where(cdistro > 0.95)[0][0]]
    return distro_stats


def get_sim_stats(sim_results):
    stats = {"mean": [], "median": [], "5th": [], "25th": [], "75th": [], "95th": []}
    n_shuffles = sorted(sim_results.keys())
    for shuffle_num in n_shuffles:
        stats["median"].append(np.median(sim_results[shuffle_num]))
        stats["mean"].append(np.mean(sim_results[shuffle_num]))
        for q, q_label in zip([0.05, 0.25, 0.75, 0.95], ["5th", "25th", "75th", "95th"]):
            stats[q_label].append(np.quantile(sim_results[shuffle_num], q))
    return stats


def kl_divergence(p, q):
    delta = 1e-6  # Adding a small number in case we have a count of 0 in the data set
    return np.sum([pi * np.log(pi / (qi + delta)) for pi, qi in zip(p, q) if pi != 0])


def get_distro(d):
    test, _ = np.histogram(d, np.arange(1, 61))
    return test / np.sum(test)


def get_kl_divs(result_set, ideal_distro):
    kl_divs = []
    for k in result_set:
        this_dist = get_distro(result_set[k])
        kl_divs.append(kl_divergence(this_dist, ideal_distro))
    return kl_divs
