# Framework

## Core developmental claims

1. Brain development is central to developmental psychology because perception, movement, attention, memory, emotion, language, regulation, and learning are embodied in the nervous system.
2. Neural development is structured but plastic.
3. Plasticity is real but bounded by timing, prior organization, biology, context, and support.
4. Early development matters intensely, but later development remains possible.
5. Caregiving, learning, sleep, nutrition, safety, sensory regulation, and health access are neurodevelopmental conditions.
6. Stress and trauma shape nervous-system development, but relational buffering and supportive environments can redirect pathways.
7. Neurodivergence and disability require support, accommodation, and respectful interpretation, not deficit-only reduction.

## Model sketch

```text
N_it = rho * N_i,t-1 + gamma_1 * learning_it + gamma_2 * care_it + gamma_3 * sleep_it - gamma_4 * stress_it - gamma_5 * environmental_risk_j + error_it

Y_it = beta_1 * N_it + beta_2 * support_it - beta_3 * stress_it + error_it
```

Where `N_it` is neural state and `Y_it` is developmental functioning.
