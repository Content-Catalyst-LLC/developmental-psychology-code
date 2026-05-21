# Methods Note

## Why this workflow exists

Critical-period and sensitive-period ideas are timing theories. They ask not only whether an experience matters, but when it matters most. This workflow therefore simulates repeated observations over developmental time.

## Conceptual variables

| Variable | Meaning |
|---|---|
| `person_id` | Unique synthetic person identifier |
| `context_id` | Context identifier such as school, family, care system, clinic, or community |
| `time` | Developmental time step |
| `experience` | Environmental input, enrichment, deprivation, support, or exposure |
| `support` | Positive developmental support |
| `adversity` | Negative developmental exposure |
| `critical_weight` | Binary timing weight for a strict critical-period window |
| `early_sensitive_weight` | Smooth timing weight centered in early development |
| `adolescent_sensitive_weight` | Smooth timing weight centered in adolescence |
| `cumulative_weighted_exposure` | Accumulated timing-weighted experience |
| `critical_outcome` | Simulated outcome under a critical-period model |
| `sensitive_outcome` | Simulated outcome under a sensitive-period model |
| `multi_window_outcome` | Simulated outcome with early and adolescent sensitivity windows |
| `recovery_outcome` | Simulated outcome including later intervention and residual plasticity |

## Modeling logic

The workflow compares four timing assumptions:

1. **No timing effect:** experience has roughly the same influence across time.
2. **Critical-period effect:** experience matters mostly inside a narrow window.
3. **Sensitive-period effect:** experience matters most around a peak but remains partially influential outside it.
4. **Multi-window effect:** more than one developmental phase may be unusually responsive.

## Interpretation standards

The models are synthetic demonstrations. They show the structure of timing hypotheses but do not estimate real critical or sensitive periods for any actual population or domain.

