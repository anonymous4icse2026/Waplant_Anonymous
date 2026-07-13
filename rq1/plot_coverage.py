#!/usr/bin/env python3
"""
plot_coverage_3panel.py

JSON structure expected (same as plot_coverage.py):
{
  "Technique1": {
    "wamr":     [[c1, c2, c3, c4, c5, c6], ...],
    "wasmedge": [[c1, ..., c6], ...],
    "wasmer":   [[c1, ..., c6], ...]
  },
  "Technique2": { ... },
  ...
}

Usage:
    python3 plot_coverage.py input.json -o coverage_3panel
    python3 plot_coverage.py input.json -o coverage_3panel
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

RUNTIME_LABELS = {
    "wasmer": "Wasmer",
    "wasmedge": "WasmEdge",
    "wasm3": "wasm3",
    "wazero": "wazero",
    "wamr": "WAMR",
    "wasmi": "wasmi",
}

CB_COLORS = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # green
    "#D55E00",  # vermillion
    "#CC79A7",  # pink
    "#56B4E9",  # sky blue
]

MARKERS = ["o", "s", "^", "D", "v", "P"]


def load_data(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def compute_band(runs: np.ndarray, mode: str, width: float):
    mean = runs.mean(axis=0)
    if mode == "std":
        spread = runs.std(axis=0, ddof=1) if runs.shape[0] > 1 else np.zeros(runs.shape[1])
        margin = width * spread
        lower, upper = mean - margin, mean + margin
    elif mode == "minmax":
        lower, upper = runs.min(axis=0), runs.max(axis=0)
    elif mode == "ci95":
        n = runs.shape[0]
        if n > 1:
            sem = runs.std(axis=0, ddof=1) / np.sqrt(n)
            margin = width * 1.96 * sem
        else:
            margin = np.zeros(runs.shape[1])
        lower, upper = mean - margin, mean + margin
    else:
        raise ValueError(f"Unknown band mode: {mode}")
    return mean, np.clip(lower, 0, 100), np.clip(upper, 0, 100)


def main():
    parser = argparse.ArgumentParser(description="Plot a 3-panel (1x3) coverage progress figure.")
    parser.add_argument("input", type=Path, help="Path to input JSON file.")
    parser.add_argument("-o", "--output", type=Path, default=Path("coverage_3panel"),
                         help="Output path without extension (writes .png and .pdf).")
    parser.add_argument("--runtimes", nargs=3, default=["wamr", "wasmedge", "wasmer"],
                         help="Exactly 3 runtime keys to plot, left-to-right (default: wamr wasmedge wasmer).")
    parser.add_argument("--band", choices=["std", "minmax", "ci95"], default="std",
                         help="Shaded band type (default: std).")
    parser.add_argument("--band-width", type=float, default=1.5,
                         help="Multiplier on band half-width (default: 1.5).")
    parser.add_argument("--interval-hours", type=float, default=4.0,
                         help="Spacing between measurement points in hours (default: 4).")
    parser.add_argument("--ymax", type=float, default=None,
                         help="Optional hard ceiling for the y-axis (e.g. 100). If set, each panel's "
                              "y-limit is min(panel_max_value + 5, ymax). If unset (default), each "
                              "panel's y-axis is capped at exactly its own max plotted value + 5.")
    args = parser.parse_args()

    data = load_data(args.input)
    techniques = list(data.keys())
    if len(techniques) > len(CB_COLORS):
        sys.exit(f"Error: {len(techniques)} techniques found, only {len(CB_COLORS)} colors defined.")

    runtimes = args.runtimes

    # Infer n_points from the first available series among the requested runtimes.
    n_points = None
    for tech in techniques:
        for rt in runtimes:
            runs = data.get(tech, {}).get(rt)
            if runs:
                n_points = len(runs[0])
                break
        if n_points:
            break
    if n_points is None:
        sys.exit(f"Error: no data found for runtimes {runtimes} in {args.input}.")

    x = np.arange(1, n_points + 1) * args.interval_hours

    mpl.rcParams.update({
        "font.size": 16,
        "font.family": "serif",
        "axes.labelsize": 17,
        "axes.titlesize": 17,
        "legend.fontsize": 15,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig, axes = plt.subplots(3, 1, figsize=(6, 11), sharey=False)

    legend_handles = {}

    for ax, rt in zip(axes, runtimes):
        any_data = False
        panel_max = 0.0
        for t_idx, tech in enumerate(techniques):
            runs_list = data.get(tech, {}).get(rt)
            if not runs_list:
                continue

            runs = np.array(runs_list, dtype=float)
            if runs.ndim != 2 or runs.shape[1] != n_points:
                sys.exit(f"Error: '{tech}' -> '{rt}' has inconsistent shape {runs.shape}; expected (*, {n_points}).")

            mean, lower, upper = compute_band(runs, args.band, args.band_width)
            color = CB_COLORS[t_idx]
            marker = MARKERS[t_idx % len(MARKERS)]

            line, = ax.plot(x, mean, color=color, marker=marker, markersize=4,
                             linewidth=1.6, label=tech)
            ax.fill_between(x, lower, upper, color=color, alpha=0.22, linewidth=0)

            legend_handles[tech] = line
            any_data = True
            panel_max = max(panel_max, float(upper.max()))

        ax.set_title(RUNTIME_LABELS.get(rt, rt))
        ax.set_xlabel("Time (hours)")
        ax.set_xticks(x)
        if any_data:
            ax.set_ylim(0, min(panel_max + 5, args.ymax) if args.ymax else panel_max + 5)
        else:
            ax.set_ylim(0, args.ymax if args.ymax else 100)
        ax.grid(True, linestyle="--", alpha=0.4, linewidth=0.6)

        if not any_data:
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                    ha="center", va="center", fontsize=10, color="gray")

        ax.set_ylabel("Branch coverage (%)")

    ordered_labels = [t for t in techniques if t in legend_handles]
    ordered_handles = [legend_handles[t] for t in ordered_labels]
    fig.legend(ordered_handles, ordered_labels, loc="lower center",
               ncol=min(len(ordered_labels), 4), frameon=False,
               bbox_to_anchor=(0.5, -0.02))

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    out_png = args.output.with_suffix(".png")
    out_pdf = args.output.with_suffix(".pdf")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    print(f"Saved: {out_png}")
    print(f"Saved: {out_pdf}")


if __name__ == "__main__":
    main()