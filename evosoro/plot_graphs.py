import os
import sys
import csv
import glob
import pickle
from pathlib import Path

import toml
import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rich import print



np.random.seed(1)


RESULTS_DIR = Path(os.path.relpath((Path(__file__).parent / '../../results/').resolve(), start=os.getcwd()))
POST_DIR    = (Path(__file__).parent / '../../post/').resolve()
FIGURES_DIR = Path(os.path.relpath((Path(__file__).parent / '../../figures/').resolve(), start=os.getcwd()))
EXT = '.pdf'


# colors of the different graph lines
# '#49006a', '#7a0177', '#e457a0'
devoevo_color = ('#49006a', '#7a0177', '#e457a0')
# control     = ('#386fa4', '#59A5d8', '#84d2f6')
# development = ('#49006a', '#7a0177', '#e457a0')

colors = {'evo'           : ('#386fa4', '#59A5d8', '#84d2f6'),
          'evodevo'       : ('#CB8260', '#EDCBB8', '#EDCBB8'),
          'evodevo_pop15' : ('#CB8260', '#EDCBB8', '#EDCBB8'),
          'devoevo_mass10': devoevo_color,
          'devoevo_mass25': devoevo_color,
          'devoevo_mass50': devoevo_color,
          'devoevo_mass10_pop7': devoevo_color,
          'devoevo_mass10_pop15': devoevo_color,
          }


# def gather_fitness(name, seed):
#     """Get the fitness of the champions of the each generation of a run

#     Use cached data if available. If not, cache it for future executions of the script.
#     """
#     data = {}

#     # fitness_pickle = os.path.join(POST_DIR, 'run_{}/seed{}_fitness.pickle'.format(name, seed))
#     # pickle_len = 0
#     # if False and os.path.exists(fitness_pickle):
#     #     with open(fitness_pickle, 'rb') as fd:
#     #         _, seed, data = pickle.load(fd)
#     #         pickle_len = len(data)
#     #         if len(data) == 10001:
#     #             #print('{}:{}: FULL'.format(name, seed))
#     #             return name, seed, data

#     filepattern = os.path.join(RESULTS_DIR, 'run_{}/seed{}'.format(name, seed),
#                                'allIndividualsData', 'Gen_*.txt')
#     for filename in glob.glob(filepattern):
#         # print(os.path.basename(filename))
#         index = int(os.path.basename(filename)[4:-4])
#         if index not in data:
#             fits = get_fitnesses(filename)
#             data[index] = max(fits)

#     if gather_max_fitness(name, seed) == data:
#         print("FITNESS ARE THE SAME")
#     else:
#         assert False

#     # if len(data) > pickle_len:
#     print('{}:{}: {} gens (+{})'.format(name, seed, len(data), len(data) - pickle_len))

#     if not os.path.exists(os.path.dirname(fitness_pickle)):
#         os.makedirs(os.path.dirname(fitness_pickle))
#     with open(fitness_pickle, 'wb') as fd:
#         pickle.dump((name, seed, data), fd)

#     return name, seed, data

# def get_fitnesses(filename):
#     """Get fitness of the champion out of the CSV of a generation"""
#     df = pd.read_csv(filename,  sep='\t+', engine='python')
#     return df['fitness'].to_numpy()


def load_seed_fitness(name, seed):
    path = POST_DIR / 'run_{}'.format(name) / 'seed{}'.format(seed) / 'fitness.feather'
    return pd.read_feather(path)['fitness'].to_numpy() / 4

def load_exp_fitness(name, seeds=tuple(range(1, 31))):
    fitnesses = [load_seed_fitness(name, seed) for seed in seeds]
    return np.stack(fitnesses, axis=1)

def bootstrapped_median(data, nboot=5000, q=95, stat=np.median):
    """Compute median and bootstrapped median CI"""
    values = []
    for _ in range(nboot):
        sample = np.random.choice(data, len(data))
        values.append(stat(sample))
    return np.percentile(values, 100-q), np.median(data), np.percentile(values, q)

def bootstrapped_medians(data, nboot=5000, q=95, stat=np.median):
    sample_indexes = np.array(range(data.shape[1]))
    values = []
    row_indexes = np.array([data.shape[1]*[i] for i in range(data.shape[0])])
    for _ in tqdm.tqdm(range(nboot), desc='bootstrapping medians...'):
        col_indexes = np.random.randint(0, data.shape[1], size=data.shape)
        values.append(stat(data[row_indexes,col_indexes], axis=1))
    return np.stack([np.percentile(values, 100-q, axis=0), stat(data, axis=1), np.percentile(values, q, axis=0)], axis=1)

# def bootstrapped_medians(data, nboot=5000, q=95, stat=np.median):
#     sample_indexes = np.array(range(data.shape[1]))
#     values = []
#     for _ in tqdm.tqdm(range(nboot), desc='bootstrapping medians...'):
#         sample = np.random.choice(sample_indexes, len(sample_indexes))
#         values.append(stat(data[:,sample], axis=1))
#     return np.stack([np.percentile(values, 100-q, axis=0), stat(data, axis=1), np.percentile(values, q, axis=0)], axis=1)


def exp_medians(name, seeds, nboot=20000, q=95):
    """Load or compute the medians of a fitness's experiment."""
    path_medians = POST_DIR / 'run_{}'.format(name) / 'medians_vectorized_{}_{}'.format(nboot, q)
    if Path(str(path_medians) + '.npy').exists():
        with open(str(path_medians) + '.toml', 'r') as fd:
            desc = toml.load(fd)
        assert desc['seeds'] == seeds and desc['nboot'] == nboot and desc['q'] == q
        return np.load(str(path_medians) + '.npy')
    else:
        fitnesses = load_exp_fitness(name, seeds)
        # medians = np.array([bootstrapped_median(fitnesses[t], nboot=nboot, q=q) for t in tqdm.tqdm(range(len(fitnesses)), desc='bootstrapping medians...')])
        medians = bootstrapped_medians(fitnesses, nboot=nboot, q=q)
        with open(str(path_medians) + '.toml', 'w') as fd:
            toml.dump({'seeds': seeds, 'nboot': nboot, 'q': q}, fd)
        np.save(path_medians, medians)
        return medians


def generate_traj_graph(exps, filename, y_max=None):
    """Generate the fitness trajectory graphs

    :param fitnesses:  list of (name, fitness_array) argument. `fitness_array` is of shape
                       n_epoch x n_seed.
    :param y_max:  set this value to get the same y-scale on different graphs.
    """
    # print('generating figure [bold]{}{}[/bold]...'.format(filename, EXT))
    fig, ax = plt.subplots(figsize=[10, 8])
    ax.spines.left.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.yaxis.tick_right()
    ax.margins(x=0)
    ax.margins(y=0)

    max_perf = 0
    for name, seeds in exps:
        fitness_array = load_exp_fitness(name)
        max_perf = max(max_perf, max(fitness_array[-1]))
        for seed in seeds:
            fitness = fitness_array[:,seed-1]
            # print(fitness)
            line_color, dark_color, light_color = colors[name]
            x = list(range(len(fitness)))
            y = fitness
            ax.plot(x, y, color=line_color, linewidth=0.25, alpha=0.75)

    if y_max is not None:
        ax.set_ylim(0, y_max)

    y_ticks = [0, 30, 65, max_perf]
    y_labels = [str(e) for e in y_ticks[:-1]] + ['{:.1f}'.format(y_ticks[-1])]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=10)

    fig.savefig(FIGURES_DIR / (filename + EXT))
    plt.close(fig)
    print('saved {}'.format(FIGURES_DIR / (filename + EXT)))


def generate_median_graph(exps, filename, nboot=5000, q=95,
                          y_ticks_displayed=[0, 30, 65], y_max=None,
                          dashed=()):
    """Generate the median graphs"""
    # print('generating figure [bold]{}{}[/bold]...'.format(filename, EXT))
    fig, ax = plt.subplots(figsize=[10, 8])
    ax.spines.left.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.yaxis.tick_right()
    ax.margins(x=0)
    ax.margins(y=0)
    pooled = {}

    y_ticks = []
    # compute medians
    for name, seeds in exps:
        medians = exp_medians(name, seeds, nboot=nboot, q=q)
        x = list(range(len(medians)))
        m       = medians[:,1]
        ci_low  = medians[:,0]
        ci_high = medians[:,2]
        shortname = name.split('_')[0]

        line_color, dark_color, light_color = colors[name]
        if name in dashed:
            ax.fill_between(x, ci_low, ci_high, facecolor=light_color, alpha=0.35)
            ax.plot(x, m, color=line_color, linewidth=1.5, label=shortname, linestyle='dotted')
        else:
            ax.fill_between(x, ci_low, ci_high, facecolor=light_color, alpha=0.5)
            ax.plot(x, m, color=line_color, linewidth=2.0, label=shortname)

        # for age in [2000, 3000, 8000, 9999]:
        #     if len(m) > age:
        #         print('{} median: {}: {:.2f} (+{:.2f}-{:.2f})'.format(age, name, m[age], ci_low[age], ci_high[age]))
        y_ticks.append(m[-1])


    y_labels = ['{:.1f}'.format(e) for e in y_ticks]
    for e in y_ticks_displayed:
        y_ticks.append(e)
        y_labels.append(str(e))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=10)
    if y_max is not None:
        ax.set_ylim(0, y_max)

    fig.savefig(FIGURES_DIR / (filename + EXT))
    print('saved {}'.format(FIGURES_DIR / (filename + EXT)))


def print_medians(exps, nboot=20000, q=95):
    print('# median values slices')
    for name, seeds in exps:
        medians = exp_medians(name, seeds, nboot=nboot, q=q)
        print('exp {}:'.format(name))
        for age in [2000, 3000, 8000, 9999]:
            print('  {} median: {:.2f} (+{:.2f}-{:.2f})'.format(age, medians[age][1], medians[age][0], medians[age][2]))


def epoch_to_fitness30(exps):
    epochs_to_30 = {}
    for name, seeds in exps:
        epochs_to_30[name] = ([], [])
        for seed in seeds:
            fitness = load_seed_fitness(name, seed)
            index = -1
            for i, f in enumerate(fitness):
                if f > 30.0:
                    index = i
                    break
            if index != -1:  # the seed reach 30.0
                epochs_to_30[name][0].append(index)
                epochs_to_30[name][1].append(index)
            else:  # never reached.
                epochs_to_30[name][1].append(len(fitness) - 1)

    print('# number of epochs to fitness 30.0')
    for name, epochs in epochs_to_30.items():
        # if unsuccessful seeds not included
        ci_low, med, ci_high = bootstrapped_median(epochs[0], nboot=nboot)
        print('{}: {:.1f} [{:.1f}-{:.1f}]'.format(name, med, ci_low, ci_high))
        # if unsuccessful seeds are counted as total epochs (not really consistent)
        ci_low, med, ci_high = bootstrapped_median(epochs[1], nboot=nboot)
        # print('{} full: {:.1f} [{:.1f}-{:.1f}]'.format(name, med, ci_low, ci_high))


def print_fitness_stats(exps):
    print('# final fitness binning')
    for name, _ in exps:
        print('exp {}:'.format(name))
        fitness_array = load_exp_fitness(name)
        bins = [0, 0, 0]  # <= 30, 30 > and <= 65, > 65
        for seed in range(fitness_array.shape[1]):
            final_fitness = fitness_array[-1, seed]
            if final_fitness > 65:
                bins[2] += 1
            elif final_fitness > 30:
                bins[1] += 1
            else:
                bins[0] += 1
        print('  seed count: {} [<= 30.0], {} [30< <= 65], {} [>65]'.format(*bins))
        print('  max perf: {:.1f}'.format(max(fitness_array[-1])))



if __name__ == '__main__':
    datas = []

    # nboot = 500  # fast but noisy
    nboot = 20000

    seed_range = list(range(1, 31))
    classes = [0, 30, 65]

    all_exps = [(name, seed_range) for name in ['evo', 'evodevo', 'evodevo_pop15',
                                                'devoevo_mass10', 'devoevo_mass25', 'devoevo_mass50',
                                                'devoevo_mass10_pop7', 'devoevo_mass10_pop15']]

    for mass in [10, 25, 50]:
        exps = [(name, seed_range) for name in ['evo', 'evodevo', 'devoevo_mass{}'.format(mass)]]
        generate_traj_graph(exps, 'figs2_mass{}_traj'.format(mass), y_max=110)
        generate_median_graph(exps, 'figs2_mass{}_median_{}'.format(mass, nboot), nboot=nboot,
                              y_ticks_displayed=classes, y_max=110)

        if mass == 25:
            generate_traj_graph(exps, 'figs1_mass{}_traj'.format(mass))
            generate_median_graph(exps, 'fig8_mass{}_median_{}'.format(mass,nboot),
                                  nboot=nboot, y_ticks_displayed=[0, 30, 65])

    for mass, pop_devoevo, dashed in [(10, 7, ['evo', 'evodevo_pop15']), (10, 15, ['evo', 'evodevo'])]:

        exps = [(name, seed_range) for name in ['evo', 'evodevo', 'evodevo_pop15', 'devoevo_mass{}_pop{}'.format(mass, pop_devoevo)]]
        generate_traj_graph(exps, 'figs3_mass{}_pop{}_traj'.format(mass, pop_devoevo), y_max=110)
        generate_median_graph(exps, 'figs3_mass{}_pop{}_median_{}'.format(mass, pop_devoevo, nboot), nboot=nboot,
                              y_ticks_displayed=classes, y_max=110, dashed=dashed)

    print('')
    epoch_to_fitness30(all_exps)
    print('')

    print_medians(all_exps, nboot=nboot)
    print('')

    print_fitness_stats(all_exps)
    print('')
