from pathlib import Path

import pytest
from django.test import Client


def test_home_has_premium_sections():
    response = Client().get("/")
    assert response.status_code == 200
    assert b"hero-editorial" in response.content
    assert b"trust-bar-editorial" in response.content
    assert b"Publier ma demande" in response.content


def test_home_uses_editorial_shell_and_service_images():
    response = Client().get("/")
    assert response.status_code == 200
    assert b"service-grid-editorial" in response.content
    assert b"/static/images/services/thumbs/plomberie.webp" in response.content
    assert b"/static/images/services/thumbs/electricite.webp" in response.content


def test_stylesheet_contains_editorial_design_tokens():
    css = Path("static/css/theme.css").read_text(encoding="utf-8")
    assert "--radius-md: 14px" in css
    assert ".hero-editorial" in css
    assert ".service-card-editorial" in css
    assert "--eyebrow-on-light: #8142FF" in css


def test_typography_scale_is_balanced_on_hero():
    css = Path("static/css/theme.css").read_text(encoding="utf-8")
    home = Path("templates/home.html").read_text(encoding="utf-8")
    assert "font-size: clamp(.9rem, 1vw, 1rem)" in css
    assert "font-size: clamp(2.3rem, 4.7vw, 4rem)" in css
    assert "hero-panel-title" in css
    assert 'style="' not in home


def test_home_section_labels_are_larger_than_standard_eyebrows():
    css = Path("static/css/theme.css").read_text(encoding="utf-8")
    home = Path("templates/home.html").read_text(encoding="utf-8")
    assert 'class="eyebrow eyebrow-section">Services</p>' in home
    assert 'class="eyebrow eyebrow-section">Processus</p>' in home
    assert "font-size: clamp(1.08rem, 1.35vw, 1.24rem)" in css


def test_home_has_all_28_service_images():
    response = Client().get("/")
    assert response.status_code == 200
    assert response.content.count(b'class="service-card-editorial"') == 28
    assert b"/static/images/services/thumbs/transport.webp" in response.content
    assert response.content.count(b'loading="lazy"') == 28
    assert response.content.count(b'decoding="async"') == 28


def test_static_service_metadata_does_not_publish_base64_payloads():
    services_dir = Path("static/images/services")
    for metadata_path in services_dir.glob("*.json"):
        assert "b64_json" not in metadata_path.read_text(encoding="utf-8")


def test_service_grid_uses_optimized_webp_thumbnails():
    thumbs_dir = Path("static/images/services/thumbs")
    thumbnails = list(thumbs_dir.glob("*.webp"))
    assert len(thumbnails) == 28
    assert all(path.stat().st_size < 80_000 for path in thumbnails)


def test_service_images_fill_card_placeholders_better():
    css = Path("static/css/theme.css").read_text(encoding="utf-8")
    assert "aspect-ratio: 1 / .88" in css
    assert "transform: scale(1.14)" in css
    assert "padding: 2px" in css


def test_forms_use_premium_form_panel():
    for path in ["/comptes/connexion/", "/comptes/inscription-client/"]:
        response = Client().get(path)
        assert response.status_code == 200
        assert b"form-panel-editorial" in response.content


@pytest.mark.django_db
def test_operational_pages_use_editorial_cards():
    response = Client().get("/travaux/")
    assert response.status_code == 200
    assert b"page-header-editorial" in response.content
    assert b"data-empty-state" in response.content


@pytest.mark.django_db
def test_primary_pages_still_render_after_redesign():
    for path in ["/", "/travaux/", "/comptes/connexion/", "/comptes/inscription-client/"]:
        response = Client().get(path)
        assert response.status_code == 200
        assert b"Book now" not in response.content


def test_home_shows_services_from_provided_list():
    response = Client().get("/")
    assert response.status_code == 200
    for service in (
        b"Ascenseurs",
        b"Carrelage",
        b"Climatisation et froid",
        b"Plomberie",
        b"Vitrerie aluminium",
    ):
        assert service in response.content
