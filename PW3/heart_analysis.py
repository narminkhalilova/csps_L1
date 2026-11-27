# PW3 sessions 1 and 2: heart disease (cleveland) dataset
# data source: kaggle, ritwikb3/heart-disease-cleveland (file heart.csv)
import matplotlib
matplotlib.use("Agg")  # save figures without opening windows
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# ---------- session 1: characterise the data ----------
# task 1: load and look
df = pd.read_csv("heart.csv")
print("shape:", df.shape)
print(df.head())
print()

continuous = ["age", "chol", "trestbps", "thalach"]
cont = df[continuous]
print(cont.describe().round(2))
print()

# task 2: distribution of each continuous variable
fig, axes = plt.subplots(2, 2, figsize=(9, 7))
for ax, col in zip(axes.ravel(), continuous):
    ax.hist(cont[col], bins=20, edgecolor="black")
    ax.set_title(col)
    ax.set_xlabel(col)
    ax.set_ylabel("count")
fig.tight_layout()
fig.savefig("distributions.png", dpi=150)

# task 3: normality, three checks per variable
# shapiro-wilk: p < 0.05 means the data is unlikely to be normal
# skew and excess kurtosis: both near 0 for a normal shape
# qq plot: points on the line means normal
print("=== task 3: normality checks ===")
fig, axes = plt.subplots(2, 2, figsize=(9, 7))
for ax, col in zip(axes.ravel(), continuous):
    x = cont[col].dropna()
    w, p = stats.shapiro(x)
    skew = stats.skew(x)
    kurt = stats.kurtosis(x)  # excess kurtosis, 0 for normal
    print(f"{col:9s} shapiro W={w:.3f} p={p:.3g}  skew={skew:+.2f}  excess kurtosis={kurt:+.2f}")
    stats.probplot(x, dist="norm", plot=ax)
    ax.set_title(f"qq plot: {col}")
fig.tight_layout()
fig.savefig("qq_plots.png", dpi=150)
print()

# ---------- session 2: draw conclusions ----------
# task 4: does max heart rate differ between disease and healthy?
disease = df.loc[df["target"] == 1, "thalach"]
healthy = df.loc[df["target"] == 0, "thalach"]
print("=== task 4: thalach by target ===")
print(f"disease: n={len(disease)} mean={disease.mean():.2f} sd={disease.std():.2f}")
print(f"healthy: n={len(healthy)} mean={healthy.mean():.2f} sd={healthy.std():.2f}")

# welch t-test: does not assume equal variances
t, p_t = stats.ttest_ind(disease, healthy, equal_var=False)
# mann-whitney: rank-based, use if the data is clearly not normal
u, p_u = stats.mannwhitneyu(disease, healthy, alternative="two-sided")
print(f"welch t-test:    t={t:.3f}  p={p_t:.3g}")
print(f"mann-whitney U:  U={u:.0f}  p={p_u:.3g}")
print()

# 95% confidence interval for each group mean, using the t distribution
print("=== mean with 95% confidence interval ===")
means, errs = [], []
for name, g in [("disease", disease), ("healthy", healthy)]:
    m = g.mean()
    sem = stats.sem(g)
    lo, hi = stats.t.interval(0.95, len(g) - 1, loc=m, scale=sem)
    means.append(m)
    errs.append(m - lo)
    print(f"{name:8s} mean={m:.2f}  95% CI=({lo:.2f}, {hi:.2f})")

fig, ax = plt.subplots(figsize=(5, 4))
ax.errorbar(["disease", "healthy"], means, yerr=errs, fmt="o", capsize=6)
ax.set_ylabel("max heart rate (thalach)")
ax.set_title("mean thalach with 95% CI")
fig.tight_layout()
fig.savefig("thalach_means_ci.png", dpi=150)
print()

# task 5: age and thalach, do they move together?
# pearson for linear relation, spearman as check without normality
r, p_r = stats.pearsonr(df["age"], df["thalach"])
rho, p_rho = stats.spearmanr(df["age"], df["thalach"])
print("=== task 5: age vs thalach ===")
print(f"pearson  r={r:+.3f}  p={p_r:.3g}")
print(f"spearman rho={rho:+.3f}  p={p_rho:.3g}")

fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(df["age"], df["thalach"], alpha=0.6)
ax.set_xlabel("age")
ax.set_ylabel("max heart rate (thalach)")
ax.set_title(f"age vs thalach, r = {r:+.2f}")
fig.tight_layout()
fig.savefig("age_vs_thalach.png", dpi=150)
print()

# bonus: how unpredictable is the target column (entropy in bits)
# max entropy for 2 classes is 1 bit (perfectly balanced)
p = df["target"].value_counts(normalize=True).values
entropy = -np.sum(p * np.log2(p))
print("=== bonus: target entropy ===")
print(df["target"].value_counts(normalize=True).round(3))
print(f"entropy = {entropy:.3f} bits (max 1.0 for a balanced column)")
