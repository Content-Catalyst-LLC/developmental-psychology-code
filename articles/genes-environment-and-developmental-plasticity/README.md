# Genes, Environment, and Developmental Plasticity

This directory is a research-grade, reproducible companion for the article **Genes, Environment, and Developmental Plasticity**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/genes-environment-and-developmental-plasticity

## Research purpose

This folder operationalizes the article's central argument: human development is not determined by genes alone or imposed by environment alone. It emerges through the dynamic relation among biological sensitivity, environmental exposure, caregiving quality, stress, nutrition, school and neighborhood context, developmental timing, biological embedding, intervention support, and developmental plasticity across time.

This repository is designed for:

- teaching gene-environment interaction as developmental coaction;
- modeling biological sensitivity and environmental exposure over repeated waves;
- representing timing-sensitive exposure and sensitive-period assumptions;
- representing biological embedding through accumulated exposure;
- comparing high-support and high-stress developmental ecologies;
- simulating intervention, nutrition, care, and stress-reduction scenarios;
- providing transparent, reusable research scaffolding.

The data are synthetic. Nothing here is a genetic test, clinical prediction model, child-risk scoring system, diagnosis tool, or high-stakes decision system.

## Directory map

```text
genes-environment-and-developmental-plasticity/
├── c/              C summary utility for generated plasticity panel data
├── cpp/            C++ gene-environment summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, plasticity framework, reproducibility
├── fortran/        numerical gene-environment plasticity simulation
├── go/             command-line summary and validation utility
├── julia/          biological sensitivity and plasticity simulation workflow
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
cd articles/genes-environment-and-developmental-plasticity
python3 python/generate_genes_environment_panel.py
python3 python/model_genes_environment_plasticity.py
python3 python/plasticity_scenario_analysis.py
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

A dynamic gene-environment-plasticity model can be written as:

```text
D_it = rho * D_i,t-1 + beta * G_i + gamma * E_it + delta * (G_i * E_it) + theta * T_it + phi * B_it + u_j + error_it
```

Where:

- `D_it` = developmental outcome for child i at time t
- `G_i` = biological sensitivity or inherited developmental susceptibility
- `E_it` = current environmental exposure
- `G_i * E_it` = gene-environment interaction
- `T_it` = developmental timing or sensitive-period weight
- `B_it` = embedded biological state from accumulated exposure
- `u_j` = shared school, neighborhood, clinic, or policy context

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T18:41:18Z`.
