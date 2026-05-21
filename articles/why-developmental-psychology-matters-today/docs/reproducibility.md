# Reproducibility Notes

## Recommended order

1. Generate the synthetic panel dataset.
2. Run Python dynamic modeling.
3. Run R mixed-effects modeling.
4. Run SQL schema and queries.
5. Compile or run optional language examples.

## Main commands

```bash
python3 python/generate_developmental_panel.py
python3 python/model_developmental_trajectories.py
Rscript r/model_developmental_conditions.R
```

## Outputs

Expected generated files include:

- `data/developmental_panel.csv`
- `data/context_metadata.csv`
- `outputs/python_model_summary.txt`
- `outputs/python_developmental_trajectory.csv`
- `outputs/python_average_trajectory.png`
- `outputs/r_model_summary.txt`
- `outputs/r_average_trajectory.csv`
- `outputs/r_average_trajectory.png`

