def test_known_festival_mid_autumn(service):
    result = service.lookup_date(__import__("datetime").date(2026, 9, 25)).to_dict()
    festivals = result["data"]["record"]["festivals"]
    assert any(f["id"] == "mid_autumn" for f in festivals)


def test_solar_term_festivals_exist(service):
    data = service.list_festivals(2026, None, None, None, None).to_dict()["data"]["items"]
    ids = {f["id"] for day in data for f in day["festivals"]}
    assert "qingming" in ids
    assert "winter_solstice" in ids

