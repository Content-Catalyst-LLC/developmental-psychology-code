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

- `data/play_development_panel.csv`
- `data/play_context_metadata.csv`
- `data/play_development_profiles.csv`
- `outputs/python_play_development_model_summary.txt`
- `outputs/python_stress_play_development_trajectory.csv`
- `outputs/python_stress_play_development_trajectory.png`
- `outputs/python_play_context_trajectory.csv`
- `outputs/python_play_context_trajectory.png`
- `outputs/python_play_development_profiles.csv`
- `outputs/python_play_context_summary.csv`
- `outputs/python_play_development_scenario_comparison.csv`
- `outputs/python_play_development_scenario_comparison.png`
