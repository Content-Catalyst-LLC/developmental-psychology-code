# Reproducibility

## Python workflow

```bash
python3 python/generate_continuity_discontinuity_panel.py
python3 python/model_continuity_discontinuity.py
python3 python/developmental_turning_point_scenarios.py
```

## R workflow

```bash
Rscript r/model_continuity_discontinuity.R
```

## Optional compiled-language checks

```bash
make c
make cpp
make go
make rust
make julia
make fortran
```

## Expected generated files

- `data/continuity_discontinuity_panel.csv`
- `data/context_metadata.csv`
- `data/developmental_change_profiles.csv`
- `outputs/python_continuity_discontinuity_model_summary.txt`
- `outputs/python_developmental_trajectory.csv`
- `outputs/python_developmental_trajectory.png`
- `outputs/python_threshold_summary.csv`
- `outputs/python_threshold_summary.png`
- `outputs/python_developmental_profiles.csv`
- `outputs/python_turning_point_scenario_comparison.csv`
- `outputs/python_turning_point_scenario_comparison.png`
- `outputs/r_continuity_discontinuity_model_summary.txt`
- `outputs/r_developmental_trajectory.csv`
- `outputs/r_developmental_trajectory.png`
