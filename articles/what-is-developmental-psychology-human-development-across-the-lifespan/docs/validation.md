# Validation

## Repository validation checks

The folder includes validation and summary utilities in multiple languages:

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

Analysts should inspect:

- row counts;
- unique child counts;
- unique school counts;
- missing values;
- plausible ranges;
- profile distributions;
- trajectory shape;
- intervention timing;
- support and risk gradients.
