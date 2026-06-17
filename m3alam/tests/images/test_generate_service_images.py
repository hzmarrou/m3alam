from scripts.generate_service_images import build_prompt, parse_services_selection


def test_build_prompt_contains_style_and_service_label():
    prompt = build_prompt("ascenseurs", "Ascenseurs")
    assert "3D isometric professional" in prompt
    assert "Ascenseurs" in prompt
    assert "1024x1024" in prompt


def test_parse_services_selection_supports_sample_keyword():
    selected = parse_services_selection(
        "sample",
        {"ascenseurs", "carrelage", "clim-et-froid", "plomberie", "vitrerie-aluminium"},
    )
    assert selected == [
        "ascenseurs",
        "carrelage",
        "clim-et-froid",
        "plomberie",
        "vitrerie-aluminium",
    ]

