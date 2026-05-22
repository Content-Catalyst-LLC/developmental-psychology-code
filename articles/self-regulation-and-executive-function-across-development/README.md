# Self-Regulation and Executive Function Across Development

Professional companion repository for the article **Self-Regulation and Executive Function Across Development**.

GitHub folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/self-regulation-and-executive-function-across-development

## Purpose

This distribution package provides reproducible synthetic-data workflows for studying self-regulation and executive function as longitudinal developmental capacities shaped by caregiving support, classroom structure, sleep quality, school climate, regulation scaffolding, disability accommodation, intervention exposure, chronic stress, acute stress, temperament reactivity, and environmental fit.

The repository translates the article's developmental framework into executable examples that model:

- attention, inhibition, working memory, flexibility, and broad regulation;
- external support, co-regulation, and internal control;
- stress physiology and contextual overload;
- sleep, classroom structure, and school scaffolding;
- disability support need and accommodation;
- intervention exposure and regulatory-support scenarios;
- state dependence in regulation across repeated waves;
- multilevel school/context effects.

## Scope

The workflows are designed for research education, methodological demonstration, teaching, and extension into validated empirical studies. The synthetic data make developmental assumptions inspectable so analysts can adapt parameters, compare scenarios, and build more formal models of executive function and self-regulation across development.

## Repository structure

```text
self-regulation-and-executive-function-across-development/
├── c/              C summary utility
├── cpp/            C++ summary utility
├── data/           Data dictionary and generated synthetic panels
├── docs/           Methods, framework, model card, validation, reproducibility
├── fortran/        Numerical simulation
├── go/             Command-line summary utility
├── julia/          Regulation simulation
├── notebooks/      Notebook scaffold
├── outputs/        Generated summaries, tables, and figures
├── python/         Synthetic data, models, and scenarios
├── r/              Mixed-effects regulation modeling
├── rust/           CSV schema validation utility
├── sql/            Schema and analytical queries
├── Makefile        Reproducible workflow commands
└── README.md
```

## Quick start

```bash
cd articles/self-regulation-and-executive-function-across-development
make python
make scenarios
```

Optional checks:

```bash
make r
make c
make cpp
make go
make rust
make julia
make fortran
```

## Data notes

The generated datasets are synthetic. They are structured to make self-regulation reasoning inspectable: caregiving support, classroom structure, sleep quality, school scaffolding, disability accommodation, stress, intervention exposure, regulatory support context, and regulation trajectories are represented explicitly.

## Updated

2026-05-22T02:39:57Z
