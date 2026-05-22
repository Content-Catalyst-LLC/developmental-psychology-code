# Social Development, Peer Relations, and the Formation of the Self

Professional companion repository for the article **Social Development, Peer Relations, and the Formation of the Self**.

GitHub folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/social-development-peer-relations-and-the-formation-of-the-self

## Purpose

This distribution package provides reproducible synthetic-data workflows for studying social development as a longitudinal process shaped by peer relations, friendship quality, family support, school connectedness, teacher support, inclusion climate, restorative practice, exclusion, bullying exposure, digital comparison, and the formation of the social self.

The repository translates the article's developmental framework into executable examples that model:

- peer support, friendship quality, and social connectedness;
- chronic exclusion, bullying exposure, digital comparison, and social risk;
- school connectedness, teacher support, inclusion climate, and restorative practice;
- social-self formation through recognition, belonging, conflict, and misrecognition;
- state dependence in social confidence and social adaptation;
- multilevel school/context effects;
- scenario comparisons for peer support, inclusion, anti-bullying, restorative practice, digital safety, and combined protective context.

## Scope

The workflows are designed for research education, methodological demonstration, teaching, and extension into validated empirical studies. The synthetic data make developmental assumptions inspectable so analysts can adapt parameters, compare scenarios, and build more formal models of peer relations and self-formation.

## Repository structure

```text
social-development-peer-relations-and-the-formation-of-the-self/
├── c/              C summary utility
├── cpp/            C++ summary utility
├── data/           Data dictionary and generated synthetic panels
├── docs/           Methods, framework, validation, reproducibility, responsible use
├── fortran/        Numerical simulation
├── go/             Command-line summary utility
├── julia/          Social-development simulation
├── notebooks/      Notebook scaffold
├── outputs/        Generated summaries, tables, and figures
├── python/         Synthetic data, models, and scenarios
├── r/              Mixed-effects social-development modeling
├── rust/           CSV schema validation utility
├── sql/            Schema and analytical queries
├── Makefile        Reproducible workflow commands
└── README.md
```

## Quick start

```bash
cd articles/social-development-peer-relations-and-the-formation-of-the-self
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

The generated datasets are synthetic. They are structured to make social-development reasoning inspectable: peer support, friendship quality, family support, school connectedness, teacher support, inclusion climate, restorative practice, exclusion, bullying, digital comparison, and social-self outcomes are represented explicitly.

## Updated

2026-05-22T02:29:54Z
