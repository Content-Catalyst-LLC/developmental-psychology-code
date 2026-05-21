# Reproducibility

## Python workflow

```bash
python3 python/generate_lifespan_baltes_panel.py
python3 python/model_lifespan_baltes.py
python3 python/lifespan_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_lifespan_baltes.R
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

- `data/lifespan_baltes_panel.csv`
- `data/cohort_metadata.csv`
- `data/person_lifespan_profiles.csv`
- `outputs/python_lifespan_baltes_model_summary.txt`
- `outputs/python_lifespan_trajectory.csv`
- `outputs/python_lifespan_trajectory.png`
- `outputs/python_soc_trajectory.csv`
- `outputs/python_lifespan_profiles.csv`
- `outputs/python_lifespan_scenario_comparison.csv`
- `outputs/python_lifespan_scenario_comparison.png`
- `outputs/r_lifespan_baltes_model_summary.txt`
- `outputs/r_lifespan_trajectory.csv`
- `outputs/r_lifespan_trajectory.png`
