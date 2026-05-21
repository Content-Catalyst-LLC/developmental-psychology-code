# Reproducibility

## Python workflow

```bash
python3 python/generate_wisdom_meaning_panel.py
python3 python/model_wisdom_meaning.py
python3 python/wisdom_meaning_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_wisdom_meaning.R
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

- `data/wisdom_meaning_later_life_panel.csv`
- `data/care_context_metadata.csv`
- `data/person_wisdom_meaning_profiles.csv`
- `outputs/python_wisdom_meaning_model_summary.txt`
- `outputs/python_meaning_trajectory.csv`
- `outputs/python_meaning_trajectory.png`
- `outputs/python_wisdom_trajectory.csv`
- `outputs/python_wisdom_trajectory.png`
- `outputs/python_wisdom_meaning_profiles.csv`
- `outputs/python_wisdom_meaning_scenario_comparison.csv`
- `outputs/python_wisdom_meaning_scenario_comparison.png`
- `outputs/r_wisdom_meaning_model_summary.txt`
- `outputs/r_meaning_trajectory.csv`
- `outputs/r_meaning_trajectory.png`
