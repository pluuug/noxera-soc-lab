# NØXERA SOC Lab — Demo Walkthrough

## 1. Run the sample

```bash
python src/analyze_auth_logs.py --input data/auth.log --output reports/alerts.json --threshold 5 --window-minutes 10
```

## 2. Inspect the JSON report

Open `reports/alerts.json` and look at each alert's `rule_id`, `severity`, `source_ip`, `evidence`, and `recommended_triage` fields. The bundled sample is designed to demonstrate repeated failures and a subsequent successful login. It uses reserved documentation IP addresses, not real attack infrastructure.

## 3. Run the tests

```bash
python -m unittest discover -s tests -v
```

## Suggested screenshots for a portfolio

Capture your own terminal after running the command and the test suite. Make sure the screenshot shows the command and successful output, and does not include personal file paths, tokens, or unrelated private information. Add the screenshots to a `docs/images/` folder and link them from the README only after verifying they contain no sensitive details.
