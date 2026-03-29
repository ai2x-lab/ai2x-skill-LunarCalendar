from datetime import date


def test_solar_to_lunar_lookup(service):
    result = service.lookup_date(date(2026, 9, 25)).to_dict()
    record = result["data"]["record"]
    assert record["lunar_month"] == 8
    assert record["lunar_day"] == 15

