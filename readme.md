Morphological Development at the Evolutionary Timescale: Robotic Developmental Evolution
--------------------
This repository contains the code used for the 3D voxel experiments presented in the following paper:

Morphological Development at the Evolutionary Timescale: Robotic Developmental Evolution<br>
F. C. Y. Benureau, J. Tani<br>
_Artificial Life Journal_ (in press) <br>

It is a fork of repository [https://github.com/skriegman/how-devo-can-guide-evo], which was the code basis for the experiments in paper:

How morphological development can guide evolution<br>
S. Kriegman, N. Cheney, J. Bongard<br>
_Nature Scientific Reports_ (2018) <br>
[<a href="https://www.nature.com/articles/s41598-018-31868-7">HTML</a>  |  <a href="https://rdcu.be/6VmZ">PDF</a> | <a href="https://youtu.be/Ee2sU-AZWC4">VID</a> ] <br>

If using this code for academic purposes, please cite both papers above.

### How to use

The repository contains:
- `evosoro/`: the code to run the simulations, generated the results, post-process them, and generate the figures.
- `post.tar.xz`: post-processed results, as obtained for the paper results. Should be unarchived into the directory `post`, so the plotting code can use it.
- `figures/`: the figures that were used in the paper
Updated version of this repository with bugfixes may exist at .... If you run into trouble, be sure to try the latest version.


### To Regenerate the Figures from Saved Results

Unarchive the post-processed results:
```bash
tar xfv post.tar.xz
```
In the `evosoro` folder, install dependencies:
```bash
pip install -r requirements.txt
```
Then generated figures:
```bash
python plot_figs.py
```
You should obtain in the terminal:
```bash
saved ../figures/figs2_mass10_traj.pdf
saved ../figures/figs2_mass10_median_20000.pdf
saved ../figures/figs2_mass25_traj.pdf
saved ../figures/figs2_mass25_median_20000.pdf
saved ../figures/figs1_mass25_traj.pdf
saved ../figures/fig8_mass25_median_20000.pdf
saved ../figures/figs2_mass50_traj.pdf
saved ../figures/figs2_mass50_median_20000.pdf
saved ../figures/figs3_mass10_pop7_median_20000.pdf
saved ../figures/figs3_mass10_pop15_median_20000.pdf
saved ../figures/figs3_mass10_pop15_traj.pdf
saved ../figures/figs3_mass10_pop7_traj.pdf

# number of epochs to fitness 30.0
evo: 5538.0 [2676.0-6902.0]
evodevo: 2569.0 [1555.0-5294.0]
evodevo_pop15: 4317.0 [510.0-8774.0]
devoevo_mass10: 7.0 [5.5-8.0]
devoevo_mass25: 78.5 [55.0-97.5]
devoevo_mass50: 1033.0 [99.0-3752.0]
devoevo_mass10_pop7: 16.5 [14.0-26.0]
devoevo_mass10_pop15: 8.5 [8.0-13.5]

# median values slices
exp evo:
  2000 median: 8.02 (+7.68-8.97)
  3000 median: 8.66 (+8.13-9.42)
  8000 median: 11.41 (+10.83-12.14)
  9999 median: 12.01 (+11.39-29.73)
exp evodevo:
  2000 median: 4.25 (+4.04-15.38)
  3000 median: 4.85 (+4.53-37.57)
  8000 median: 49.68 (+30.20-52.66)
  9999 median: 52.88 (+48.18-55.16)
exp evodevo_pop15:
  2000 median: 3.50 (+3.16-3.71)
  3000 median: 3.81 (+3.51-4.20)
  8000 median: 4.98 (+4.80-5.69)
  9999 median: 5.91 (+5.60-6.09)
exp devoevo_mass10:
  2000 median: 55.32 (+52.56-58.41)
  3000 median: 56.71 (+54.59-60.71)
  8000 median: 58.36 (+56.48-62.35)
  9999 median: 58.95 (+57.02-62.55)
exp devoevo_mass25:
  2000 median: 54.50 (+52.41-56.52)
  3000 median: 56.63 (+54.71-58.89)
  8000 median: 59.04 (+57.50-60.98)
  9999 median: 59.21 (+57.72-61.24)
exp devoevo_mass50:
  2000 median: 9.00 (+8.18-9.89)
  3000 median: 9.88 (+8.89-10.63)
  8000 median: 11.54 (+10.82-47.55)
  9999 median: 12.02 (+11.28-48.00)
exp devoevo_mass10_pop7:
  2000 median: 47.30 (+39.86-50.45)
  3000 median: 51.10 (+45.54-54.12)
  8000 median: 53.01 (+47.03-57.63)
  9999 median: 55.33 (+47.28-57.89)
exp devoevo_mass10_pop15:
  2000 median: 52.31 (+50.77-59.08)
  3000 median: 55.10 (+53.22-60.84)
  8000 median: 58.72 (+56.85-67.67)
  9999 median: 59.58 (+57.19-69.65)

# final fitness binning
exp evo:
  seed count: 20 [<= 30.0], 6 [30< <= 65], 4 [>65]
  max perf: 80.9
exp evodevo:
  seed count: 8 [<= 30.0], 18 [30< <= 65], 4 [>65]
  max perf: 70.5
exp evodevo_pop15:
  seed count: 25 [<= 30.0], 3 [30< <= 65], 2 [>65]
  max perf: 70.8
exp devoevo_mass10:
  seed count: 1 [<= 30.0], 19 [30< <= 65], 10 [>65]
  max perf: 83.4
exp devoevo_mass25:
  seed count: 3 [<= 30.0], 19 [30< <= 65], 8 [>65]
  max perf: 88.5
exp devoevo_mass50:
  seed count: 17 [<= 30.0], 11 [30< <= 65], 2 [>65]
  max perf: 74.2
exp devoevo_mass10_pop7:
  seed count: 9 [<= 30.0], 12 [30< <= 65], 9 [>65]
  max perf: 77.6
exp devoevo_mass10_pop15:
  seed count: 1 [<= 30.0], 16 [30< <= 65], 13 [>65]
  max perf: 75.7
```

The figures will be created in

### To Regenerate the Results

Create a folder `results` in the root directory:
```bash
mkdir results
```

In the `evosoro/_voxcad/` directory, compile voxelyze and voxcad. You will need Qt (tested with 5) and Qwt (http://qwt.sourceforge.net/index.html) installed:
```bash
./rebuild_everything.sh
```
This step might throw diverse errors, as the code is less and less uptodate with today's compiler. You can try creating an issue/PR if it is the case.

The experiments take a lot of time. We used a cluster based on Slurm (https://slurm.schedmd.com/documentation.html) to run them. If you have access to such a cluster, create a python virtual environment on it, install the requirements, recompile voxelyze/voxcad as above, and then modify the file `evosoro/slurm_batch.py` to match your configuration/hardware. Then, run:
```bash
python slurm_batch.py evo.py
python slurm_batch.py evodevo.py
python slurm_batch.py devoevo_mass10.py
python slurm_batch.py devoevo_mass25.py
python slurm_batch.py devoevo_mass50.py
python slurm_batch.py devoevo_mass10_pop7.py
python slurm_batch.py devoevo_mass10_pop15.py
```
The script will write in the directory `results/`, so you might want to create a symbolic link to whichever partition of the folder storage your job can/should write to during their execution. Each slurm command above runs the experiment with seed 1 to 30 (submits 30 jobs).

If you don't have access to a cluster, you can run each experiments one by one. For instance, running the experiment "devoevo_mass10" (developmental evolution with starting mass 10%) with seed 1 can be done with:
```bash
python devoevo_mass10.py 1
```

Once the results are in, clean-up the `post/` folder and postprocess them, run in `evosoro/`:
```bash
rm -Rf ../post/*
python postprocess.py
```

And then to regenerate figures:
```bash
python plot_figs.py
```
