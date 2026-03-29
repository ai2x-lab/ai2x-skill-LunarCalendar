from datetime import date


def test_year_boundary_next_festival(service):
    result = service.next_festival(date(2026, 12, 25)).to_dict()
    record = result["data"]["record"]
    assert record is not None
    assert record["solar_date"] >= "2026-12-25"

