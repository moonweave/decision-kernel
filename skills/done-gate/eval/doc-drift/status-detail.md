# Scorecard Detail

Last updated after Phase 2 merge.

## Test results

- Unit tests: 48 / 48 passing
- Integration tests: 5 / 8 passing
  - `test_multi_host_merge` — FAIL (Phase 3 not landed)
  - `test_aggregated_view` — FAIL (Phase 3 not landed)
  - `test_schema_round_trip` — FAIL (regression introduced in latest schema patch)

## Lint

Clean.

## Score breakdown

| Domain | Points earned | Points available |
|---|---|---|
| Unit tests | 40 | 40 |
| Integration tests | 25 | 40 |
| Lint | 10 | 10 |
| Docs | 7 | 10 |
| **Total** | **82** | **100** |
