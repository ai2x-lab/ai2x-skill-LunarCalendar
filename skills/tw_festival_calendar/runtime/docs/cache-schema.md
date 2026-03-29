# Cache Schema Notes

Cache file path: `cache/YYYY.json`

Top-level fields:

- `schema_version`
- `generated_at`
- `year`
- `engine_version`
- `source`
- `days`

Each day record:

- `solar_date`
- `weekday`
- `weekday_name`
- `lunar_year`
- `lunar_month`
- `lunar_day`
- `lunar_month_name`
- `lunar_day_name`
- `is_leap_month`
- `solar_term`
- `festivals`
- `notes`

Festival entry fields:

- `id`
- `name_zh`
- `name_en`
- `type`
- `category`
- `source_rule`
- `tags`
- `notes`

