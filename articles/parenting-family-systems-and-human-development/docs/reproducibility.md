# Reproducibility

## Python workflow

```bash
python3 python/generate_family_systems_panel.py
python3 python/model_family_systems.py
python3 python/family_support_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_family_systems.R
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

- `data/family_systems_panel.csv`
- `data/household_metadata.csv`
- `data/child_family_profiles.csv`
- `outputs/python_family_systems_model_summary.txt`
- `outputs/python_development_trajectory.csv`
- `outputs/python_development_trajectory.png`
- `outputs/python_family_support_trajectory.csv`
- `outputs/python_family_support_profiles.csv`
- `outputs/python_family_support_scenario_comparison.csv`
- `outputs/python_family_support_scenario_comparison.png`
- `outputs/r_family_systems_model_summary.txt`
- `outputs/r_development_trajectory.csv`
- `outputs/r_development_trajectory.png`
