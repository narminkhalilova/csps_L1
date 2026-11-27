# PW3 task 6 and 7: which chemical drives malignancy?
# naive correlation first, then control for the confounder (pollution index)
import pandas as pd
from scipy import stats

df = pd.read_csv("chemicals_cancer.csv")
print("shape:", df.shape)
print(df.head())
print()

# task 6: naive analysis, correlation of each chemical with malignancy
print("=== task 6: naive correlation with malignancy ===")
for chem in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(df[chem], df["malignancy"])
    print(f"{chem:10s} r = {r:.3f}   p = {p:.3g}")
print()

# how strongly does each chemical depend on pollution? (possible confounder)
print("=== is each chemical related to pollution_index? ===")
for chem in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(df[chem], df["pollution_index"])
    print(f"{chem:10s} vs pollution: r = {r:.3f}   p = {p:.3g}")
print()

# task 7: stratify by pollution index, recompute within narrow bands
print("=== task 7: correlation inside pollution bands ===")
bins = [0, 20, 40, 60, 80, 100]
df["pollution_band"] = pd.cut(df["pollution_index"], bins=bins)
for band, group in df.groupby("pollution_band", observed=True):
    if len(group) < 10:
        continue
    row = [f"{str(band):12s} n={len(group):3d}"]
    for chem in ["benzene", "cadmium"]:
        r, _ = stats.pearsonr(group[chem], group["malignancy"])
        row.append(f"{chem} r={r:+.2f}")
    print("   ".join(row))
print()

# partial correlation: remove the effect of pollution from both variables
print("=== partial correlation controlling for pollution and age ===")
import numpy as np
def residuals(y, covars):
    X = np.column_stack([np.ones(len(y))] + [covars[c] for c in covars])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta
controls = {"pollution": df["pollution_index"].values, "age": df["age"].values}
y = df["malignancy"].values
for chem in ["benzene", "cadmium"]:
    rx = residuals(df[chem].values, controls)
    ry = residuals(y, controls)
    r, p = stats.pearsonr(rx, ry)
    print(f"{chem:10s} partial r = {r:+.3f}   p = {p:.3g}")
