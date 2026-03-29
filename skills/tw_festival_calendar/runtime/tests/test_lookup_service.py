from datetime import date


def test_next_festival(service):
    result = service.next_festival(date(2026, 9, 1)).to_dict()
    record = result["data"]["record"]
    assert record is not None
    assert record["solar_date"] >= "2026-09-01"


def test_custom_festival_lifecycle(service):
    rule = {
        "id": "temp_test_day",
        "name_zh": "測試節日",
        "name_en": None,
        "type": "custom",
        "category": "custom_user",
        "rule_type": "solar_fixed",
        "rule": {"month": 10, "day": 20},
        "tags": ["test"],
        "notes": [],
    }
    service.add_custom_festival(rule, rebuild_years=[2026])
    listed = service.search_festival(2026, "測試節日").to_dict()
    assert listed["data"]["items"]
    removed = service.remove_custom_festival("temp_test_day", rebuild_years=[2026]).to_dict()
    assert removed["data"]["removed"] is True


def test_search_festival_fuzzy_mode(service):
    result = service.search_festival(2026, "中秋", mode="fuzzy").to_dict()
    items = result["data"]["items"]
    assert items
    all_ids = {f["id"] for row in items for f in row["festivals"]}
    assert "mid_autumn" in all_ids


def test_search_festival_suggestions_when_not_found(service):
    result = service.search_festival(2026, "完全無關詞", mode="exact").to_dict()
    assert result["data"]["items"] == []
    assert isinstance(result["data"]["suggestions"], list)


def test_search_festival_alias_returns_items(service):
    result = service.search_festival(2026, "月娘節", mode="fuzzy").to_dict()
    items = result["data"]["items"]
    assert items
    assert any(row["solar_date"] == "2026-09-25" for row in items)


def test_search_festival_alias_file_supports_zhongqiu(service):
    result = service.search_festival(2026, "仲秋", mode="contains").to_dict()
    items = result["data"]["items"]
    assert items
    assert any(row["solar_date"] == "2026-09-25" for row in items)
