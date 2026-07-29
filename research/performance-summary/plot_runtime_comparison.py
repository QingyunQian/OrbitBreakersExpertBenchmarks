#!/usr/bin/env python3
"""Render the expert-versus-collaboration runtime comparison."""

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

# ORBIT-Q visual language: Okabe-Ito colors, black outlines, light grid,
# DejaVu Sans typography, and uncluttered axes.
HUMAN_COLOR = "#D55E00"
COLLAB_COLOR = "#0072B2"
GRID_COLOR = "#DDDDDD"
TEXT_COLOR = "#222222"


def _runtime_label(value: float) -> str:
    return f"{value:.2f}" if value < 10 else f"{value:.1f}"


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    records = payload["records"]

    challenges = [record["challenge"] for record in records]
    human = np.array(
        [
            np.nan
            if record["human_expert_seconds"] is None
            else record["human_expert_seconds"]
            for record in records
        ],
        dtype=float,
    )
    collaboration = np.array(
        [
            np.nan
            if record["ai_human_seconds"] is None
            else record["ai_human_seconds"]
            for record in records
        ],
        dtype=float,
    )

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10.5,
            "axes.labelsize": 11,
            "axes.titlesize": 11.5,
            "legend.fontsize": 9.5,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )

    x = np.arange(len(records), dtype=float)
    width = 0.36
    fig, ax = plt.subplots(figsize=(12.8, 5.9), facecolor="white")
    ax.set_facecolor("white")

    human_bars = ax.bar(
        x - width / 2,
        human,
        width,
        color=HUMAN_COLOR,
        edgecolor="black",
        linewidth=0.7,
        label="Human expert",
        zorder=3,
    )
    collaboration_bars = ax.bar(
        x + width / 2,
        collaboration,
        width,
        color=COLLAB_COLOR,
        edgecolor="black",
        linewidth=0.7,
        label="AI–human optimized",
        zorder=3,
    )

    ax.set_yscale("log")
    ax.set_ylim(0.55, 390)
    ax.set_yticks([1, 3, 10, 30, 100, 300])
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.minorticks_off()
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.8, zorder=0)

    ax.set_xticks(x, challenges)
    ax.set_xlabel("Challenge")
    ax.set_ylabel("Mean evaluator runtime (s, log scale)")
    ax.set_title(
        "Human expert versus AI–human optimized runtime",
        fontweight="bold",
        pad=12,
    )

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("black")
        ax.spines[side].set_linewidth(1.0)
    ax.tick_params(colors=TEXT_COLOR)

    for index, record in enumerate(records):
        expert_time = record["human_expert_seconds"]
        optimized_time = record["ai_human_seconds"]
        speedup = record["speedup"]

        if expert_time is None or optimized_time is None:
            ax.text(
                x[index],
                1.05,
                "pending\nhigh-memory run",
                ha="center",
                va="center",
                fontsize=7.8,
                color="#666666",
                fontstyle="italic",
                linespacing=1.05,
            )
            continue

        ax.text(
            human_bars[index].get_x() + human_bars[index].get_width() / 2,
            expert_time * 1.08,
            _runtime_label(expert_time),
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=TEXT_COLOR,
        )
        ax.text(
            collaboration_bars[index].get_x()
            + collaboration_bars[index].get_width() / 2,
            optimized_time * 1.08,
            _runtime_label(optimized_time),
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=TEXT_COLOR,
        )
        ax.text(
            x[index],
            max(expert_time, optimized_time) * 1.52,
            f"{speedup:.2f}×",
            ha="center",
            va="bottom",
            fontsize=8.0,
            color=TEXT_COLOR,
            fontweight="bold",
        )

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.005),
        ncol=2,
        frameon=False,
        handlelength=1.6,
        columnspacing=2.2,
    )
    ax.margins(x=0.02)

    fig.tight_layout(rect=(0.02, 0.02, 0.995, 0.97))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_stem = OUTPUT_DIR / "expert-vs-collaboration-runtime-bars"
    fig.savefig(f"{output_stem}.png", dpi=220, bbox_inches="tight")
    fig.savefig(f"{output_stem}.pdf", bbox_inches="tight")
    fig.savefig(f"{output_stem}.svg", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
