#!/usr/bin/env python3
"""Render linear- and log-scale expert-versus-collaboration runtime bars."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter


HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "runtime-comparison-data.json"
OUTPUT_DIR = HERE / "figures"

# ORBIT-Q visual language: Okabe–Ito colors, black outlines, light grid,
# sans-serif typography, and uncluttered axes.
HUMAN_COLOR = "#D55E00"
COLLAB_COLOR = "#0072B2"
GRID_COLOR = "#DEDEDE"
TEXT_COLOR = "#222222"


def _runtime_label(value: float) -> str:
    if value < 10:
        return f"{value:.2f}"
    return f"{value:.1f}"


def _load_records() -> list[dict[str, object]]:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    records = payload["records"]
    for record in records:
        if record["human_expert_seconds"] <= 0 or record["ai_human_seconds"] <= 0:
            raise ValueError("Runtime values must be strictly positive")
        if record["mean_paired_speedup"] <= 0:
            raise ValueError("Paired speedups must be strictly positive")
    return records


def _render(records: list[dict[str, object]], scale: str) -> None:
    if scale not in {"linear", "log"}:
        raise ValueError(f"Unsupported scale: {scale}")

    challenges = [str(record["challenge"]) for record in records]
    human = np.array(
        [float(record["human_expert_seconds"]) for record in records],
        dtype=float,
    )
    collaboration = np.array(
        [float(record["ai_human_seconds"]) for record in records],
        dtype=float,
    )

    x = np.arange(len(records), dtype=float)
    width = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 4.0), facecolor="white")
    ax.set_facecolor("white")

    human_bars = ax.bar(
        x - width / 2,
        human,
        width,
        color=HUMAN_COLOR,
        edgecolor="black",
        linewidth=0.55,
        label="Human expert",
        zorder=3,
    )
    collaboration_bars = ax.bar(
        x + width / 2,
        collaboration,
        width,
        color=COLLAB_COLOR,
        edgecolor="black",
        linewidth=0.55,
        label="AI–human optimized",
        zorder=3,
    )

    if scale == "log":
        ax.set_yscale("log")
        ax.set_ylim(0.65, 315)
        ax.set_yticks([1, 3, 10, 30, 100, 300])
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.minorticks_off()
        ylabel = "Mean evaluator runtime (s; log scale)"
    else:
        ax.set_ylim(0, 205)
        ax.set_yticks([0, 50, 100, 150, 200])
        ylabel = "Mean evaluator runtime (s)"

    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.65, zorder=0)
    ax.set_xticks(x, challenges)
    ax.set_xlabel("Challenge")
    ax.set_ylabel(ylabel)

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("black")
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(colors=TEXT_COLOR)

    for index, record in enumerate(records):
        expert_time = float(record["human_expert_seconds"])
        optimized_time = float(record["ai_human_seconds"])
        paired_speedup = float(record["mean_paired_speedup"])

        if scale == "log":
            human_y = expert_time * 1.07
            collaboration_y = optimized_time * 1.07
            speedup_y = max(expert_time, optimized_time) * 1.40
        else:
            human_y = expert_time + 2.2
            collaboration_y = optimized_time + 2.2
            speedup_y = max(expert_time, optimized_time) + 12.5

        # Separate labels slightly when the paired bars are almost equal height.
        # This is most visible for Challenge 08 and avoids a false merged value.
        close_pair = max(expert_time, optimized_time) / min(
            expert_time, optimized_time
        ) < 1.15
        label_nudge = 0.04 if close_pair else 0.0

        ax.text(
            human_bars[index].get_x()
            + human_bars[index].get_width() / 2
            - label_nudge,
            human_y,
            _runtime_label(expert_time),
            ha="center",
            va="bottom",
            fontsize=6.2,
            color=TEXT_COLOR,
        )
        ax.text(
            collaboration_bars[index].get_x()
            + collaboration_bars[index].get_width() / 2
            + label_nudge,
            collaboration_y,
            _runtime_label(optimized_time),
            ha="center",
            va="bottom",
            fontsize=6.2,
            color=TEXT_COLOR,
        )
        ax.text(
            x[index],
            speedup_y,
            f"{paired_speedup:.2f}×",
            ha="center",
            va="bottom",
            fontsize=6.8,
            color=TEXT_COLOR,
            fontweight="bold",
        )

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.08),
        ncol=2,
        frameon=False,
        handlelength=1.5,
        columnspacing=2.0,
    )
    ax.margins(x=0.018)
    fig.tight_layout(rect=(0.01, 0.01, 0.995, 0.95))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_stem = OUTPUT_DIR / f"expert-vs-collaboration-runtime-bars-{scale}"
    fig.savefig(f"{output_stem}.png", dpi=600, bbox_inches="tight")
    fig.savefig(f"{output_stem}.pdf", bbox_inches="tight")
    fig.savefig(f"{output_stem}.svg", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Arial",
                "Helvetica",
                "DejaVu Sans",
                "sans-serif",
            ],
            "font.size": 7.2,
            "axes.labelsize": 8,
            "legend.fontsize": 7.2,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.dpi": 600,
        }
    )
    records = _load_records()
    _render(records, "log")
    _render(records, "linear")


if __name__ == "__main__":
    main()
