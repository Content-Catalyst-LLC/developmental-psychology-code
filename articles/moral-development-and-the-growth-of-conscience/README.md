# Moral Development and the Growth of Conscience

Professional companion repository for the article **Moral Development and the Growth of Conscience**.

GitHub folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/moral-development-and-the-growth-of-conscience

## Purpose

This distribution package provides reproducible synthetic-data workflows for studying moral development as a longitudinal process shaped by conscience formation, caregiving guidance, empathy, peer fairness, self-regulation, restorative repair, school moral climate, punitive inconsistency, anti-bullying climate, exclusion, digital moral context, and moral action under social pressure.

## Scope

The workflow is designed for research education, methodological demonstration, teaching, and extension into validated empirical studies. It models moral development as a trajectory rather than a fixed trait: conscience grows through emotion, relationship, practice, institutional fairness, peer worlds, repair, and moral action under pressure.

## Repository structure

```text
moral-development-and-the-growth-of-conscience/
├── c/              C summary utility
├── cpp/            C++ summary utility
├── data/           Data dictionary and generated synthetic panels
├── docs/           Methods, framework, validation, reproducibility, responsible use
├── fortran/        Numerical simulation
├── go/             Command-line summary utility
├── julia/          Moral-development simulation
├── notebooks/      Notebook scaffold
├── outputs/        Generated summaries, tables, and figures
├── python/         Synthetic data, models, and scenarios
├── r/              Mixed-effects moral-development modeling
├── rust/           CSV schema validation utility
├── sql/            Schema and analytical queries
├── Makefile        Reproducible workflow commands
└── README.md
```

## Quick start

```bash
cd articles/moral-development-and-the-growth-of-conscience
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

The generated datasets are synthetic. They are structured to make moral-development reasoning inspectable: conscience trajectories, peer fairness, empathy, restorative repair, punitive inconsistency, school moral climate, exclusion, digital context, and moral action under peer pressure are represented explicitly.

## Updated

2026-05-22T02:11:24Z
