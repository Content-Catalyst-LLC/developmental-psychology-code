# Reproducibility

## Python workflow

```bash
python3 python/generate_schooling_development_panel.py
python3 python/model_schooling_development.py
python3 python/schooling_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_schooling_development.R
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

- `data/schooling_development_panel.csv`
- `data/school_metadata.csv`
- `data/student_school_profiles.csv`
- `outputs/python_schooling_model_summary.txt`
- `outputs/python_development_trajectory.csv`
- `outputs/python_development_trajectory.png`
- `outputs/python_connectedness_trajectory.png`
- `outputs/python_school_support_profiles.csv`
- `outputs/python_schooling_scenario_comparison.csv`
- `outputs/python_schooling_scenario_comparison.png`
- `outputs/r_schooling_model_summary.txt`
- `outputs/r_development_trajectory.csv`
- `outputs/r_development_trajectory.png`
