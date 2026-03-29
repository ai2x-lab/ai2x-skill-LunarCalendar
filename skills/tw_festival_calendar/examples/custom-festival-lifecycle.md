# Example: Add and Query Custom Festival

Add:

```bash
twcal add-festival --id company_day --name-zh 公司紀念日 --rule-type solar_fixed --rule '{"month":11,"day":3}' --rebuild auto --json
```

Query:

```bash
twcal search-festival --year 2026 --name 公司紀念日 --mode exact --json
```

Cleanup:

```bash
twcal remove-festival --id company_day --rebuild auto --json
```
