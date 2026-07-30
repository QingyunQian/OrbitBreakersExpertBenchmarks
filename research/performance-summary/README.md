# Expert vs AI–Human Runtime Summary

This directory contains a reproducible grouped-bar comparison of the original
human-expert implementations and the fastest validated AI–human optimized
implementations.

The figures follow the visual language used by the main ORBIT-Q repository:
Okabe–Ito colors, black bar outlines, a white background, light-gray horizontal
grid lines, sans-serif typography, and uncluttered axes. Two versions are
provided from the same source data:

- a logarithmic vertical axis, which keeps sub-second and roughly three-minute
  results legible in the same panel;
- a linear vertical axis, which emphasizes absolute wall-time savings.

## Interpretation

- Numbers immediately above bars are mean evaluator runtimes in seconds.
- Bold labels above each pair are the mean paired speedup from the corresponding
  benchmark campaign.
- Challenge 08 uses the complete sufficient-memory five-pair comparison. Its
  95% paired-speedup interval crosses 1, so the displayed 1.05× mean is
  descriptive rather than a confirmed speedup.
- Challenge 07 uses an exact reduction exposed by the challenge design.
- Challenge 12 uses the promoted batched-SU4 implementation, not the secondary
  fused variant.
- Challenges 06, 08, and 10 use five benchmark pairs; the other comparisons
  use six.
- Error bars are intentionally omitted because replicate-level uncertainty is
  not uniformly available across every task in this cross-task summary.
  Task-specific reports retain the paired intervals and raw measurements.

The machine-readable values are in
[`runtime-comparison-data.json`](runtime-comparison-data.json).

## Suggested manuscript captions

### Log-scale version

**Runtime comparison of the original human-expert and AI–human optimized
solutions.** Bars show mean end-to-end evaluator runtime; the logarithmic
vertical axis accommodates the full runtime range. Values above individual
bars are seconds, and bold labels give mean paired speedup. Comparisons use
five or six matched pairs on the same machine within each task. Challenge 08
shows no confirmed runtime improvement because its paired 95% confidence
interval includes 1. Challenge 07 uses an exact reduction exposed by the
challenge design. Lower runtime is better.

### Linear-scale version

**Absolute runtime comparison of the original human-expert and AI–human
optimized solutions.** Bars show mean end-to-end evaluator runtime on a linear
vertical axis, emphasizing absolute wall-time reductions. Values above
individual bars are seconds, and bold labels give mean paired speedup.
Comparisons use five or six matched pairs on the same machine within each task.
Challenge 08 shows no confirmed runtime improvement because its paired 95%
confidence interval includes 1. Challenge 07 uses an exact reduction exposed
by the challenge design. Lower runtime is better.

## Reproduce

From the repository root:

```bash
python3 research/performance-summary/plot_runtime_comparison.py
```

The script writes PNG, PDF, and editable SVG outputs for both
`expert-vs-collaboration-runtime-bars-log` and
`expert-vs-collaboration-runtime-bars-linear` to `figures/`.
