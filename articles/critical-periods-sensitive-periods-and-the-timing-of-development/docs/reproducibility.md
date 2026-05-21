# Reproducibility Notes

## Recommended order

```bash
python3 python/generate_timing_panel.py
python3 python/model_timing_windows.py
Rscript r/model_critical_sensitive_periods.R
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

- `data/developmental_timing_panel.csv`
- `data/timing_window_summary.csv`
- `outputs/python_timing_model_summary.txt`
- `outputs/python_timing_trajectory.csv`
- `outputs/python_timing_windows.png`
- `outputs/r_timing_model_summary.txt`
- `outputs/r_timing_trajectory.csv`
- `outputs/r_timing_windows.png`
- `outputs/julia_timing_windows.csv`
- `outputs/fortran_timing_windows.csv`

