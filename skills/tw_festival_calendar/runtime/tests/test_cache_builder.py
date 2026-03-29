def test_cache_generation_and_loading(service):
    init = service.initialize(2026).to_dict()
    assert init["status"] == "ok"
    check = service.check_cache([2026, 2027]).to_dict()
    assert check["data"]["status"][2026] == "ok"
    assert check["data"]["status"][2027] == "ok"

