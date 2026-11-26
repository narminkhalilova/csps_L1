# read observed decay data and compare it with the analytical law
import numpy as np
import matplotlib.pyplot as plt

lam = 0.3  # decay constant, given

# read the csv: skip the header, split into two columns
t, observed = np.loadtxt("decay_observed.csv", delimiter=",", skiprows=1, unpack=True)

# n0 is the first observed count, then build the analytical curve
n0 = observed[0]
analytical = n0 * np.exp(-lam * t)

# 1x2 figure with shared axes, so both plots are on the same scale
fig, (ax_obs, ax_ana) = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)

ax_obs.scatter(t, observed)
ax_obs.set_title("Observed data")
ax_obs.set_xlabel("time t")
ax_obs.set_ylabel("count n")

ax_ana.plot(t, analytical)
ax_ana.set_title("Analytical")
ax_ana.set_xlabel("time t")
ax_ana.set_ylabel("count n")

fig.savefig("figure.png", dpi=150)
