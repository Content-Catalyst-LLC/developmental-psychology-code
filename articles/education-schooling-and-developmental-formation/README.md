# Education, Schooling, and Developmental Formation

This directory is a research-grade, reproducible companion for the article **Education, Schooling, and Developmental Formation**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/education-schooling-and-developmental-formation

## Research purpose

This folder operationalizes the article's central argument: schooling is not merely instructional delivery or academic measurement. It is a developmental institution that shapes cognition, school connectedness, self-regulation, belonging, peer life, authority, stress, identity, opportunity, health, and future orientation.

This repository is designed for:

- teaching schooling as developmental formation;
- modeling school connectedness, teacher support, peer belonging, and school climate;
- representing curriculum opportunity and institutional resources;
- modeling school stress, discipline climate, and restorative-practice exposure;
- comparing support, connectedness, and resource scenarios;
- showing how schools shape development through relationships, routines, curriculum, and opportunity;
- providing transparent, reusable research scaffolding.

The data are synthetic. Nothing here is a causal estimate from real students, a school accountability model, a student prediction system, or a high-stakes educational decision tool.

## Directory map

```text
education-schooling-and-developmental-formation/
├── c/              C summary utility for generated schooling panel data
├── cpp/            C++ school connectedness summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, school-climate framework, reproducibility
├── fortran/        numerical schooling-development simulation
├── go/             command-line summary and validation utility
├── julia/          school connectedness and development simulation workflow
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
cd articles/education-schooling-and-developmental-formation
python3 python/generate_schooling_development_panel.py
python3 python/model_schooling_development.py
python3 python/schooling_scenario_analysis.py
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

A dynamic schooling-development model can be written as:

```text
D_it = rho * D_i,t-1 + beta * T_it + gamma * P_it + delta * C_j + eta * O_j - lambda * R_it + theta * I_it + error_it
```

Where:

- `D_it` = developmental outcome for student i at time t
- `T_it` = teacher support
- `P_it` = peer belonging
- `C_j` = school climate
- `O_j` = curriculum opportunity or institutional resource capacity
- `R_it` = school-related stress
- `I_it` = support/intervention exposure

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T18:20:21Z`.
