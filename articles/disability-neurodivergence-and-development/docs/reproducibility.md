# Reproducibility

## Python workflow

```bash
python3 python/generate_disability_neurodivergence_panel.py
python3 python/model_disability_neurodivergence.py
python3 python/access_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_disability_neurodivergence.R
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

- `data/disability_neurodivergence_panel.csv`
- `data/setting_metadata.csv`
- `data/child_access_profiles.csv`
- `outputs/python_accessibility_model_summary.txt`
- `outputs/python_development_trajectory.csv`
- `outputs/python_development_trajectory.png`
- `outputs/python_participation_trajectory.png`
- `outputs/python_access_profiles.csv`
- `outputs/python_access_scenario_comparison.csv`
- `outputs/python_access_scenario_comparison.png`
- `outputs/r_accessibility_model_summary.txt`
- `outputs/r_development_trajectory.csv`
- `outputs/r_development_trajectory.png`
