# Festival Rule Schema

Rule file examples:

- `src/calendar_engine/data/festival_rules_base.json`
- `src/calendar_engine/data/festival_rules_user.json`

Fields:

- `id`: unique key
- `name_zh`: Chinese name
- `name_en`: optional English name
- `type`: `traditional|seasonal|religious|custom`
- `category`: filtering category
- `rule_type`: `lunar_fixed|solar_fixed|solar_term|weekday_based`
- `rule`: payload by rule type
- `tags`: optional tags
- `notes`: optional notes

Supported category examples:

- `major_traditional`
- `lunar_1_15`
- `buddhist_taoist`
- `solar_term`
- `folk_custom`
- `custom_user`

