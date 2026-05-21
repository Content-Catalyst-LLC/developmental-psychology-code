# Parenting, Family Systems, and Human Development

This directory is a research-grade, reproducible companion for the article **Parenting, Family Systems, and Human Development**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/parenting-family-systems-and-human-development

## Research purpose

This folder operationalizes the article's central argument: parenting and family systems are not background influences on development. They are relational developmental systems through which children learn regulation, attachment, communication, conflict, repair, responsibility, identity, trust, and participation in shared life.

This repository is designed for:

- teaching parenting as a developmental relationship rather than an isolated technique;
- modeling family systems as nested relational ecologies;
- representing parenting responsiveness, family climate, household stability, kin support, sibling support, and stress;
- modeling caregiver support and family-system intervention scenarios;
- showing how child development is shaped by recurring relational patterns;
- providing transparent, reusable research scaffolding.

The data are synthetic. Nothing here is a clinical parenting assessment, custody tool, family-risk prediction system, or high-stakes decision model.

## Directory map

```text
parenting-family-systems-and-human-development/
├── c/              C summary utility for generated family-systems panel data
├── cpp/            C++ family-support summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, family-systems framework, reproducibility
├── fortran/        numerical family-systems development simulation
├── go/             command-line summary and validation utility
├── julia/          parenting and family-systems simulation workflow
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
cd articles/parenting-family-systems-and-human-development
python3 python/generate_family_systems_panel.py
python3 python/model_family_systems.py
python3 python/family_support_scenario_analysis.py
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

A dynamic family-systems development model can be written as:

```text
D_it = rho * D_i,t-1 + beta * P_it + gamma * F_it + delta * H_j + eta * K_j - lambda * S_it + theta * I_it + error_it
```

Where:

- `D_it` = developmental outcome for child i at time t
- `P_it` = parenting responsiveness
- `F_it` = family climate
- `H_j` = household stability
- `K_j` = kin support or extended-family support
- `S_it` = stress burden
- `I_it` = caregiver support, family support, or intervention exposure

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T18:32:28Z`.
