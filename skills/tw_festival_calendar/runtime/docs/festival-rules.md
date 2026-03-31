# Festival Rule Schema

Rule/data file examples:

- `src/calendar_engine/data/festival_rules_base.json` (日期規則)
- `src/calendar_engine/data/festival_rules_user.json` (使用者擴充規則)
- `src/calendar_engine/data/festival_stories.json` (典故摘要/來源/關鍵字)
- `src/calendar_engine/data/stories/*.md` (可選長文典故)

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

