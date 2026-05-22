# Social Development Framework

## Core developmental claims

1. Social development is not simply sociability; it is the organization of selfhood through relation.
2. Peer relations create developmental feedback loops involving recognition, belonging, exclusion, and social interpretation.
3. Friendship quality and peer support can stabilize confidence, participation, and self-formation.
4. Chronic exclusion, bullying exposure, and digital comparison can redirect developmental pathways.
5. School connectedness, teacher support, inclusion climate, and restorative practice are developmental infrastructure.
6. Disability, neurodivergence, language, culture, and power shape whose social competence is recognized.
7. Digital peer worlds extend social development into networked visibility, comparison, belonging, and harm.

## Analytical structure

```text
S_it = rho * S_i,t-1 + beta * time + gamma * peer_it + delta * family_it + theta * school_it - lambda * exclusion_it + error_it
```

Where:

- `S_it` = social-self score for person `i` at time `t`;
- `S_i,t-1` = prior social-self score;
- `peer_it` = peer support and friendship quality;
- `family_it` = family support;
- `school_it` = school connectedness and inclusion climate;
- `exclusion_it` = exclusion, bullying, or harmful social comparison.

A digital extension can be represented as:

```text
S_it = rho * S_i,t-1 + gamma * support_it - lambda * exclusion_it - mu * digital_comparison_it + error_it
```

This distinction matters because digital environments can support recognition while also intensifying visibility, comparison, and exclusion.
