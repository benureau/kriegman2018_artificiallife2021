import random
import os
import sys
import numpy as np
import subprocess as sub

rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(rootdir))

import evosoro
from evosoro.base import Sim, Env, ObjectiveDict
from evosoro.networks import DirectEncoding
from evosoro.softbot import Genotype, Phenotype, Population
from evosoro.tools.algorithms import SetMutRateOptimization
from evosoro.tools.checkpointing import continue_from_checkpoint

from config import *


START_DENSITY = 2.5e+005
ADULT_DENSITY = 1e+006
ADULT_GEN     = 2000
RUN_NAME = "devoevo_mass25"


if __name__ == '__main__':
    try:
        SEED = int(os.environ['SLURM_ARRAY_TASK_ID'])
    except KeyError:
        SEED = int(sys.argv[1])
    RUN_DIR = os.path.join(os.path.dirname(__file__), "../../results/run_{}/seed{}".format(RUN_NAME.lower(), SEED))
    if not os.path.exists(RUN_DIR):
        os.makedirs(RUN_DIR)

    cmd = "cp {}/_voxcad/voxelyzeMain/voxelyze .".format(rootdir)
    sub.call(cmd, shell=True)

    class MyGenotype(Genotype):
        def __init__(self):
            Genotype.__init__(self, orig_size_xyz=IND_SIZE)

            self.add_network(DirectEncoding(output_node_name="mutation_rate", orig_size_xyz=IND_SIZE,
                                            scale=META_MUT_SCALE, p=META_MUT_RATE, symmetric=False,
                                            lower_bound=MUT_RATE, start_val=MUT_RATE, mutate_start_val=True))

            self.add_network(DirectEncoding(output_node_name="init_size", orig_size_xyz=IND_SIZE,
                                            scale=MUT_SCALE))
            self.to_phenotype_mapping.add_map(name="init_size", tag="<InitialVoxelSize>")

            self.add_network(DirectEncoding(output_node_name="init_offset", orig_size_xyz=IND_SIZE,
                                            scale=MUT_SCALE, symmetric=False))
            self.to_phenotype_mapping.add_map(name="init_offset", tag="<PhaseOffset>")


    if not os.path.isfile("./" + RUN_DIR + "/pickledPops/Gen_0.pickle"):

        random.seed(SEED)
        np.random.seed(SEED)

        my_sim = Sim(dt_frac=DT_FRAC, simulation_time=SIM_TIME, min_temp_fact=MIN_TEMP_FACT,
                     fitness_eval_init_time=INIT_TIME)

        my_env = Env(temp_amp=TEMP_AMP, density=START_DENSITY)
        my_env.add_param("adult_gen", ADULT_GEN, "<AdultGen>")
        my_env.add_param("adult_density", ADULT_DENSITY, "<AdultDensity>")
        my_env.add_param("growth_amplitude", GROWTH_AMPLITUDE, "<GrowthAmplitude>")

        my_objective_dict = ObjectiveDict()
        my_objective_dict.add_objective(name="fitness", maximize=True, tag="<finalDistY>")
        my_objective_dict.add_objective(name="age", maximize=False, tag=None)

        my_pop = Population(my_objective_dict, MyGenotype, Phenotype, pop_size=POP_SIZE)

        my_optimization = SetMutRateOptimization(my_sim, my_env, my_pop, MUT_NET_PROB_DIST)
        my_optimization.run(max_hours_runtime=MAX_TIME, max_gens=MAX_GENS, num_random_individuals=NUM_RANDOM_INDS,
                            directory=RUN_DIR, name=RUN_NAME, max_eval_time=MAX_EVAL_TIME,
                            time_to_try_again=TIME_TO_TRY_AGAIN, checkpoint_every=CHECKPOINT_EVERY,
                            save_vxa_every=SAVE_VXA_EVERY, save_lineages=SAVE_LINEAGES)

    else:
        continue_from_checkpoint(directory=RUN_DIR, additional_gens=EXTRA_GENS, max_hours_runtime=MAX_TIME,
                                 max_eval_time=MAX_EVAL_TIME, time_to_try_again=TIME_TO_TRY_AGAIN,
                                 checkpoint_every=CHECKPOINT_EVERY, save_vxa_every=SAVE_VXA_EVERY,
                                 save_lineages=SAVE_LINEAGES)
