# LunarCalendar-Skills

`ai2x-skill-LunarCalendar` 是一個給 Agent 使用的「台灣節慶 / 農民曆查詢與規則化推理」技能集合。

它的目標是讓 Jarvis / Lumi / Scribe 這類助理，在對話中可以：

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

## 相關文件

- Quickstart: `skills/tw_festival_calendar/docs/quickstart.md`
- Command reference: `skills/tw_festival_calendar/docs/command-reference.md`
- Agent integration: `skills/tw_festival_calendar/docs/agent-integration.md`
