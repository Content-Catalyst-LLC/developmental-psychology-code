# Reproducibility

## Standard run

```bash
python3 python/generate_life_course_inequality.py
python3 python/model_life_course_inequality.py
Rscript r/model_life_course_inequality.R
```

## Make shortcuts

```bash
make python
make r
make all
```

## Expected outputs

- `data/life_course_inequality_panel.csv`
- `data/person_inequality_profiles.csv`
- `outputs/python_life_course_model_summary.txt`
- `outputs/python_life_course_trajectory.csv`
- `outputs/python_life_course_trajectory.png`
- `outputs/python_inequality_profiles.csv`
- `outputs/python_profile_trajectories.csv`
- `outputs/r_life_course_model_summary.txt`
- `outputs/r_life_course_trajectory.csv`
- `outputs/r_life_course_trajectory.png`
- `outputs/r_profile_trajectories.csv`

