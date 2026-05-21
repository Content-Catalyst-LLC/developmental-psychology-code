# Critical Periods, Sensitive Periods, and the Timing of Development

This folder provides a reproducible, multi-language research companion for the article **“Critical Periods, Sensitive Periods, and the Timing of Development.”**

GitHub article folder:  
<https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/critical-periods-sensitive-periods-and-the-timing-of-development>

The article argues that developmental timing matters because organisms do not respond to experience with equal openness at all moments. Some developmental windows are unusually consequential because specific inputs may be required, while others are especially influential because the system is more plastic, responsive, or vulnerable during that period.

This repository translates that article into reproducible computational workflows.

## Research purpose

The code examples model:

- critical-period effects
- sensitive-period effects
- timing-weight functions
- experience-by-time interactions
- cumulative timing-weighted exposure
- early-childhood and adolescent sensitivity windows
- late intervention and residual plasticity
- deprivation, enrichment, support, and adversity simulations

The examples use synthetic data only. They are designed for teaching, methodological demonstration, and reproducible research scaffolding. They are not diagnostic tools and should not be used to make claims about real individuals or populations.

## Conceptual distinction

A **critical period** is modeled here as a narrow window in which a developmental input has a strong effect inside the window and little or no effect outside it.

A **sensitive period** is modeled here as a broader window in which an input has heightened influence around a developmental peak, but some influence remains outside the peak window.

## Directory structure

```text
critical-periods-sensitive-periods-and-the-timing-of-development/
├── c/              Low-level CSV summary utility
├── cpp/            C++ timing-window summary utility
├── data/           Synthetic data, schema, and data dictionary
├── docs/           Methods, ethics, interpretation, and reproducibility notes
├── fortran/        Numerical timing-window simulation
├── go/             Command-line timing summary tool
├── julia/          Multi-window developmental timing simulation
├── notebooks/      Notebook scaffold and reproducibility notes
├── outputs/        Generated summaries, figures, and model outputs
├── python/         Main synthetic data generator and timing models
├── r/              Timing-window and mixed-effects examples
├── rust/           CSV validation utility
├── sql/            Schema and analytical queries
├── Makefile        Reproducible command shortcuts
└── README.md
```

## Quick start

From this article folder:

```bash
python3 python/generate_timing_panel.py
python3 python/model_timing_windows.py
Rscript r/model_critical_sensitive_periods.R
```

Optional compiled-language examples:

```bash
gcc c/timing_summary.c -o outputs/timing_summary_c
./outputs/timing_summary_c data/developmental_timing_panel.csv

g++ -std=c++17 cpp/timing_summary.cpp -o outputs/timing_summary_cpp
./outputs/timing_summary_cpp data/developmental_timing_panel.csv

gfortran fortran/timing_window_simulation.f90 -o outputs/timing_window_simulation_fortran
./outputs/timing_window_simulation_fortran

go run go/timing_summary.go data/developmental_timing_panel.csv

rustc rust/validate_timing_panel.rs -o outputs/validate_timing_panel_rust
./outputs/validate_timing_panel_rust data/developmental_timing_panel.csv

julia julia/simulate_timing_windows.jl
```

## Core analytical model

A timing-weighted developmental effect can be written as:

```text
D_it = alpha_i + beta * E_it * w_t + error_it
```

where:

- `D_it` is a developmental outcome for person `i` at time `t`
- `E_it` is an environmental experience or input
- `w_t` is a timing weight
- `beta` is the timing-weighted effect of experience

A strict critical-period model uses a window indicator:

```text
w_t = 1 when t is inside the critical window; otherwise 0
```

A sensitive-period model can use a smooth Gaussian timing curve:

```text
w_t = exp(-((t - mu)^2) / (2 * sigma^2))
```

A cumulative timing model can sum timing-weighted exposure across development:

```text
D_it = alpha_i + sum(beta * E_i_tau * w_tau) + error_it
```

## Ethical note

Timing-window research can be misused if it becomes deterministic. Sensitive and critical period concepts should not be used to imply that children, adolescents, adults, or older adults are permanently defined by missed opportunities or early adversity. The workflow here treats timing as important but not as fate.

