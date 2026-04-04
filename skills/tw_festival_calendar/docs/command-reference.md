# Command Reference

## Query

- `twcal today --json`
- `twcal lookup-date YYYY-MM-DD --json`
- `twcal lookup-lunar --year Y --month M --day D [--leap-month] --json`
- `twcal next-festival --from YYYY-MM-DD --json`
- `twcal list-festivals --year Y [--month M] [--type T] [--ignore-lunar-1-15] [--ignore-religious] --json`
- `twcal search-festival --year Y --name KW [--mode exact|contains|fuzzy] --json`
- `twcal range --start YYYY-MM-DD --end YYYY-MM-DD --json`
- `twcal lookup-story --id FESTIVAL_ID --json`
- `twcal search-story --keyword KW --json`
- `twcal hour-fortune --date YYYY-MM-DD --json`
- `twcal hour-fortune --datetime YYYY-MM-DDTHH:MM --json`

## Story Query

- `twcal lookup-story --id mid_autumn --json`
- `twcal search-story --keyword 普渡 --json`

Story result fields:
- `id`
- `name_zh`
- `summary`
- `keywords`
- `source_refs`
- `markdown_path`

## Cache

- `twcal rebuild-cache --years 2026,2027 --json`
- `twcal check-cache [--year Y] --json`

## Custom Festivals

- `twcal add-festival --id ID --name-zh NAME --rule-type TYPE --rule '{...}' --rebuild auto --json`
- `twcal remove-festival --id ID --rebuild auto --json`
- `twcal list-custom-festivals --json`
