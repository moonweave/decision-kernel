# Anneal Example: Inventory Dashboard Direction

This is a representative `/anneal` run for a coding agent deciding the primary
UI direction for a developer inventory dashboard.

## Prompt

```text
/anneal choose the primary UI direction for a developer inventory dashboard:
table vs graph vs cards
```

## Goal

The dashboard must help a developer answer three practical questions quickly:

1. Who owns this service?
2. Which inventory items are risky right now?
3. How does this item relate to teams, services, and repositories?

## Direction Fitness

| Fitness Question | Measurement | Weight |
| --- | --- | ---: |
| Find owner | Steps to identify owner for a named service | 3 |
| Spot risk | Count of high-risk items visible without drilling in | 3 |
| Trace relationships | Relationship types visible from the first screen | 2 |
| Compare items | Number of items comparable at once | 2 |
| Build cost | Estimated implementation complexity for first usable version | 1 |

## Candidate Sketches

| Candidate | Find Owner | Spot Risk | Trace Relationships | Compare Items | Build Cost | Weighted Score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Table-first | 3 | 3 | 2 | 3 | 2 | 31 |
| Graph-first | 2 | 2 | 3 | 1 | 1 | 22 |
| Card-first | 2 | 2 | 1 | 2 | 3 | 22 |

## Decision

Build the table-first direction. The graph is useful later as a secondary
relationship view, but it should not be the primary screen because it performs
worse on owner lookup, risk scanning, and item comparison.

## Implementation Guidance

Start with a dense table that includes owner, service, repository, risk, stale
age, and relationship count. Add filters for owner and risk before adding a
graph. If relationship tracing becomes the main bottleneck after the table
exists, then add a graph detail panel from the selected row.

## Why This Matters

Without the fitness sheet, the agent may spend the session polishing a graph
because it feels more sophisticated. With the fitness sheet, the first build
serves the user's actual questions.

