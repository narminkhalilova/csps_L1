# cspc - computer science for physics and chemistry

my coursework repository. each practical is under PW<n>/Lab_<X>/.

## setup

create the environment for a given lab:

    conda env create -f PW1/Lab_A/environment.yml
    conda activate cspc

---

## pw1 - lab a: reproducible foundations

**what i built:**
- conda environment (environment.yml), .gitignore, radioactive decay simulation in PW1/Lab_A/decay.py
- unit tests in PW1/Lab_A/test_decay.py (3 tests)
- benchmark script PW1/Lab_A/speed.py

**speed comparison (loop vs numpy):**
- loop    : 0.378691 s
- numpy   : 0.000097 s
- speed-up: 3893.95 x faster

**tests:** all passing (yes). `pytest -v` gives 3 passed.

**conclusion:**
- the numpy version is about 3900 times faster than the pure python loop, because the loop over atoms runs in python while numpy does all atoms in one compiled call.
- all three tests pass, including the test that checks the average follows n0 * exp(-lam * t).

---

## pw1 - lab b: data, plotting, and automation

**what the data showed:**
- observed counts decrease over time from the first value n0.

**observed vs analytical:**
- the figure has observed points on the left and the analytical curve n0 * exp(-lam * t) on the right, with the same axes.
- the points follow the decreasing shape of the curve.

**snakemake pipeline:**
- one rule (plot) builds figure.png from decay_observed.csv and plot.py, and reruns only when one of these changes.
