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

- `data/attachment_development_panel.csv`
- `data/attachment_context_metadata.csv`
- `data/attachment_development_profiles.csv`
- `outputs/python_attachment_model_summary.txt`
- `outputs/python_stress_attachment_trajectory.csv`
- `outputs/python_stress_attachment_trajectory.png`
- `outputs/python_attachment_context_trajectory.csv`
- `outputs/python_attachment_context_trajectory.png`
- `outputs/python_attachment_development_profiles.csv`
- `outputs/python_attachment_context_summary.csv`
- `outputs/python_attachment_support_scenario_comparison.csv`
- `outputs/python_attachment_support_scenario_comparison.png`
