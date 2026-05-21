# Reproducibility Notes

## Recommended order

```bash
python3 python/generate_developmental_designs.py
python3 python/analyze_developmental_designs.py
Rscript r/analyze_research_designs.R
```

## Makefile shortcuts

```bash
make python
make r
make all
```

Optional:

```bash
make c
make cpp
make go
make rust
make julia
make fortran
```

## Expected outputs

- `data/developmental_design_panel.csv`
- `data/cross_sectional_sample.csv`
- `data/cohort_summary.csv`
- `outputs/python_design_model_summary.txt`
- `outputs/python_growth_trajectory.csv`
- `outputs/python_design_comparison.png`
- `outputs/python_missingness_by_wave.csv`
- `outputs/r_design_model_summary.txt`
- `outputs/r_growth_trajectory.csv`
- `outputs/r_design_comparison.png`
- `outputs/julia_cohort_sequential_summary.csv`
- `outputs/fortran_growth_curve.csv`

