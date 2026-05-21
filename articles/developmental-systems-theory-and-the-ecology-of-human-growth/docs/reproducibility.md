# Reproducibility

## Python workflow

```bash
python3 python/generate_developmental_systems_panel.py
python3 python/model_developmental_systems.py
python3 python/systems_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_developmental_systems.R
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

- `data/developmental_systems_panel.csv`
- `data/school_metadata.csv`
- `data/neighborhood_metadata.csv`
- `data/child_systems_profiles.csv`
- `outputs/python_developmental_systems_model_summary.txt`
- `outputs/python_development_trajectory.csv`
- `outputs/python_development_trajectory.png`
- `outputs/python_ecological_support_trajectory.csv`
- `outputs/python_ecological_support_profiles.csv`
- `outputs/python_systems_scenario_comparison.csv`
- `outputs/python_systems_scenario_comparison.png`
- `outputs/r_developmental_systems_model_summary.txt`
- `outputs/r_development_trajectory.csv`
- `outputs/r_development_trajectory.png`
