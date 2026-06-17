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
    assert b"/static/images/services/plomberie.png" in response.content
    assert b"/static/images/services/electricite.png" in response.content


def test_stylesheet_contains_editorial_design_tokens():
    css = Path("static/css/theme.css").read_text(encoding="utf-8")
    assert "--radius-md: 14px" in css
    assert ".hero-editorial" in css
    assert ".service-card-editorial" in css


def test_home_has_all_28_service_images():
    response = Client().get("/")
    assert response.status_code == 200
    assert response.content.count(b'class="service-card-editorial"') == 28
    assert b"/static/images/services/transport.png" in response.content


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
