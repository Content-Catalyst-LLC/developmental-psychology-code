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

- `data/language_development_panel.csv`
- `data/language_context_metadata.csv`
- `data/language_development_profiles.csv`
- `outputs/python_language_model_summary.txt`
- `outputs/python_stress_language_trajectory.csv`
- `outputs/python_stress_language_trajectory.png`
- `outputs/python_language_context_trajectory.csv`
- `outputs/python_language_context_trajectory.png`
- `outputs/python_language_development_profiles.csv`
- `outputs/python_language_context_summary.csv`
- `outputs/python_language_support_scenario_comparison.csv`
- `outputs/python_language_support_scenario_comparison.png`
