# Command Reference

## Query

- `twcal today --json`
- `twcal lookup-date YYYY-MM-DD --json`
- `twcal lookup-lunar --year Y --month M --day D [--leap-month] --json`
- `twcal next-festival --from YYYY-MM-DD --json`
- `twcal list-festivals --year Y [--month M] [--type T] [--ignore-lunar-1-15] [--ignore-religious] --json`
- `twcal search-festival --year Y --name KW [--mode exact|contains|fuzzy] --json`
- `twcal range --start YYYY-MM-DD --end YYYY-MM-DD --json`

## Cache

- `twcal rebuild-cache --years 2026,2027 --json`
- `twcal check-cache [--year Y] --json`

## Custom Festivals

- `twcal add-festival --id ID --name-zh NAME --rule-type TYPE --rule '{...}' --rebuild auto --json`
- `twcal remove-festival --id ID --rebuild auto --json`
- `twcal list-custom-festivals --json`
