# Disability, Neurodivergence, and Development

This directory is a research-grade, reproducible companion for the article **Disability, Neurodivergence, and Development**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/disability-neurodivergence-and-development

## Research purpose

This folder operationalizes the article's central argument: disability and neurodivergence are not departures from development, but part of human development itself. Developmental outcomes are modeled as the relation among profile, support, accessibility, barrier burden, participation, communication access, sensory flexibility, caregiver advocacy, and institutional climate over time.

This repository is designed for:

- teaching disability and neurodivergence as developmental relations;
- modeling support, access, barriers, and participation;
- representing person-environment fit;
- comparing high-access and high-barrier settings;
- simulating communication access and assistive-technology scenarios;
- showing how institutions can enable or disable development;
- providing transparent, reusable research scaffolding.

The data are synthetic. Nothing here is a diagnostic model, clinical assessment, eligibility tool, or policy prediction system.

## Directory map

```text
disability-neurodivergence-and-development/
├── c/              C summary utility for generated accessibility panel data
├── cpp/            C++ access/barrier summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, accessibility, reproducibility
├── fortran/        numerical access-barrier development simulation
├── go/             command-line summary and validation utility
├── julia/          accessibility and participation simulation workflow
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
cd articles/disability-neurodivergence-and-development
python3 python/generate_disability_neurodivergence_panel.py
python3 python/model_disability_neurodivergence.py
python3 python/access_scenario_analysis.py
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

A dynamic person-environment development model can be written as:

```text
D_it = rho * D_i,t-1 + beta * N_i + gamma * S_it + delta * A_it - lambda * B_it + eta * P_it + u_j + error_it
```

Where:

- `D_it` = developmental outcome for child i at time t
- `N_i` = disability-related or neurodevelopmental profile
- `S_it` = support quality
- `A_it` = accessibility and accommodation
- `B_it` = barrier burden
- `P_it` = meaningful participation
- `u_j` = shared setting or institutional influence

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T18:09:44Z`.
