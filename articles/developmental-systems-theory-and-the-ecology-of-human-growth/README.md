# Developmental Systems Theory and the Ecology of Human Growth

This directory is a research-grade, reproducible companion for the article **Developmental Systems Theory and the Ecology of Human Growth**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/developmental-systems-theory-and-the-ecology-of-human-growth

## Research purpose

This folder operationalizes the article's central argument: human development is not produced by isolated genes, private traits, fixed stages, or external environments acting alone. Development emerges through reciprocal, nested, embodied, historical, and relational systems involving biology, family, peers, schools, neighborhoods, institutions, culture, material conditions, and time.

This repository is designed for:

- teaching developmental systems theory as a relational and ecological framework;
- modeling nested contexts such as family, school, neighborhood, service access, and material conditions;
- representing reciprocal person-context development and path dependence;
- modeling ecological support, ecological stress, intervention exposure, and developmental plasticity;
- comparing family, school, neighborhood, and combined support scenarios;
- showing how nested developmental systems can be represented computationally without reducing human development to a single level;
- providing transparent, reusable research scaffolding.

The data are synthetic. Nothing here is a clinical model, child-risk scoring system, school accountability tool, genetic explanation, or high-stakes decision system.

## Directory map

```text
developmental-systems-theory-and-the-ecology-of-human-growth/
├── c/              C summary utility for generated developmental systems panel data
├── cpp/            C++ ecological-development summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, systems framework, reproducibility
├── fortran/        numerical developmental-systems simulation
├── go/             command-line summary and validation utility
├── julia/          nested ecological systems simulation workflow
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
cd articles/developmental-systems-theory-and-the-ecology-of-human-growth
python3 python/generate_developmental_systems_panel.py
python3 python/model_developmental_systems.py
python3 python/systems_scenario_analysis.py
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

A dynamic developmental-systems model can be written as:

```text
D_it = rho * D_i,t-1 + beta * B_it + gamma * R_it + delta * E_it + theta * I_it + u_j + error_it
```

Where:

- `D_it` = developmental outcome for child i at time t
- `B_it` = biological sensitivity or embodied developmental state
- `R_it` = relational experience such as family support and peer belonging
- `E_it` = ecological context such as school climate, neighborhood safety, service access, and material security
- `I_it` = intervention or support exposure
- `u_j` = shared contextual influence such as school or neighborhood clustering

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T18:49:24Z`.
