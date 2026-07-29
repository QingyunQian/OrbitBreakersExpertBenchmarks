# Expert vs AI–Human Runtime Summary

This directory contains a reproducible grouped-bar comparison of the original
human-expert implementations and the fastest validated AI–human optimized
implementations.

The figure follows the visual language used by the main ORBIT-Q repository:
Okabe–Ito colors, black bar outlines, a white background, light-gray horizontal
grid lines, DejaVu Sans typography, and uncluttered axes. A logarithmic runtime
axis keeps sub-second and roughly three-minute results legible in the same
panel.

## Interpretation

- Numbers immediately above bars are mean evaluator runtimes in seconds.
- Bold labels above each pair are `expert runtime / optimized runtime`.
- Challenge 08 is intentionally left blank. Its current records do not provide
  a fair same-machine expert-versus-optimized pair, so the chart does not
  present the existing optimized-only runtime as a comparison.
- Challenge 07 uses an exact reduction exposed by the challenge design.
- Challenge 12 uses the fastest validated fused collaboration implementation
  against the unchanged public human-expert baseline.
- Challenge 06 uses five benchmark repetitions; the other displayed
  comparisons use six.

The machine-readable values are in
[`runtime-comparison-data.json`](runtime-comparison-data.json).

## Suggested manuscript caption

**Runtime comparison of the original human-expert and AI–human optimized
solutions.** Bars show mean end-to-end evaluator runtime; the logarithmic
vertical axis accommodates the full runtime range. Values above individual
bars are seconds, and bold labels give the expert-to-optimized runtime ratio.
Challenge 08 is withheld pending a fair paired high-memory measurement. Lower
runtime is better.

## Reproduce

From the repository root:

```bash
python3 research/performance-summary/plot_runtime_comparison.py
```

The script writes PNG, PDF, and editable SVG outputs to `figures/`.
