# Continuity, Discontinuity, and the Logic of Developmental Change

This directory is a research-grade, reproducible companion for the article **Continuity, Discontinuity, and the Logic of Developmental Change**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/continuity-discontinuity-and-the-logic-of-developmental-change

## Research purpose

This folder operationalizes the article's central argument: developmental change is not simply continuous or discontinuous. Human development often combines gradual accumulation, nonlinear growth, threshold shifts, logistic transition, institutional rupture, biological maturation, intervention, trauma, and ecological context.

This repository is designed for:

- teaching the difference between continuous growth, nonlinear growth, discontinuity, stage-like shifts, thresholds, and contextual rupture;
- modeling developmental trajectories with gradual change and threshold-sensitive reorganization;
- representing support, chronic stress, school/context support, resource stability, transition readiness, and intervention-like turning points;
- comparing continuous, threshold, and logistic-transition models;
- showing how small continuous processes can produce visible discontinuities;
- showing how institutional rupture or support can redirect developmental pathways;
- documenting ethical limits around ranking, deficit narratives, disability, neurodivergence, culture, trauma, and inequality.

The data are synthetic. Nothing here is a clinical developmental screening tool, school-placement tool, child-risk score, maturity score, disability classification system, trauma prediction tool, or high-stakes decision system.

## Directory map

```text
continuity-discontinuity-and-the-logic-of-developmental-change/
├── c/              C summary utility for generated continuity/discontinuity panel data
├── cpp/            C++ developmental-change summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, framework, reproducibility
├── fortran/        numerical continuity/discontinuity simulation
├── go/             command-line summary and validation utility
├── julia/          continuous and threshold development simulation workflow
├── notebooks/      notebook scaffold and exploratory-analysis notes
├── outputs/        generated summaries, figures, and model outputs
├── python/         synthetic data generator, models, scenarios
├── r/              mixed-effects and trajectory workflow
├── rust/           strict CSV schema validation utility
├── sql/            schema, views, and analytical queries
├── Makefile        reproducible command shortcuts
└── README.md
```

## Quick start

```bash
cd articles/continuity-discontinuity-and-the-logic-of-developmental-change
python3 python/generate_continuity_discontinuity_panel.py
python3 python/model_continuity_discontinuity.py
python3 python/developmental_turning_point_scenarios.py
```

Or:

```bash
make python
make scenarios
make all
```

Optional language checks:

```bash
make c
make cpp
make go
make rust
make julia
make fortran
```

## Model frame

A continuous developmental trajectory can be represented as:

```text
Y_it = alpha_i + beta_i * t + error_it
```

A nonlinear continuous trajectory can be represented as:

```text
Y_it = alpha_i + beta_1i * t + beta_2i * t^2 + error_it
```

A threshold-sensitive transition can be represented as:

```text
Y_it = alpha_i + beta_i * t + gamma_i * I(t >= tau_i) + delta * X_it + error_it
```

A smoother logistic transition can be represented as:

```text
Y_it = alpha_i + beta_i * t + gamma_i / (1 + exp(-k * (t - tau_i))) + delta * X_it + error_it
```

Where:

- `Y_it` = developmental outcome;
- `t` = developmental time;
- `tau_i` = person-specific threshold timing;
- `gamma_i` = transition strength;
- `k` = transition sharpness;
- `X_it` = support, stress, context, intervention, rupture, or resource variables.

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T20:19:46Z`.
