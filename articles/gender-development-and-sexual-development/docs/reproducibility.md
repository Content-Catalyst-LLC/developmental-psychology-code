# Reproducibility

## Python workflow

```bash
python3 python/generate_gender_sexual_development_panel.py
python3 python/model_gender_sexual_development.py
python3 python/gender_sexual_development_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_gender_sexual_development.R
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

- `data/gender_sexual_development_panel.csv`
- `data/school_context_metadata.csv`
- `data/adolescent_development_profiles.csv`
- `outputs/python_gender_sexual_development_model_summary.txt`
- `outputs/python_stigma_trajectory.csv`
- `outputs/python_stigma_trajectory.png`
- `outputs/python_protective_context_trajectory.csv`
- `outputs/python_protective_context_trajectory.png`
- `outputs/python_adolescent_development_profiles.csv`
- `outputs/python_gender_sexual_development_scenario_comparison.csv`
- `outputs/python_gender_sexual_development_scenario_comparison.png`
- `outputs/r_gender_sexual_development_model_summary.txt`
- `outputs/r_stigma_trajectory.csv`
- `outputs/r_stigma_trajectory.png`
