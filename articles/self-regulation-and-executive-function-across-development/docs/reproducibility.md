# Reproducibility

Run the main workflow:

```bash
make python
make scenarios
```

Run optional language checks:

```bash
make r
make c
make cpp
make go
make rust
make julia
make fortran
```

Outputs are written to `outputs/`.

## Expected primary outputs

- `data/regulation_development_panel.csv`
- `data/school_regulation_context_metadata.csv`
- `data/regulation_development_profiles.csv`
- `outputs/python_regulation_model_summary.txt`
- `outputs/python_stress_regulation_trajectory.csv`
- `outputs/python_stress_regulation_trajectory.png`
- `outputs/python_regulation_context_trajectory.csv`
- `outputs/python_regulation_context_trajectory.png`
- `outputs/python_regulation_profiles.csv`
- `outputs/python_school_regulation_context_summary.csv`
- `outputs/python_regulation_support_scenario_comparison.csv`
- `outputs/python_regulation_support_scenario_comparison.png`
