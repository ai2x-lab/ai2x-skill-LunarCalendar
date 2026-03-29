# Usage Examples

Lookup a date:

```bash
twcal lookup-date 2026-09-25 --json
```

Lookup lunar date:

```bash
twcal lookup-lunar --year 2026 --month 8 --day 15 --json
```

List festivals and ignore religious events:

```bash
twcal list-festivals --year 2026 --ignore-religious --json
```

Add custom weekday-based reminder:

```bash
twcal add-festival \
  --id team_day \
  --name-zh 團隊日 \
  --type custom \
  --category custom_user \
  --rule-type weekday_based \
  --rule '{"month":10,"weekday":2,"nth":2}' \
  --rebuild years=2026,2027 \
  --json
```

