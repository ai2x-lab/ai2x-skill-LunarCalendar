# Example: Ambiguous Festival Name

User asks: 「幫我查仲秋是幾號」

Run:

```bash
twcal search-festival --year 2026 --name 仲秋 --mode fuzzy --json
```

Then read:

- `data.items[0].solar_date` => `2026-09-25`
- `data.items[0].festivals[0].name_zh` => `中秋節`
