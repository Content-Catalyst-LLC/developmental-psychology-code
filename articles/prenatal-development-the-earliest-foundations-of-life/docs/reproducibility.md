# Reproducibility

## Python workflow

```bash
python3 python/generate_prenatal_development_panel.py
python3 python/model_prenatal_development.py
python3 python/prenatal_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_prenatal_development.R
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

- `data/prenatal_development_foundations_panel.csv`
- `data/neighborhood_context_metadata.csv`
- `data/prenatal_case_profiles.csv`
- `outputs/python_prenatal_development_model_summary.txt`
- `outputs/python_prenatal_stress_summary.csv`
- `outputs/python_prenatal_stress_summary.png`
- `outputs/python_effective_care_summary.csv`
- `outputs/python_effective_care_summary.png`
- `outputs/python_prenatal_profiles.csv`
- `outputs/python_prenatal_scenario_comparison.csv`
- `outputs/python_prenatal_scenario_comparison.png`
- `outputs/r_prenatal_development_model_summary.txt`
- `outputs/r_prenatal_stress_summary.csv`
- `outputs/r_prenatal_stress_summary.png`
