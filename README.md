# LunarCalendar-Skills

`ai2x-skill-LunarCalendar` 是一個給 Agent 使用的「台灣節慶 / 農民曆查詢與規則化推理」技能集合。

它的目標是讓 AI Agent 助理，在對話中可以：

- 以台灣常用名稱查節日（含別名）
- 解析農曆/國曆節慶規則（固定日、週次規則、節氣關聯）
- 提供可被程式/Agent 消費的結構化結果（JSON）
- 支援快取與測試，方便部署到自動化流程

---

## 應用場景

- 行事曆提醒：節慶前通知（如端午、中秋、清明）
- 內容排程：節日主題貼文 / 行銷活動時間點
- 客服問答：使用者詢問「某節是幾號」時快速回覆
- 自動化流程：搭配 Cron / 任務分派做節日觸發任務

---

## 專案結構

Skill packages are under:

- `skills/tw_festival_calendar/`

Main runtime (self-contained):

- `skills/tw_festival_calendar/runtime/`

Start from:

- `skills/tw_festival_calendar/SKILL.md`

---

## 主要能力（tw_festival_calendar）

- 節日查詢（名稱、別名）
- 節日日期推算（農曆轉換、節氣、週次型規則）
- 結果輸出 schema（便於 Agent/MCP 整合）
- 年度快取（降低重複計算成本）
- 測試覆蓋（保障規則正確性）

---

## 工具指令集（twcal）

### 查詢指令

- `twcal today --json`
- `twcal lookup-date YYYY-MM-DD --json`
- `twcal lookup-lunar --year Y --month M --day D [--leap-month] --json`
- `twcal next-festival --from YYYY-MM-DD --json`
- `twcal list-festivals --year Y [--month M] [--type T] [--ignore-lunar-1-15] [--ignore-religious] --json`
- `twcal search-festival --year Y --name KW [--mode exact|contains|fuzzy] --json`
- `twcal range --start YYYY-MM-DD --end YYYY-MM-DD --json`

### 快取維護指令

- `twcal rebuild-cache --years 2026,2027 --json`
- `twcal check-cache [--year Y] --json`

### 私有節日管理（使用者可自行新增/刪除）

- 新增私有節日：
  - `twcal add-festival --id ID --name-zh NAME --rule-type TYPE --rule '{...}' --rebuild auto --json`
- 刪除私有節日：
  - `twcal remove-festival --id ID --rebuild auto --json`
- 列出私有節日：
  - `twcal list-custom-festivals --json`

> 私有節日會寫入：
> `skills/tw_festival_calendar/runtime/src/calendar_engine/data/festival_rules_user.json`

---

## 相關文件

- Quickstart: `skills/tw_festival_calendar/docs/quickstart.md`
- Command reference: `skills/tw_festival_calendar/docs/command-reference.md`
- Agent integration: `skills/tw_festival_calendar/docs/agent-integration.md`

