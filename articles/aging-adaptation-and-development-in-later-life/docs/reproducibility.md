# Reproducibility

## Python workflow

```bash
python3 python/generate_aging_adaptation_panel.py
python3 python/model_aging_adaptation.py
python3 python/aging_adaptation_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_aging_adaptation.R
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

- `data/aging_adaptation_later_life_panel.csv`
- `data/care_context_metadata.csv`
- `data/person_aging_adaptation_profiles.csv`
- `outputs/python_aging_adaptation_model_summary.txt`
- `outputs/python_adjustment_trajectory.csv`
- `outputs/python_adjustment_trajectory.png`
- `outputs/python_functional_fit_trajectory.csv`
- `outputs/python_functional_fit_trajectory.png`
- `outputs/python_aging_adaptation_profiles.csv`
- `outputs/python_aging_adaptation_scenario_comparison.csv`
- `outputs/python_aging_adaptation_scenario_comparison.png`
- `outputs/r_aging_adaptation_model_summary.txt`
- `outputs/r_adjustment_trajectory.csv`
- `outputs/r_adjustment_trajectory.png`
