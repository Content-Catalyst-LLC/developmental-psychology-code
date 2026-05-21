# Gender Development and Sexual Development

This directory is a research-grade, reproducible companion for the article **Gender Development and Sexual Development**.

GitHub article folder:  
https://github.com/Content-Catalyst-LLC/developmental-psychology-code/tree/main/articles/gender-development-and-sexual-development

## Research purpose

This folder operationalizes the article's central argument: gender development and sexual development are related but distinct developmental processes. Gender development concerns gender categories, gendered norms, identity, expression, social recognition, and the meanings attached to the body in family, peer, cultural, and institutional life. Sexual development concerns puberty, bodily maturation, attraction, sexual knowledge, consent, relationships, sexual health, and sexual self-understanding.

This repository is designed for:

- teaching the distinction between gender development, sex development, sexual development, sexual orientation, and adolescent adjustment;
- modeling pubertal progression, family support, social recognition, consent knowledge, school connectedness, health education quality, anti-harassment support, stigma exposure, and protective context;
- representing support, recognition, knowledge, and safety as developmental protections;
- modeling stigma, exclusion, misinformation, and coercive pressure as contextual risks;
- comparing family support, school connectedness, consent education, anti-harassment support, stigma reduction, health-service access, and combined support scenarios;
- showing how healthy development depends on support, safety, accurate information, dignity, and care rather than silence, stigma, coercion, or shame;
- providing transparent, reusable research scaffolding.

The data are synthetic. Nothing here is a clinical diagnostic tool, sexuality assessment tool, gender identity screening tool, school discipline tool, student surveillance system, mental-health prediction system, or high-stakes decision system.

## Directory map

```text
gender-development-and-sexual-development/
├── c/              C summary utility for generated adolescent-development panel data
├── cpp/            C++ adolescent-development summary utility
├── data/           data dictionary and generated synthetic datasets
├── docs/           research notes, methods, ethics, framework, reproducibility
├── fortran/        numerical support/stigma/protective-context simulation
├── go/             command-line summary and validation utility
├── julia/          gender/sexual-development simulation workflow
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
cd articles/gender-development-and-sexual-development
python3 python/generate_gender_sexual_development_panel.py
python3 python/model_gender_sexual_development.py
python3 python/gender_sexual_development_scenario_analysis.py
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

A dynamic adolescent-development model can be written as:

```text
A_it = rho * A_i,t-1 + beta_P * P_it + beta_F * F_it
       + beta_R * R_it + beta_K * K_it + beta_C * C_it
       + beta_E * E_j + beta_H * H_j - beta_S * S_it
       + beta_B * (S_it x protective_context_it) + u_j + error_it
```

Where:

- `A_it` = broad adolescent adjustment, belonging, or developmental well-being outcome
- `P_it` = pubertal progression or embodied developmental timing
- `F_it` = family support
- `R_it` = social recognition
- `K_it` = consent knowledge and sexual-health literacy
- `C_it` = school connectedness
- `E_j` = health education quality
- `H_j` = anti-harassment support
- `S_it` = stigma, exclusion, misinformation, coercive pressure, or unsafe social sanction
- `u_j` = school, family, community, clinic, or peer-context influence

## Updated

Full research-grade directory upgrade written at UTC: `2026-05-21T19:58:35Z`.
