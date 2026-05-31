# Project Roadmap

## Phase 1 — Core server (DONE)
Implement the base server, unit tests, CI pipeline.

## Phase 2 — Config schema validation (DONE)
Add JSON Schema validation for ingested config files.

## Phase 3 — Multi-host aggregation (DEFERRED)
Aggregate config entries across multiple host registries into a unified view.
Blocked on host-registry API stabilization; revisit in Q3.

## Phase 4 — Alerting integration (NOT STARTED)
Emit alerts when a registered server disappears from a host config.
