# PW3 - Data, Distributions, Testing, and Causation

Scripts and results for practical work 3. Datasets: Heart Disease (Cleveland) and a synthetic chemical-exposure dataset.

## Files

- `heart_analysis.py`: sessions 1 and 2 on heart.csv
- `chemicals_analysis.py`: task 6 and 7 on chemicals_cancer.csv
- `distributions.png`, `qq_plots.png`, `thalach_means_ci.png`, `age_vs_thalach.png`: figures from the heart script

## Data sources

- Heart Disease (Cleveland): Kaggle, ritwikb3/heart-disease-cleveland, https://www.kaggle.com/datasets/ritwikb3/heart-disease-cleveland (original data from UCI Machine Learning Repository, Heart Disease dataset, Cleveland database).
- Chemical exposure: synthetic dataset provided on Moodle (chemicals_cancer.csv).

## Session 1: characterise the data

### Distributions

- **age**: roughly bell-shaped, slightly skewed to the left (more older patients). Most patients are between 48 and 61 years old.
- **chol**: strongly right-skewed with a long tail of high values (up to 564). Most values lie between 211 and 275.
- **trestbps**: right-skewed, with a tail of high blood pressure readings (up to 200).
- **thalach**: left-skewed, with most values between 133 and 166 and a tail of low maximum heart rates (down to 71).

### Normality verdicts

Output:

    age       shapiro W=0.986 p=0.00607  skew=-0.21  excess kurtosis=-0.53
    chol      shapiro W=0.947 p=5.91e-09  skew=+1.13  excess kurtosis=+4.40
    trestbps  shapiro W=0.967 p=1.8e-06  skew=+0.70  excess kurtosis=+0.85
    thalach   shapiro W=0.976 p=7e-05  skew=-0.53  excess kurtosis=-0.07

Verdicts:
- **age: approximately normal.** Skew and kurtosis are small. Shapiro-Wilk gives p = 0.006, but with n = 303 this test flags small deviations, so the shape itself is judged close to normal.
- **chol: not normal.** Skew 1.13 and excess kurtosis 4.40 are large;.
- **trestbps: not normal.** Clear right skew (0.70) and a tail of high readings.
- **thalach: not normal, but mildly.** Skew -0.53. Shapiro-Wilk rejects normality (p = 7e-05). The shape is close enough that it matters only for the choice of test.

Why it matters: for thalach, the group comparison uses a Welch t-test and a Mann-Whitney test as a check, since Mann-Whitney does not depend on normality. The age/thalach relation uses Pearson and Spearman, and the two agree.

## Session 2: conclusions

### Task 4: does max heart rate differ between disease and healthy?

Method: the two groups are compared with a Welch t-test (does not assume equal variances). Mann-Whitney is reported as a check because thalach is not perfectly normal (see above).

| group | n | mean thalach | sd | 95% CI of mean |
|---|---|---|---|---|
| disease (target = 1) | 139 | 139.26 | 22.59 | (135.47, 143.05) |
| healthy (target = 0) | 164 | 158.38 | 19.20 | (155.42, 161.34) |

- Welch t-test: t = -7.86, p = 9.1e-14
- Mann-Whitney U: U = 5806, p = 1.9e-13

**Conclusion:** patients with heart disease reach a lower maximum heart rate. The difference is about 19 beats per minute, and it is highly significant with both tests. The 95% confidence intervals do not overlap, so the plot (thalach_means_ci.png) agrees with the test result.

### Task 5: age and thalach

Method: Pearson correlation (linear relation). Spearman is reported as a check, because it works without normality.

- Pearson: r = -0.394, p = 1.1e-12
- Spearman: rho = -0.392, p = 1.5e-12

**Interpretation:** age and maximum heart rate move in opposite directions. Older patients reach lower maximum heart rates, with a moderate correlation (about -0.4). Correlation does not show that age causes the change. Age could be linked to other factors, such as fitness or the disease itself.

## Chemical exposure: the mystery

### Task 6: the naive analysis

| chemical | r with malignancy | p |
|---|---|---|
| benzene | 0.385 | 1.3e-36 |
| cadmium | 0.880 | < 1e-300 |

Taken at face value, cadmium looks like the cause: its correlation with malignancy is more than twice as strong.

### Task 7: look again

A third variable could be driving both. The pollution index is the obvious suspect. Checking the relation of each chemical to pollution:

| chemical | r with pollution_index |
|---|---|
| benzene | 0.054 (p = 0.085) |
| cadmium | 0.982 (p < 1e-300) |

Cadmium moves almost perfectly with pollution. Benzene does not. So cadmium is a stand-in for pollution, and its correlation with malignancy may come from pollution.

To test this, the script controls for pollution and age. It computes the partial correlation: the parts of each chemical and of malignancy that are not explained by pollution and age are correlated with each other.

| chemical | partial r (controlling pollution and age) | p |
|---|---|---|
| benzene | +0.759 | 1.5e-188 |
| cadmium | +0.007 | 0.83 |

After controlling for pollution and age, cadmium's association disappears (r = 0.007, p = 0.83). Benzene's association gets stronger (r rises from 0.39 to 0.76).

The band analysis (correlation inside pollution bands of width 20) agrees on benzene: r is about +0.7 in every band. For cadmium it is smaller but not zero (+0.18 to +0.32), because the bands are wide and cadmium still tracks pollution inside each band. The partial correlation removes that leftover pollution effect, which is why it is the stronger evidence.

**Conclusion:** benzene is the real cause of malignancy in this dataset. Cadmium only looked guilty because it is almost perfectly tied to pollution. Confounding by a third variable explains the naive cadmium result.

Note on correlation vs causation: these results show that benzene is associated with malignancy after controlling for pollution and age. A dataset cannot prove causation on its own. The conclusion depends on the assumption that pollution and age are the main confounders.

## Bonus: how unpredictable is a category?

Column: `target`. Proportions: healthy (0) = 0.541, disease (1) = 0.459.

Entropy H = -sum(p log2 p) = 0.995 bits. The maximum for two classes is 1 bit (perfectly balanced). The value is almost at the maximum, so the column is nearly balanced and hard to guess: always guessing "healthy" is right only 54% of the time.
