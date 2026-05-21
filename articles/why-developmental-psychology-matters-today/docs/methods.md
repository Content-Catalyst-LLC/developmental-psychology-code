# Methods Note

## Why this workflow exists

The article argues that developmental psychology is necessary because many contemporary problems unfold across time. A research workflow should therefore avoid static, one-time snapshots whenever possible.

This folder models development using synthetic longitudinal data. Each simulated person is observed across repeated waves and nested within a context such as a school, neighborhood, clinic, service environment, workplace, care system, or community.

## Conceptual variables

| Variable | Meaning |
|---|---|
| `person_id` | Unique person identifier |
| `context_id` | Shared institutional or environmental context |
| `time` | Repeated observation wave |
| `current_support` | Current support conditions |
| `current_risk` | Current risk burden |
| `policy_access` | Access to policy, institutional, or service support |
| `health_status` | General health-related condition |
| `institutional_climate` | Context-level relational and institutional quality |
| `resource_level` | Context-level resource condition |
| `development_score` | Synthetic developmental outcome |

## Modeling logic

The examples model development as:

1. dynamic, because prior state influences later state;
2. contextual, because people are nested within institutions and environments;
3. cumulative, because repeated exposure to risk and support matters;
4. modifiable, because support, policy, and institutional conditions can change trajectories.

## Interpretation standards

The models should be interpreted as demonstrations of structure, not empirical findings. Coefficients are generated from synthetic assumptions and therefore should not be treated as estimates of real-world causal effects.

