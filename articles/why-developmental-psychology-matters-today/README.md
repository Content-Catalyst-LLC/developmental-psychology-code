# Why Developmental Psychology Matters Today

This folder provides a reproducible, multi-language research companion for the article **“Why Developmental Psychology Matters Today.”**

The article argues that developmental psychology matters because many contemporary social problems are developmental problems: mental health, early childhood, schooling, inequality, trauma, disability, adolescence, life-course health, aging, and public policy all concern how human beings grow, adapt, participate, and change across time.

This repository translates that argument into a research workflow.

## Research purpose

The code examples model developmental outcomes as dynamic processes shaped by:

- developmental support
- developmental risk
- institutional climate
- policy access
- health status
- context-level resources
- prior developmental state
- cumulative exposure over time

The examples use synthetic data only. They are designed for reproducible demonstration, teaching, and method development, not for clinical diagnosis or policy claims about real populations.

## Directory structure

```text
why-developmental-psychology-matters-today/
├── c/              Low-level CSV summary utility
├── cpp/            C++ developmental trajectory summary utility
├── data/           Synthetic data, schema, and data dictionary
├── docs/           Methods, ethics, reproducibility, and interpretation notes
├── fortran/        Numerical simulation example
├── go/             Command-line summary tool
├── julia/          Dynamic developmental simulation
├── notebooks/      Notebook scaffold and reproducibility notes
├── outputs/        Generated model outputs and figures
├── python/         Main synthetic data generator and dynamic model
├── r/              Mixed-effects modeling workflow
├── rust/           CSV validation and summary utility
├── sql/            Database schema and analytical queries
└── README.md
```

## Quick start

From the root of the repository:

```bash
cd articles/why-developmental-psychology-matters-today

python3 python/generate_developmental_panel.py
python3 python/model_developmental_trajectories.py

Rscript r/model_developmental_conditions.R
```

Optional compiled-language examples:

```bash
gcc c/development_summary.c -o outputs/development_summary_c
./outputs/development_summary_c data/developmental_panel.csv

g++ -std=c++17 cpp/development_summary.cpp -o outputs/development_summary_cpp
./outputs/development_summary_cpp data/developmental_panel.csv

gfortran fortran/life_course_simulation.f90 -o outputs/life_course_simulation_fortran
./outputs/life_course_simulation_fortran

go run go/development_summary.go data/developmental_panel.csv

rustc rust/validate_developmental_panel.rs -o outputs/validate_developmental_panel_rust
./outputs/validate_developmental_panel_rust data/developmental_panel.csv

julia julia/simulate_life_course.jl
```

## Core analytical model

A stylized developmental outcome for person \(i\) at time \(t\) can be written as:

\[
D_{it} = \rho D_{i,t-1} + \beta S_{it} - \gamma R_{it} + \delta P_{it} + \theta C_{jt} + \eta_i + \varepsilon_{it}
\]

where:

- \(D_{it}\) is a developmental outcome score
- \(D_{i,t-1}\) is the prior developmental state
- \(S_{it}\) is developmental support
- \(R_{it}\) is developmental risk
- \(P_{it}\) is policy or service access
- \(C_{jt}\) is contextual or institutional climate
- \(\eta_i\) captures person-level heterogeneity
- \(\varepsilon_{it}\) is residual variation

## Ethical note

The synthetic score in this repository is not a diagnostic scale. It is a teaching and modeling construct. Real developmental research requires validated measures, careful sampling, informed consent, privacy protection, domain expertise, institutional review when appropriate, and strong safeguards against stigmatizing individuals or groups.

