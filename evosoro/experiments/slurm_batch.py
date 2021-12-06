import os
import sys
import time
import argparse
import importlib
import subprocess


SCRIPT = """
#!/bin/bash
sbatch << EOT
#!/bin/bash

#SBATCH -p {queue_name}                        \t# Queue name (default short on deigo, compute on mario)
#SBATCH --job-name=k18_{name}                  \t# Job name
#SBATCH --mail-type=FAIL                       \t# Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=fabien.benureau@oist.jp
#SBATCH --ntasks=1                             \t# Run a single task
#SBATCH --cpus-per-task={n_cores}              \t# Number of cores per tasks
#SBATCH --mem={memory}                         \t# Job Memory
#SBATCH --time={duration}                      \t# Time limit hrs:min:sec
#SBATCH --output={output_filepath_slurm}       \t# Standard output log
#SBATCH --error={error_filepath_slurm}         \t# Standard error log
#SBATCH --array={array_index}                  \t# Array indexes

pwd; hostname; date;

source ~/.venvs/kriegman2018/bin/activate
time python {python_script}

echo ""
date;

EOT
"""


parser = argparse.ArgumentParser()
parser.add_argument('script',     help="the experiment script")
parser.add_argument('--quiet',    help="don't display slurm script", default=False, action='store_true')
parser.add_argument('--restart',  help="restart from scratch the computation", action='store_true', default=False)
parser.add_argument('--force',    help="launch even disabled configs", action='store_true', default=False)
parser.add_argument('--pretend',  help="do not actually submit", default=False, action='store_true')
parser.add_argument('--queue',    help="queue name (default short)", default='compute', action='store')
parser.add_argument('--tag',      help="only run config with this tag", default=None, action='store')
parser.add_argument('--array',    help="slurm array", default=None)
parser.add_argument('--nosqueue', help="don't try to get active job status", default=False, action='store_true')
args = parser.parse_args()

if __name__ == '__main__':

    assert args.script.endswith('.py')
    modname = args.script[:-3]
    exp = importlib.import_module(modname)

    queue_name = 'compute'
    duration = '{}:05:00'.format(exp.MAX_TIME)
    n_cores = exp.POP_SIZE + 3
    memory = '32gb'

    prefix = os.path.join(os.path.dirname(__file__), '../../../results/run_{}/'.format(modname))
    for seed in range(exp.MIN_SEED, exp.MAX_SEED+1):
        output_filepath = prefix + 'seed{}'.format(seed)
        if not os.path.exists(output_filepath):
            os.makedirs(output_filepath)

    output_filepath_slurm = prefix + 'seed%a_log_%A.out'
    error_filepath_slurm  = prefix + 'seed%a_log_%A.err'

    array_index ='{}-{}'.format(exp.MIN_SEED, exp.MAX_SEED)
    script = SCRIPT.format(name=modname, array_index=array_index,
                           memory=memory, duration=duration, n_cores=n_cores,
                           output_filepath_slurm=output_filepath_slurm,
                           error_filepath_slurm=error_filepath_slurm,
                           queue_name=args.queue,
                           python_script=args.script)

    print('submitting {} for seeds {}'.format(modname, array_index))

    if not args.quiet:
        print(script)
        print('')

    if not args.pretend:
        p = subprocess.Popen(script, shell=True)
        p.wait()
        time.sleep(1.0)
