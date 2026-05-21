# Python Workflow

This folder contains the main reproducible workflow.

## Scripts

- `generate_adult_development_panel.py` creates the synthetic adult-development panel.
- `model_adult_development.py` estimates adjustment, role-burden, and health-burden models.
- `adult_development_scenario_analysis.py` compares relational-support, work-integration, adaptive-resource, institutional/community, health-burden, role-burden, and combined-support scenarios.

Run:

```bash
python3 python/generate_adult_development_panel.py
python3 python/model_adult_development.py
python3 python/adult_development_scenario_analysis.py
```
