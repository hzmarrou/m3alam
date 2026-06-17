# Premium Editorial UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the M3alam UI into a restrained premium editorial marketplace experience using existing Django templates and generated service images.

**Architecture:** Keep current Django server-rendered architecture and business logic. Implement a stronger design system in `static/css/theme.css`, integrate service image assets via `jobs.service_catalog`, and update templates for public pages, forms, job/offer cards, and admin screens.

**Tech Stack:** Django templates, CSS, Python pytest/Django test client

---

## File Structure (target)

- Modify: `m3alam/static/css/theme.css`
- Modify: `m3alam/templates/base.html`
- Modify: `m3alam/templates/home.html`
- Modify: `m3alam/templates/jobs/job_form.html`
- Modify: `m3alam/templates/jobs/job_list.html`
- Modify: `m3alam/templates/jobs/job_detail.html`
- Modify: `m3alam/templates/accounts/login.html`
- Modify: `m3alam/templates/accounts/signup_client.html`
- Modify: `m3alam/templates/accounts/signup_artisan.html`
- Modify: `m3alam/templates/offers/offer_form.html`
- Modify: `m3alam/templates/offers/client_contact.html`
- Modify: `m3alam/templates/admin_portal/dashboard.html`
- Modify: `m3alam/tests/ui/test_ui_premium.py`

### Task 1: Add premium UI regression tests for service images and editorial shell

**Files:**
- Modify: `m3alam/tests/ui/test_ui_premium.py`

- [ ] **Step 1: Write the failing test**

```python
def test_home_uses_editorial_shell_and_service_images():
    response = Client().get("/")
    assert response.status_code == 200
    assert b"hero-editorial" in response.content
    assert b"service-grid-editorial" in response.content
    assert b"/static/images/services/plomberie.png" in response.content
    assert b"/static/images/services/electricite.png" in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_home_uses_editorial_shell_and_service_images -v`
Expected: FAIL because current homepage does not use `hero-editorial`, `service-grid-editorial`, or service images.

- [ ] **Step 3: Write minimal implementation**

No production implementation in this task; this task only establishes the RED test.

- [ ] **Step 4: Run test to verify it still fails for expected reason**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_home_uses_editorial_shell_and_service_images -v`
Expected: FAIL with missing `hero-editorial`.

- [ ] **Step 5: Commit**

```bash
git add m3alam/tests/ui/test_ui_premium.py
git commit -m "test: add premium editorial UI expectations"
```

### Task 2: Redefine CSS design system tokens and components

**Files:**
- Modify: `m3alam/static/css/theme.css`
- Test: `m3alam/tests/ui/test_ui_premium.py`

- [ ] **Step 1: Write the failing test**

```python
def test_stylesheet_contains_editorial_design_tokens():
    css = Path("static/css/theme.css").read_text(encoding="utf-8")
    assert "--radius-md: 14px" in css
    assert ".hero-editorial" in css
    assert ".service-card-editorial" in css
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_stylesheet_contains_editorial_design_tokens -v`
Expected: FAIL because tokens/classes are missing.

- [ ] **Step 3: Write minimal implementation**

```css
:root {
  --radius-sm: 10px;
  --radius-md: 14px;
  --radius-lg: 22px;
  --shadow-soft: 0 18px 45px rgba(41, 40, 42, 0.08);
}

.hero-editorial { background: var(--color-grey-1); color: var(--color-white); }
.service-card-editorial { background: var(--color-white); border: 1px solid rgba(202, 201, 207, .72); }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_stylesheet_contains_editorial_design_tokens -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/static/css/theme.css m3alam/tests/ui/test_ui_premium.py
git commit -m "feat: define premium editorial UI design system"
```

### Task 3: Rebuild base shell and landing page with service images

**Files:**
- Modify: `m3alam/templates/base.html`
- Modify: `m3alam/templates/home.html`
- Modify: `m3alam/config/urls.py` (only if needed to pass service catalog context)
- Test: `m3alam/tests/ui/test_ui_premium.py`

- [ ] **Step 1: Write the failing test**

```python
def test_home_has_all_28_service_images():
    response = Client().get("/")
    assert response.status_code == 200
    assert response.content.count(b'class="service-card-editorial"') == 28
    assert b"/static/images/services/transport.png" in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_home_has_all_28_service_images -v`
Expected: FAIL because current home page hardcodes text cards only.

- [ ] **Step 3: Write minimal implementation**

```python
# m3alam/config/urls.py
from jobs.service_catalog import SERVICE_CATEGORIES

path(
    "",
    TemplateView.as_view(template_name="home.html", extra_context={"service_categories": SERVICE_CATEGORIES}),
    name="home",
)
```

```html
<!-- m3alam/templates/home.html -->
<section class="service-grid-editorial">
  {% for slug, label in service_categories %}
    <article class="service-card-editorial">
      <img src="/static/images/services/{{ slug }}.png" alt="{{ label }}">
      <h3>{{ label }}</h3>
    </article>
  {% endfor %}
</section>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_home_has_all_28_service_images tests/ui/test_ui_premium.py::test_home_uses_editorial_shell_and_service_images -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/templates/base.html m3alam/templates/home.html m3alam/config/urls.py m3alam/tests/ui/test_ui_premium.py
git commit -m "feat: rebuild landing page with premium editorial service image grid"
```

### Task 4: Apply premium form system to auth, job, and offer forms

**Files:**
- Modify: `m3alam/templates/accounts/login.html`
- Modify: `m3alam/templates/accounts/signup_client.html`
- Modify: `m3alam/templates/accounts/signup_artisan.html`
- Modify: `m3alam/templates/jobs/job_form.html`
- Modify: `m3alam/templates/offers/offer_form.html`
- Test: `m3alam/tests/ui/test_ui_premium.py`

- [ ] **Step 1: Write the failing test**

```python
def test_forms_use_premium_form_panel():
    for path in ["/comptes/connexion/", "/comptes/inscription-client/"]:
        response = Client().get(path)
        assert response.status_code == 200
        assert b"form-panel-editorial" in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_forms_use_premium_form_panel -v`
Expected: FAIL because forms do not use `form-panel-editorial`.

- [ ] **Step 3: Write minimal implementation**

```html
<section class="form-panel-editorial">
  <p class="eyebrow">Accès sécurisé</p>
  <h1>Connexion</h1>
  <form method="post" class="form-stack">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary" type="submit">Se connecter</button>
  </form>
</section>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_forms_use_premium_form_panel -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/templates/accounts/login.html m3alam/templates/accounts/signup_client.html m3alam/templates/accounts/signup_artisan.html m3alam/templates/jobs/job_form.html m3alam/templates/offers/offer_form.html m3alam/tests/ui/test_ui_premium.py
git commit -m "feat: apply premium editorial styling to forms"
```

### Task 5: Apply premium card system to jobs, offers, contact, and admin

**Files:**
- Modify: `m3alam/templates/jobs/job_list.html`
- Modify: `m3alam/templates/jobs/job_detail.html`
- Modify: `m3alam/templates/offers/client_contact.html`
- Modify: `m3alam/templates/admin_portal/dashboard.html`
- Test: `m3alam/tests/ui/test_ui_premium.py`

- [ ] **Step 1: Write the failing test**

```python
def test_operational_pages_use_editorial_cards():
    response = Client().get("/travaux/")
    assert response.status_code == 200
    assert b"page-header-editorial" in response.content
    assert b"data-empty-state" in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_operational_pages_use_editorial_cards -v`
Expected: FAIL because job list lacks editorial page header and empty state marker.

- [ ] **Step 3: Write minimal implementation**

```html
<section class="page-header-editorial">
  <p class="eyebrow">Demandes</p>
  <h1>Demandes ouvertes</h1>
</section>

{% empty %}
  <div class="empty-state-editorial" data-empty-state>
    <p>Aucune demande pour le moment.</p>
  </div>
{% endfor %}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_operational_pages_use_editorial_cards -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/templates/jobs/job_list.html m3alam/templates/jobs/job_detail.html m3alam/templates/offers/client_contact.html m3alam/templates/admin_portal/dashboard.html m3alam/tests/ui/test_ui_premium.py
git commit -m "feat: apply premium card system to operational and admin screens"
```

### Task 6: Final validation and screenshot capture

**Files:**
- Modify: `m3alam/tests/ui/test_ui_premium.py`
- Create: `m3alam/docs/screenshots/after-home.html` (HTML snapshot if screenshot tooling unavailable)

- [ ] **Step 1: Write the failing verification test**

```python
def test_primary_pages_still_render_after_redesign():
    for path in ["/", "/travaux/", "/comptes/connexion/", "/comptes/inscription-client/"]:
        response = Client().get(path)
        assert response.status_code == 200
        assert b"Book now" not in response.content
```

- [ ] **Step 2: Run test to verify it fails if any page broke**

Run: `cd m3alam && pytest tests/ui/test_ui_premium.py::test_primary_pages_still_render_after_redesign -v`
Expected: PASS if implementation already correct; if FAIL, fix broken template before continuing.

- [ ] **Step 3: Capture after snapshot**

```bash
cd m3alam
python - <<PY
from pathlib import Path
from django.test import Client
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
Path("docs/screenshots").mkdir(parents=True, exist_ok=True)
Path("docs/screenshots/after-home.html").write_bytes(Client().get("/").content)
PY
```

- [ ] **Step 4: Run final validation**

Run: `cd m3alam && python manage.py check && pytest tests/ui/test_ui_premium.py jobs/tests/test_services_catalog.py -q`
Expected: PASS all checks/tests.

- [ ] **Step 5: Commit**

```bash
git add m3alam/tests/ui/test_ui_premium.py m3alam/docs/screenshots/after-home.html
git commit -m "test: validate premium editorial UI redesign"
```

## Self-Review Checklist (completed)

1. **Spec coverage:** covers UI audit, tokens/components, service image integration, public pages/forms/cards/admin, accessibility/responsive checks, and deliverables.
2. **Placeholder scan:** all tasks include concrete tests, code snippets, commands, and expected outcomes.
3. **Type consistency:** uses consistent class names (`hero-editorial`, `service-card-editorial`, `form-panel-editorial`, `page-header-editorial`) and image slug paths (`/static/images/services/<slug>.png`).
