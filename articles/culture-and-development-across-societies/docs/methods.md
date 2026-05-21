# Methods Note

## Why this workflow exists

The article argues that culture organizes development through family practices, institutional fit, language, social support, moral worlds, migration, and cross-context negotiation. A suitable workflow therefore needs nested data: repeated observations within children, children within societies or cultural settings, and cultural conditions that change over time.

## Conceptual variables

| Variable | Meaning |
|---|---|
| `child_id` | Unique synthetic child identifier |
| `society_id` | Synthetic cultural, social, or institutional context |
| `time` | Repeated developmental observation wave |
| `family_orientation` | Baseline family cultural orientation or home-context support |
| `institutional_fit` | Baseline fit between child/family and institutional setting |
| `cross_context_mismatch` | Baseline tension between home and school/host setting |
| `social_support` | Baseline support from family, peers, school, or community |
| `bicultural_flexibility` | Capacity to navigate multiple cultural contexts |
| `society_climate` | Context-level cultural-development climate |
| `institutional_inclusion` | Context-level inclusion or recognition |
| `linguistic_support` | Context-level support for language continuity and multilingual development |
| `current_family` | Time-varying family/home support |
| `current_fit` | Time-varying institutional fit |
| `current_mismatch` | Time-varying cross-context mismatch |
| `current_support` | Time-varying social support |
| `current_flexibility` | Time-varying bicultural flexibility |
| `development_score` | Synthetic developmental outcome |

## Modeling logic

The workflow represents cultural development as:

1. nested, because children develop within societies, schools, families, and institutions;
2. dynamic, because prior developmental state influences later developmental state;
3. relational, because support, fit, mismatch, and recognition matter;
4. culturally valid, because constructs should not be assumed to mean the same thing everywhere;
5. non-ranking, because the goal is to model developmental conditions, not to rank cultures.

