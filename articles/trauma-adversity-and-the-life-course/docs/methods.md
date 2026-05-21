# Methods Note

## Why this workflow exists

The article argues that trauma and adversity are developmental processes shaped by timing, accumulation, support, context, embodiment, and institutional response. A suitable workflow therefore needs repeated observations, timing weights, cumulative exposure, protective conditions, and multilevel contexts.

## Conceptual variables

| Variable | Meaning |
|---|---|
| `child_id` | Unique synthetic child identifier |
| `context_id` | Shared developmental context such as school, neighborhood, clinic, or service ecology |
| `time` | Repeated developmental observation wave |
| `adversity_burden` | Baseline adversity burden tendency |
| `caregiver_support` | Baseline caregiver or relational support tendency |
| `contextual_stability` | Baseline stability tendency |
| `baseline_health` | Baseline health-related condition |
| `child_resilience` | Synthetic person-level adaptation tendency |
| `community_buffer` | Context-level buffering capacity |
| `institutional_safety` | Context-level trauma-informed institutional safety |
| `service_access` | Context-level access to care or support services |
| `current_adversity` | Time-varying adversity burden |
| `current_support` | Time-varying support |
| `current_stability` | Time-varying contextual stability |
| `early_timing_weight` | Higher weight for earlier developmental exposure |
| `transition_weight` | Weight for transition/recovery opportunity |
| `cumulative_adversity` | Cumulative timing-weighted adversity |
| `cumulative_support` | Cumulative support exposure |
| `adaptation_score` | Synthetic adaptation outcome |
| `adversity_support_profile` | Profile grouping based on average adversity and support |

## Modeling logic

The workflow represents trauma/adversity as:

1. cumulative, because repeated burden matters;
2. timing-sensitive, because exposures may differ by developmental period;
3. relational, because support and caregiving buffer risk;
4. institutional, because schools, services, and communities shape recovery;
5. dynamic, because prior adaptation influences later adaptation.

