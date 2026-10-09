# Hospital Ontology Excercise

## The goal of this project is to practice the ontology architecture behind Palantir Foundry (object types, link types, action types with validation, and permissions) by modelling a reduced version of a hospital backend.

## Technologies used: Python, SQLAlchemy 2.0, Postgres, Pydantic v2, Alembic, pytest.

## Concept mapping (Foundry concept)

| Object types | SQLAlchemy models: `Patient`, `Bed`, `Section`, `Staff`, `Equipment` |
| Link types (named relationship between two object types) | `Occupancy` (patient ↔ bed), `ShiftAssignment` (staff ↔ section) | Links live in the models, as foreign keys and link tables | Think of it as object cardinality.
| Action types | Functions in `actions/`: `create_bed`, `assign_patient_to_bed`, `discharge_patient`, `create_equipment`, `assign_shift_to_staff` |
| Action parameters and validation | Pydantic schemas in `schemas/` |
| Permissions | Role check at the start of every action (RBAC) |
| Effects | State transitions: bed `free → taken → free`, occupancy `active → discharged` |

## How an action runs

```
params (Pydantic) -> permission check -> load and validate objects -> apply state change -> commit
```

Example: `assign_patient_to_bed` requires the `admin_staff` role, requires the
bed to be free and the patient to exist, then creates an `Occupancy` and marks
the bed `taken`. `discharge_patient` closes the occupancy and frees the bed.

## Design decisions
- **Models stay plain, schemas validate.** Models describe storage. Pydantic
  schemas validate the input at the boundary of each action.
- **Status is derived, never supplied.** Callers cannot set an occupancy or bed
  status directly. Only actions move the state machine.
- **Authorization first.** Each action checks the caller's role before touching
  the database.
- **UUID primary keys.** Records from different systems can be merged without id
  collisions, which matters for an ontology that integrates several sources.
- **Test-driven.** Each action started from a failing test following the red-green-refactor pattern famous in Ruby on Rails.

## Project layout
```
actions/      action types (business logic)
schemas/      Pydantic parameter schemas
models/       SQLAlchemy models
migrations/   Alembic migrations
tests/        schemas/, actions/, helpers/
constants.py  BedStatus, OccupancyStatus
```

## Run it
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# tests use in-memory SQLite, no database needed
python -m pytest

# migrations need Postgres
export DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/hospital_ontology
alembic upgrade head
```

## Future improvements
- ABAC (attribute-based rules, e.g. only staff assigned to a section can act on it)
- Audit log of every action
- HTTP API layer
- CI