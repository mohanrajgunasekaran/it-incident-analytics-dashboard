# 📊 IT Incident Analytics Dashboard

An interactive portfolio dashboard for incident trends, restoration performance, SLA risk, and recurring causes.

> **Synthetic data only.** The included records are generated for demonstration and do not represent any employer, customer, or production environment.

## Features
- KPI cards: incident volume, P1/P2 count, resolved-only SLA breach rate, and MTTR
- Date, priority, service, and status filters
- Incident trends, priority mix, MTTR by priority, SLA breach rate by service, root-cause analysis
- Filtered CSV export
- Synthetic data generator, SQL examples, and unit tests for core metric behaviour

## Stack
Python · Pandas · Streamlit · Plotly · SQL · pytest

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
```
Windows PowerShell: `\.venv\Scripts\Activate.ps1`  
Linux/macOS: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
streamlit run app.py
```
Regenerate the synthetic dataset with `python generate_data.py`. Run metric tests with `pytest -q`.

## SQL examples
See [`sql/analysis_queries.sql`](sql/analysis_queries.sql) for incident counts by priority, MTTR by priority, SLA breach rates by service, and root-cause frequency. The examples expect a SQLite table named `incidents` populated from the CSV.

## Metric definitions
- **MTTR:** average elapsed time between creation and resolution for resolved incidents only.
- **SLA breach rate:** resolved incidents exceeding the illustrative target divided by all resolved incidents in the selected view.
- **P1/P2:** combined count of records classified as P1 or P2.

SLA targets are demonstration assumptions, not any organisation's actual policy. Synthetic patterns are not evidence of real operational performance.

## Structure
```text
app.py
generate_data.py
requirements.txt
README.md
data/incidents.csv
sql/analysis_queries.sql
tests/test_metrics.py
```

## Roadmap
Add SQLite-backed dashboard mode, data-quality checks, GitHub Actions CI, screenshots, and a hosted demo.

## Responsible use
Never publish confidential incident notes, customer names, internal ticket IDs, IP addresses, hostnames, or production details. Use synthetic or approved anonymised data only.
