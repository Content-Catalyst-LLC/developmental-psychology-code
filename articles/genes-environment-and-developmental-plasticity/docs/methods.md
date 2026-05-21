# Methods

## Overview

This workflow models genes, environment, and developmental plasticity as a longitudinal developmental system. The synthetic data include children nested within contexts and observed repeatedly across time.

The model includes:

- biological sensitivity;
- caregiving quality;
- environmental stress;
- nutritional support;
- early exposure;
- intervention support;
- school support;
- neighborhood safety;
- service access;
- timing-sensitive exposure;
- weighted stress and support;
- embedded stress and embedded support;
- developmental outcome;
- sensitivity-stress profile.

## Conceptual interpretation

### Biological sensitivity

`bio_sensitivity` is not treated as fate. It represents biological susceptibility or responsiveness to conditions.

### Environment

The model includes multiple environmental dimensions: care, stress, nutrition, school support, neighborhood safety, and service access.

### Timing

`timing_weight` represents the idea that early or developmentally sensitive periods can carry different exposure weights.

### Biological embedding

`embedded_stress` and `embedded_support` summarize accumulated timing-weighted exposures carried forward across waves.

### Plasticity

Plasticity is represented through timing, interaction terms, and scenario differences. It means conditional developmental responsiveness, not unlimited reversibility.

## Synthetic-data caution

The data are not empirical findings. They are simulated for reproducible demonstration only.
