# Architecture

## Layers

1. Engine layer (`engine/`)
- Gregorian/lunar conversion
- Solar term extraction
- Festival evaluation

2. Rule layer (`rules/`)
- Rule parsing and validation
- Rule-type evaluators (`lunar_fixed`, `solar_fixed`, `solar_term`, `weekday_based`)

3. Cache layer (`cache/`)
- Per-year JSON storage
- Cache document schema
- Build/rebuild and validation

4. Service layer (`services/`)
- Query orchestration
- Cache initialization policy
- Custom festival lifecycle

5. Interface layer (`cli/`)
- Argparse command routing
- Human/JSON output modes

## Startup behavior

- `initialize` ensures current year + next year caches exist and are valid.
- Missing or schema-mismatched cache files are rebuilt automatically.

## Extensibility

- New festivals can be appended in base/user rule JSON.
- New rule types can be introduced by adding evaluator modules and registry mapping.
- Storage can later support SQLite by introducing a new store implementation.

