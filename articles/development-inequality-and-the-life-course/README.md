# Development, Inequality, and the Life Course

This folder is a reproducible, multi-language research companion for **“Development, Inequality, and the Life Course.”**

GitHub article folder:  
<https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/development-inequality-and-the-life-course>

The article argues that developmental inequality is cumulative: access to safety, nutrition, health care, schooling, housing, family time, institutional support, environmental quality, and opportunities for repair are unequally distributed across the life course.

## What this workflow models

- cumulative advantage and cumulative disadvantage
- unequal exposure to resources and burdens
- early timing sensitivity
- transition-period support
- community opportunity
- institutional support
- environmental safety
- support buffering
- context-level clustering
- dynamic developmental pathways

Synthetic data only. Nothing here is a real clinical, educational, or policy measure.

## Structure

```text
development-inequality-and-the-life-course/
├── c/              C CSV summary utility
├── cpp/            C++ CSV summary utility
├── data/           synthetic data, metadata, dictionaries
├── docs/           methods, ethics, reproducibility, runbook
├── fortran/        numerical life-course simulation
├── go/             command-line summary utility
├── julia/          cumulative inequality simulation
├── notebooks/      notebook scaffold
├── outputs/        generated summaries and plots
├── python/         data generation and models
├── r/              mixed-effects modeling workflow
├── rust/           CSV validation utility
├── sql/            schema and analysis queries
└── Makefile
```

## Quick start

```bash
cd articles/development-inequality-and-the-life-course
make python
make r
```

## Optional checks

```bash
make c
make cpp
make go
make rust
make julia
make fortran
```

## Core model

```text
D_it = rho * D_i,t-1 + beta * R_it - gamma * U_it + delta * S_it + context_j + error_it
```

Where:

- `D_it` = developmental outcome
- `R_it` = resource access
- `U_it` = unequal burden
- `S_it` = support or buffering
- `context_j` = community/institutional context

