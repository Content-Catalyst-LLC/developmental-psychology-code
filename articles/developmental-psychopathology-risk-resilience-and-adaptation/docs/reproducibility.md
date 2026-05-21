# Reproducibility

## Python workflow

```bash
python3 python/generate_developmental_psychopathology.py
python3 python/model_developmental_psychopathology.py
python3 python/scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_developmental_psychopathology.R
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

- `data/developmental_psychopathology_panel.csv`
- `data/context_metadata.csv`
- `data/child_risk_support_profiles.csv`
- `outputs/python_psychopathology_model_summary.txt`
- `outputs/python_adaptation_trajectory.csv`
- `outputs/python_adaptation_trajectory.png`
- `outputs/python_multifinality_pathways.png`
- `outputs/python_risk_support_profiles.csv`
- `outputs/python_scenario_comparison.csv`
- `outputs/python_scenario_comparison.png`
- `outputs/r_psychopathology_model_summary.txt`
- `outputs/r_adaptation_trajectory.csv`
- `outputs/r_adaptation_trajectory.png`
