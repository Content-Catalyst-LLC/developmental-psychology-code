# Reproducibility Notes

## Recommended order

```bash
python3 python/generate_cultural_development_panel.py
python3 python/model_cultural_development.py
Rscript r/model_culture_development.R
```

## Makefile shortcuts

```bash
make python
make r
make all
```

Optional:

```bash
make c
make cpp
make go
make rust
make julia
make fortran
```

## Expected outputs

- `data/cultural_development_panel.csv`
- `data/society_metadata.csv`
- `data/cultural_condition_summary.csv`
- `outputs/python_culture_model_summary.txt`
- `outputs/python_culture_trajectory.csv`
- `outputs/python_culture_trajectory.png`
- `outputs/python_cultural_conditions.csv`
- `outputs/python_condition_trajectories.csv`
- `outputs/python_condition_trajectories.png`
- `outputs/r_culture_model_summary.txt`
- `outputs/r_culture_trajectory.csv`
- `outputs/r_culture_trajectory.png`
- `outputs/r_condition_trajectories.csv`
- `outputs/r_condition_trajectories.png`
- `outputs/julia_cultural_development.csv`
- `outputs/fortran_cultural_development.csv`

