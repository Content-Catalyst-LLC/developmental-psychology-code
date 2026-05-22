# Language Development Framework

## Core developmental claims

1. Language development is not only vocabulary growth or grammar acquisition; it is the social formation of speech and communication.
2. Language begins before fluent words through sound, rhythm, gesture, gaze, turn-taking, and shared attention.
3. Responsive interaction, joint attention, conversational turn-taking, reading, storytelling, and singing shape language growth.
4. Hearing, speech production, gesture, sign, AAC, and embodied communication all matter.
5. Multilingual development is a normal human condition, not a developmental deficit.
6. Home-language recognition and institutional respect shape language opportunity.
7. Chronic stress and unequal access to books, healthcare, early education, and hearing support can shape language trajectories.
8. Communication difference should not be equated with absence of meaning.

## Analytical structure

A general language-growth trajectory can be represented as:

```text
L_it = rho * L_i,t-1 + beta * time + gamma * interaction_it + theta * support_it - lambda * stress_it + error_it
```

Where:

- `L_it` = language-development outcome for child `i` at time `t`;
- `L_i,t-1` = prior language status;
- `interaction_it` = responsive interaction, joint attention, turn-taking, or shared reading;
- `support_it` = hearing support, books, early education, or language ecology support;
- `stress_it` = acute stress, chronic stress, instability, or language-opportunity constraint.

A differentiated language ecology model can separate language forms:

```text
L_it = alpha_i + beta_1 * interaction_it + beta_2 * reading_it + beta_3 * joint_attention_it + beta_4 * turn_taking_it + beta_5 * hearing_support_i + error_it
```

A multilingual ecology model can represent institutional recognition:

```text
L_it = alpha_i + beta * time + gamma * multilingual_exposure_i + theta * home_language_recognition_j + eta * multilingual_exposure_i * home_language_recognition_j + error_it
```

This captures the idea that multilingual exposure is shaped by whether institutions support or devalue the child's home language.
