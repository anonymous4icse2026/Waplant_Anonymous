import json
import numpy as np
from scipy.stats import mannwhitneyu


# -------------------------------------------------------
# Cliff's Delta
# -------------------------------------------------------
def cliffs_delta(x, y):
    """
    x = baseline (waplant)
    y = ablation
    Positive means x > y
    """
    gt = 0
    lt = 0

    for xi in x:
        for yi in y:
            if xi > yi:
                gt += 1
            elif xi < yi:
                lt += 1

    return (gt - lt) / (len(x) * len(y))


# -------------------------------------------------------
# Load
# -------------------------------------------------------
with open("waplant_ablation.json") as f:
    data = json.load(f)

runtimes = ["wamr", "wasmedge", "wasmer"]

baseline = data["waplant"]


# -------------------------------------------------------
# Baseline means
# -------------------------------------------------------
baseline_means = {}

for rt in runtimes:
    baseline_means[rt] = np.mean(baseline[rt])


# -------------------------------------------------------
# Print header
# -------------------------------------------------------
print("=" * 120)
print(
    f'{"Method":25s}'
    f'{"WAMR":30s}'
    f'{"WasmEdge":30s}'
    f'{"Wasmer":30s}'
)
print("=" * 120)


# -------------------------------------------------------
# Waplant row (absolute means only)
# -------------------------------------------------------
print(
    f'{"waplant":25s}'
    f'{baseline_means["wamr"]:<30.2f}'
    f'{baseline_means["wasmedge"]:<30.2f}'
    f'{baseline_means["wasmer"]:<30.2f}'
)


# -------------------------------------------------------
# Ablations
# -------------------------------------------------------
for method, values in data.items():

    if method == "waplant":
        continue

    row = f"{method:25s}"

    for rt in runtimes:

        x = baseline[rt]
        y = values[rt]

        # mean drop
        mean_drop = baseline_means[rt] - np.mean(y)

        # significance
        _, p = mannwhitneyu(
            x,
            y,
            alternative="greater"
        )

        # effect size
        delta = cliffs_delta(x, y)

        cell = f'-{mean_drop:.2f} (p={p:.3f},d={delta:.2f})'

        row += f"{cell:<30s}"

    print(row)

print("=" * 120)
