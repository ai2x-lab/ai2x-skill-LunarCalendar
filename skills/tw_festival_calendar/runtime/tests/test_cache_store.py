def test_cache_store_exists_after_lookup(service):
    service.lookup_date(__import__("datetime").date(2026, 1, 1))
    assert service.store.exists(2026)

