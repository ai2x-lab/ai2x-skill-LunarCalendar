# ai2x-skill-LunarCalendar

`ai2x-skill-LunarCalendar` 是一個給 OpenClaw / Agent 使用的「台灣節慶 / 農民曆 / 民俗行事曆查詢」技能專案。

## 正式 Skill 入口
**請從這裡開始：**
- `skills/tw_festival_calendar/SKILL.md`

**主要 runtime 位置：**
- `skills/tw_festival_calendar/runtime/`

也就是說，這個 repo 的正式 skill root 是：
- `skills/tw_festival_calendar/`

不是 repo 根目錄本身。

---

## 這個 skill 能做什麼
- 查詢台灣常見節慶、節日別名
- 查詢農曆/國曆對應日期
- 查詢節氣與週次型節日
- 查詢時辰吉凶（祭祀 / 安排時段參考）
- 輸出結構化 JSON，方便給 Agent 或自動化流程使用

---

## 快速開始
### 1. 讀 skill 定義
- `skills/tw_festival_calendar/SKILL.md`

### 2. 看快速安裝說明
- `skills/tw_festival_calendar/docs/quickstart.md`

### 3. 先做環境檢查
```bash
cd skills/tw_festival_calendar/runtime
python3 doctor.py
```

---

## 目錄說明
- `skills/tw_festival_calendar/SKILL.md`：Agent 使用規則與入口
- `skills/tw_festival_calendar/docs/`：部署與使用文件
- `skills/tw_festival_calendar/runtime/`：實際 CLI/runtime
- `skills/tw_festival_calendar/runtime/doctor.py`：部署前檢查

---

## Deployment hardening
- 已補 `.gitignore`（忽略 `.venv/`, `*.egg-info/`, `__pycache__/`, `*.pyc`）
- 已補 `doctor.py`
- Quickstart 已補 Linux/macOS/Windows 說明
- Debian/Ubuntu 已補 `python3-venv` 依賴提醒

---

## 建議部署原則
- Agent flow 請使用 `--json`
- 若搭配 cron，建議使用 `isolated`
- 上線前先跑 `doctor.py`
- 不要把 `.venv/`、cache、egg-info 產物 commit 進 repo
