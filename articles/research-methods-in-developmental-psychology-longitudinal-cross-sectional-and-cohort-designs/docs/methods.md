# Methods Note

## Why this workflow exists

Developmental psychology studies change across time, but not every design can directly observe change. This workflow demonstrates the inferential differences among cross-sectional, longitudinal, cohort, and cohort-sequential designs using synthetic data.

## Design types

| Design | Main strength | Main limitation |
|---|---|---|
| Cross-sectional | Efficient age comparison | Confounds age and cohort |
| Longitudinal | Direct within-person change | Attrition, cost, period effects |
| Cohort design | Historical comparison | Cohort differences may not equal development |
| Cohort-sequential | Efficient age-span coverage | More complex design and modeling |

## Conceptual variables

| Variable | Meaning |
|---|---|
| `person_id` | Unique synthetic participant identifier |
| `context_id` | Shared developmental context |
| `birth_cohort` | Synthetic birth cohort group |
| `study_wave` | Observation wave |
| `age` | Participant age at observation |
| `period` | Historical or study period |
| `support` | Positive developmental support |
| `risk` | Developmental risk exposure |
| `context_quality` | Shared context-level support |
| `development_score` | Synthetic developmental outcome |
| `observed` | Missingness / retention indicator |

## Design logic

The workflow simulates a developmental outcome as a function of:

1. age-related developmental change;
2. cohort differences;
3. period effects;
4. context-level clustering;
5. support and risk;
6. missingness due to attrition.

The purpose is to show why research design matters for interpretation.

