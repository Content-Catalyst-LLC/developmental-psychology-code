# Reproducibility

## Python workflow

```bash
python3 python/generate_genes_environment_panel.py
python3 python/model_genes_environment_plasticity.py
python3 python/plasticity_scenario_analysis.py
```

## R workflow

```bash
Rscript r/model_genes_environment_plasticity.R
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

- `data/genes_environment_plasticity_panel.csv`
- `data/context_metadata.csv`
- `data/child_plasticity_profiles.csv`
- `outputs/python_plasticity_model_summary.txt`
- `outputs/python_development_trajectory.csv`
- `outputs/python_development_trajectory.png`
- `outputs/python_embedded_exposure_trajectory.csv`
- `outputs/python_sensitivity_stress_profiles.csv`
- `outputs/python_plasticity_scenario_comparison.csv`
- `outputs/python_plasticity_scenario_comparison.png`
- `outputs/r_plasticity_model_summary.txt`
- `outputs/r_development_trajectory.csv`
- `outputs/r_development_trajectory.png`
