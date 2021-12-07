import copy
import shutil
import pickle
from pathlib import Path
from collections import OrderedDict

import xmltodict
import numpy as np
import pandas as pd


# path = '/Users/fcyb/Data/local/kriegman2018/results/run_devoevo_mass10/seed1/bestSoFar/fitOnly/devoevo_mass10--Gen_0002--fit_78.93030000--id_00013.vxa'
# with open(path, 'r') as fd:
#     d = xmltodict.parse(fd.read())

# print(d)
# with open(path + '.pickle', 'wb') as fd:
#     pickle.dump(d, fd)


keys = OrderedDict({'gen'      : np.int32,
                    'id'       : np.int32,
                    'dom'      : np.int32,
                    'parent_id': np.int32,
                    'fitness'  : np.float32,
                    'age'      : np.int32})

def gen_full_key(keys, dtype=np.float32):
    full_keys = copy.deepcopy(keys)
    full_keys.update(OrderedDict(
        {'variation_type'                   : str,
         'parent_fitness'                   : np.float32,
         'parent_age'                       : np.int32,
         'init_size_different_from_parent'  : bool,
         'mean_init_size'                   : dtype,
         'mean_parent_init_size'            : dtype,
         'mean_parent_diff_init_size'       : dtype,
         'init_offset_different_from_parent': bool,
         'mean_init_offset'                 : dtype,
         'mean_parent_init_offset'          : dtype,
         'mean_parent_diff_init_offset'     : dtype})
    )
    return full_keys

full_keys = gen_full_key(keys, dtype=np.float32)
full_keys = gen_full_key(keys, dtype=np.float64)

RESULT_DIR = Path(__file__).parent / '..' / 'results'
POST_DIR = Path(__file__).parent / '..' / 'post'


def compress_seed_best(exp_name, seed_index):
    seed_name = 'seed{}'.format(seed_index)
    path = RESULT_DIR / exp_name / seed_name
    frame_path = path / 'bestSoFar' / 'bestOfGen.txt'
    frame = pd.read_csv(frame_path,  sep='\t+', engine='python', usecols=list(full_keys.keys()), dtype=full_keys)
    save_path = POST_DIR / exp_name / seed_name / 'fitness.feather'.format(seed_index)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_feather(save_path)
    print('created {}'.format(save_path))


def compress_seed_best_vxa(exp_name, seed_index):
    seed_name = 'seed{}'.format(seed_index)
    path = RESULT_DIR / exp_name / seed_name
    dir_path = path / 'bestSoFar' / 'fitOnly'
    name = shutil.make_archive('champions_vxa', 'xztar', path / 'bestSoFar', 'fitOnly')
    dest_path = POST_DIR / exp_name / seed_name
    dest_path.mkdir(parents=True, exist_ok=True)
    shutil.move(name, dest_path)
    print('created {}'.format(dest_path / Path(name).name))


def compress_seed_gen(exp_name, seed_index):
    path = RESULT_DIR / exp_name / 'seed{}'.format(seed_index)
    frames = []
    for g in range(10001):
        frame_path = path / 'allIndividualsData' / 'Gen_{:04d}.txt'.format(g)
        frame = pd.read_csv(frame_path,  sep='\t+', engine='python')
        frames.append(frame)
    full_data = pd.concat(frames, ignore_index=True, sort=False)
    save_path = path / 'allIndividualsData.feather'

    # save_path = POST_DIR / exp_name / 'seed{}.feather'.format(seed_index)
    # save_path.parent.mkdir(parents=True, exist_ok=True)
    full_data.to_feather(save_path)
    print('saved {}'.format(save_path))


def small_txt_files(exp_name, seed_index):
    path = RESULT_DIR / exp_name / 'seed{}'.format(seed_index)
    frames = []
    for g in range(10001):
        frame_path = path / 'allIndividualsData' / 'Gen_{:04d}.txt'.format(g)
        frame = pd.read_csv(frame_path,  sep='\t+', engine='python', usecols=list(full_keys.keys()), dtype=full_keys)
        frame.to_csv(str(frame_path), sep='\t')


if __name__ == '__main__':
    for exp_name in ['run_devoevo_mass10',
                     'run_devoevo_mass10_pop7',
                     'run_devoevo_mass10_pop15',
                     'run_devoevo_mass25',
                     'run_devoevo_mass50',
                     'run_evo',
                     'run_evodevo',
                     'run_evodevo_pop15'
                    ]:
        for seed in range(1, 31):
            compress_seed_best(exp_name, seed)
            compress_seed_best_vxa(exp_name, seed)
            # compress_seed_gen(exp_name, seed)
