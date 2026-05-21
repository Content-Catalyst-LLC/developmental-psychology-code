# Reproducibility

## Python workflow

```bash
python3 python/generate_nature_nurture_panel.py
python3 python/model_nature_nurture_development.py
python3 python/nature_nurture_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_nature_nurture_development.R
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

- `data/nature_nurture_development_panel.csv`
- `data/school_context_metadata.csv`
- `data/nature_nurture_child_profiles.csv`
- `outputs/python_nature_nurture_model_summary.txt`
- `outputs/python_structural_risk_trajectory.csv`
- `outputs/python_structural_risk_trajectory.png`
- `outputs/python_protective_context_trajectory.csv`
- `outputs/python_protective_context_trajectory.png`
- `outputs/python_sensitivity_profiles.csv`
- `outputs/python_nature_nurture_scenario_comparison.csv`
- `outputs/python_nature_nurture_scenario_comparison.png`
- `outputs/r_nature_nurture_model_summary.txt`
- `outputs/r_structural_risk_trajectory.csv`
- `outputs/r_structural_risk_trajectory.png`
