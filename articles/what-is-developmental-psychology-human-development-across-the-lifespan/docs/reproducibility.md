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

- `data/developmental_lifespan_panel.csv`
- `data/school_development_context_metadata.csv`
- `data/developmental_profiles.csv`
- `outputs/python_developmental_lifespan_model_summary.txt`
- `outputs/python_structural_risk_trajectory.csv`
- `outputs/python_structural_risk_trajectory.png`
- `outputs/python_support_context_trajectory.csv`
- `outputs/python_support_context_trajectory.png`
- `outputs/python_developmental_profiles.csv`
- `outputs/python_school_context_summary.csv`
- `outputs/python_developmental_support_scenario_comparison.csv`
- `outputs/python_developmental_support_scenario_comparison.png`
