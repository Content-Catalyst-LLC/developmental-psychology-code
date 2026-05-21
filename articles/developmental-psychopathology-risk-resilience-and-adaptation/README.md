# Developmental Psychopathology: Risk, Resilience, and Adaptation

This directory is a research-grade, reproducible companion for the article **Developmental Psychopathology: Risk, Resilience, and Adaptation**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/developmental-psychopathology-risk-resilience-and-adaptation

## Research purpose

Developmental psychopathology studies psychological difficulty as a developmental pathway rather than a static label. This folder models how risk, protection, resilience, adaptation, internalizing pathways, externalizing pathways, biological sensitivity, caregiver stability, school belonging, service access, community support, and cumulative exposure interact across repeated developmental waves.

This repository is designed for:

- teaching developmental-pathway concepts;
- demonstrating longitudinal and multilevel research structures;
- modeling cumulative risk and protective support;
- representing multifinality and equifinality;
- comparing adaptation, internalizing, and externalizing pathways;
- showing how protective systems can redirect risk trajectories;
- providing reusable, transparent research scaffolding.

The data are synthetic. Nothing here is a clinical model, diagnostic tool, prediction system, or validated measurement instrument.

## Directory map

```text
developmental-psychopathology-risk-resilience-and-adaptation/
├── c/              C summary utility for generated panel data
├── cpp/            C++ risk-support summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, reproducibility
├── fortran/        numerical developmental-pathway simulation
├── go/             command-line summary and validation utility
├── julia/          risk/resilience simulation workflow
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
cd articles/developmental-psychopathology-risk-resilience-and-adaptation
python3 python/generate_developmental_psychopathology.py
python3 python/model_developmental_psychopathology.py
python3 python/scenario_analysis.py
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

A dynamic developmental-pathway model can be written as:

```text
D_it = rho * D_i,t-1 - beta * K_it + gamma * P_it + delta * C_it + u_j + error_it
```

Where:

- `D_it` = adaptation for child i at time t
- `K_it` = current and cumulative risk
- `P_it` = protective support
- `C_it` = caregiver stability, school belonging, services, community support
- `u_j` = shared context influence

A branching pathway representation is:

```text
{adaptation, internalizing, externalizing} = f(risk, support, regulation, stability, context, timing)
```

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T17:58:38Z`.
