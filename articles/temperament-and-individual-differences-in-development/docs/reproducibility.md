# Reproducibility

## Python workflow

```bash
python3 python/generate_temperament_panel.py
python3 python/model_temperament_goodness_of_fit.py
python3 python/temperament_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_temperament_goodness_of_fit.R
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

- `data/temperament_individual_differences_panel.csv`
- `data/classroom_metadata.csv`
- `data/child_temperament_profiles.csv`
- `outputs/python_temperament_model_summary.txt`
- `outputs/python_temperament_trajectory.csv`
- `outputs/python_temperament_trajectory.png`
- `outputs/python_goodness_of_fit_trajectory.csv`
- `outputs/python_goodness_of_fit_trajectory.png`
- `outputs/python_temperament_profiles.csv`
- `outputs/python_temperament_scenario_comparison.csv`
- `outputs/python_temperament_scenario_comparison.png`
- `outputs/r_temperament_model_summary.txt`
- `outputs/r_temperament_trajectory.csv`
- `outputs/r_temperament_trajectory.png`
