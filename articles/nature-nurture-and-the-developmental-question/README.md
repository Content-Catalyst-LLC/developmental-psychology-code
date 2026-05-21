# Nature, Nurture, and the Developmental Question

This directory is a research-grade, reproducible companion for the article **Nature, Nurture, and the Developmental Question**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/nature-nurture-and-the-developmental-question

## Research purpose

This folder operationalizes the article's central argument: the nature-nurture question should no longer be treated as a simple contest between biology and environment. Development unfolds through interaction, timing, feedback, biological embedding, institutional context, inequality, disability support, culture, and history.

This repository is designed for:

- teaching gene-environment interaction and differential susceptibility;
- modeling structural risk, biological sensitivity, caregiver support, acute stress, institutional support, disability support, resource stability, intervention exposure, and developmental outcomes;
- showing how biological sensitivity can amplify both supportive and harmful contexts;
- representing nested school/institutional contexts as developmental environments;
- comparing family-support, institutional-support, disability-support, stress-reduction, resource-stability, intervention, and combined protective-context scenarios;
- documenting ethical limits around genetics, developmental prediction, disability, neurodivergence, inequality, surveillance, and blame.

The data are synthetic. Nothing here is a genetic-risk tool, clinical diagnostic tool, school-placement tool, disability classification system, child-ranking tool, family-risk score, surveillance system, or high-stakes decision system.

## Directory map

```text
nature-nurture-and-the-developmental-question/
├── c/              C summary utility for generated nature-nurture panel data
├── cpp/            C++ gene-environment summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, framework, reproducibility
├── fortran/        numerical gene-environment interaction simulation
├── go/             command-line summary and validation utility
├── julia/          differential susceptibility simulation workflow
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
cd articles/nature-nurture-and-the-developmental-question
python3 python/generate_nature_nurture_panel.py
python3 python/model_nature_nurture_development.py
python3 python/nature_nurture_scenario_analysis.py
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

A simple gene-environment interaction model can be represented as:

```text
Y_it = alpha + beta_G * G_i + beta_E * E_it
       + beta_GE * (G_i x E_it) + error_it
```

A dynamic developmental model can be represented as:

```text
Y_it = rho * Y_i,t-1 + beta_G * G_i + beta_E * E_it
       + beta_GE * (G_i x E_it) + beta_C * C_j + error_it
```

Where:

- `Y_it` = developmental outcome;
- `G_i` = biological sensitivity;
- `E_it` = time-varying environment;
- `G_i x E_it` = differential susceptibility or gene-environment interaction;
- `C_j` = school, clinic, community, or institutional context;
- `rho` = developmental path dependence.

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T20:34:15Z`.
