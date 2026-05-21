# Reproducibility

## Python workflow

```bash
python3 python/generate_stage_theory_panel.py
python3 python/model_stage_like_development.py
python3 python/stage_transition_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_stage_like_development.R
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

- `data/stage_theory_development_panel.csv`
- `data/context_metadata.csv`
- `data/stage_theory_child_profiles.csv`
- `outputs/python_stage_model_summary.txt`
- `outputs/python_stage_trajectory.csv`
- `outputs/python_stage_trajectory.png`
- `outputs/python_threshold_summary.csv`
- `outputs/python_threshold_summary.png`
- `outputs/python_stage_profiles.csv`
- `outputs/python_stage_transition_scenario_comparison.csv`
- `outputs/python_stage_transition_scenario_comparison.png`
- `outputs/r_stage_model_summary.txt`
- `outputs/r_stage_trajectory.csv`
- `outputs/r_stage_trajectory.png`
