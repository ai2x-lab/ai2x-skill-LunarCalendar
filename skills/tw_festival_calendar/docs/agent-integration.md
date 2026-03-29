# Agent Integration Notes

## Recommended flow

1. Use narrow query command.
2. Parse JSON output by stable fields (`status`, `action`, `data`, `meta`, `errors`).
3. If ambiguous search result, retry with fuzzy mode.
4. If still not found, check `data.suggestions`.

## Example command and expected keys

Command:

```bash
twcal search-festival --year 2026 --name 月娘節 --mode fuzzy --json
```

Expected JSON keys:

- `data.items[*].solar_date`
- `data.items[*].festivals[*].id`
- `data.items[*].festivals[*].name_zh`

## Deterministic behavior notes

- No external API calls.
- Data comes from local cache and local rule files.
- Rebuild is explicit and year-scoped.
