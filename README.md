# Codex-Temp

Sales Intelligence AI MVP (deterministic, SQL-safe conversational analytics prototype).

## Documents
- [Sales Intelligence AI — Product Requirements Document](docs/sales-intelligence-ai-prd.md)

## Quick Start
1. Initialize data and run a sample chat response:
   ```bash
   python -m app.main
   ```
2. Run tests:
   ```bash
   pytest -q
   ```

## What is implemented
- Synthetic 1000-row multi-country/multi-product sales dataset.
- Read-only NL→SQL query generation (`SELECT` only).
- Deterministic KPI/insight layer from executed query outputs.
- Visualization recommendation engine.
- Session memory, query logging, usage tracking, and tenant-aware filtering.
