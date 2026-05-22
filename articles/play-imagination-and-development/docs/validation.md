# Validation

## Repository validation checks

- Rust validates expected CSV columns.
- C, C++, and Go summarize key variables.
- Python and R generate trajectory summaries and plots.
- SQL provides schema and analytical views.

## Suggested workflow

```bash
make python
make scenarios
make rust
make go
```

## Quality checks

Inspect row counts, unique child counts, unique context counts, missing values, plausible ranges, profile distributions, play trajectory shape, support/restriction gradients, stress gradients, and context-level play ecology summaries.
