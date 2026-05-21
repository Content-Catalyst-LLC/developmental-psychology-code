# Reproducibility Notes

## Recommended order

```bash
python3 python/generate_trauma_life_course.py
python3 python/model_trauma_life_course.py
Rscript r/model_trauma_life_course.R
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

- `data/trauma_life_course_panel.csv`
- `data/context_metadata.csv`
- `data/child_adversity_profiles.csv`
- `outputs/python_trauma_model_summary.txt`
- `outputs/python_adaptation_trajectory.csv`
- `outputs/python_adaptation_trajectory.png`
- `outputs/python_adversity_support_profiles.csv`
- `outputs/python_profile_trajectories.csv`
- `outputs/python_profile_trajectories.png`
- `outputs/r_trauma_model_summary.txt`
- `outputs/r_adaptation_trajectory.csv`
- `outputs/r_adaptation_trajectory.png`
- `outputs/r_profile_trajectories.csv`
- `outputs/r_profile_trajectories.png`
- `outputs/julia_trauma_life_course.csv`
- `outputs/fortran_trauma_life_course.csv`

