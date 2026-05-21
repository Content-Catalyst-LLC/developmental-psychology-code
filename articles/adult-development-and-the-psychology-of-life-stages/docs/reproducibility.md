# Reproducibility

## Python workflow

```bash
python3 python/generate_adult_development_panel.py
python3 python/model_adult_development.py
python3 python/adult_development_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_adult_development.R
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

- `data/adult_development_life_stages_panel.csv`
- `data/context_metadata.csv`
- `data/person_adult_development_profiles.csv`
- `outputs/python_adult_development_model_summary.txt`
- `outputs/python_adult_stage_trajectory.csv`
- `outputs/python_adult_stage_trajectory.png`
- `outputs/python_adult_support_burden_trajectory.csv`
- `outputs/python_adult_support_burden_trajectory.png`
- `outputs/python_adult_development_profiles.csv`
- `outputs/python_adult_development_scenario_comparison.csv`
- `outputs/python_adult_development_scenario_comparison.png`
- `outputs/r_adult_development_model_summary.txt`
- `outputs/r_adult_stage_trajectory.csv`
- `outputs/r_adult_stage_trajectory.png`
