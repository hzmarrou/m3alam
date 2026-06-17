from jobs.service_catalog import SERVICE_CATEGORIES


def test_service_catalog_has_28_items_and_expected_labels():
    assert len(SERVICE_CATEGORIES) == 28
    mapping = dict(SERVICE_CATEGORIES)
    assert mapping["ascenseurs"] == "Ascenseurs"
    assert mapping["electricite"] == "Électricité"
    assert mapping["vitrerie-aluminium"] == "Vitrerie aluminium"

