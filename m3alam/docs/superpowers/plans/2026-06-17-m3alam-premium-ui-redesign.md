# M3alam Premium UI Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a premium, conversion-focused French UI redesign for M3alam while preserving existing backend behavior and routes.

**Architecture:** Keep Django server-rendered templates and current view logic, and replace the visual layer with a shadcn-inspired Tailwind system plus reusable component blocks in templates. Centralize brand tokens and UI states in one stylesheet entrypoint and wire reusable page sections through template includes.

**Tech Stack:** Python 3.12, Django 5.x templates, Tailwind CSS CLI, pytest, pytest-django

---

## File Structure (target)

- Create: `m3alam/package.json` (Tailwind toolchain)
- Create: `m3alam/tailwind.config.js` (theme tokens + content scan)
- Create: `m3alam/static/css/input.css` (Tailwind source with token layer)
- Modify: `m3alam/static/css/theme.css` (fallback legacy tokens only)
- Create: `m3alam/templates/components/{nav.html,hero.html,trust_strip.html,footer.html,card_job.html,card_offer.html}`
- Modify: `m3alam/templates/{base.html,home.html,jobs/job_list.html,jobs/job_detail.html,jobs/job_form.html,accounts/login.html,accounts/signup_client.html,accounts/signup_artisan.html,offers/offer_form.html,offers/client_contact.html,admin_portal/dashboard.html}`
- Create: `m3alam/tests/ui/test_ui_render.py`
- Create: `m3alam/tests/ui/test_ui_french_copy.py`

### Task 1: Add UI toolchain and brand token foundation

**Files:**
- Create: `m3alam/package.json`
- Create: `m3alam/tailwind.config.js`
- Create: `m3alam/static/css/input.css`
- Modify: `m3alam/templates/base.html`
- Test: `m3alam/tests/ui/test_ui_render.py`

- [ ] **Step 1: Write the failing test**

```python
# m3alam/tests/ui/test_ui_render.py
from django.test import Client

def test_base_loads_new_ui_stylesheet():
    client = Client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"/static/css/output.css" in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_render.py::test_base_loads_new_ui_stylesheet -v`
Expected: FAIL because `output.css` is not referenced yet.

- [ ] **Step 3: Write minimal implementation**

```json
// m3alam/package.json
{
  "name": "m3alam-ui",
  "private": true,
  "scripts": {
    "build:css": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.10"
  }
}
```

```js
// m3alam/tailwind.config.js
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        black1: "#000000",
        white1: "#FFFFFF",
        grey1: "#29282A",
        creme: "#F7F6F9",
        primary: "#8142FF",
        primaryLight: "#AA80FF",
        grey3: "#706D72",
        grey2: "#434045",
        grey5: "#CAC9CF",
        lime: "#DAFF01"
      }
    }
  },
  plugins: []
};
```

```css
/* m3alam/static/css/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body { @apply bg-creme text-grey1 antialiased; }
}
```

```html
<!-- m3alam/templates/base.html -->
<link rel="stylesheet" href="{% static 'css/output.css' %}">
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && npm install && npm run build:css && pytest tests/ui/test_ui_render.py::test_base_loads_new_ui_stylesheet -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/package.json m3alam/tailwind.config.js m3alam/static/css/input.css m3alam/templates/base.html m3alam/tests/ui/test_ui_render.py
git commit -m "feat: add tailwind foundation with brand color tokens"
```

### Task 2: Rebuild base layout (premium nav + footer + spacing system)

**Files:**
- Create: `m3alam/templates/components/nav.html`
- Create: `m3alam/templates/components/footer.html`
- Modify: `m3alam/templates/base.html`
- Test: `m3alam/tests/ui/test_ui_render.py`

- [ ] **Step 1: Write the failing test**

```python
def test_home_has_premium_nav_and_footer():
    client = Client()
    response = client.get("/")
    assert b"data-testid='premium-nav'" in response.content
    assert b"data-testid='premium-footer'" in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_render.py::test_home_has_premium_nav_and_footer -v`
Expected: FAIL because new components do not exist.

- [ ] **Step 3: Write minimal implementation**

```html
<!-- m3alam/templates/components/nav.html -->
<header data-testid="premium-nav" class="sticky top-0 z-40 border-b border-grey5/70 bg-white1/95 backdrop-blur">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
    <a href="/" class="text-xl font-bold text-grey1">M3alam</a>
    <nav class="flex items-center gap-6 text-sm font-medium">
      <a href="/travaux/" class="text-grey2 hover:text-primary">Demandes</a>
      <a href="/travaux/nouveau/" class="rounded-xl bg-primary px-4 py-2 text-white1 hover:bg-primaryLight">Publier ma demande</a>
    </nav>
  </div>
</header>
```

```html
<!-- m3alam/templates/components/footer.html -->
<footer data-testid="premium-footer" class="mt-12 border-t border-grey5 bg-white1">
  <div class="mx-auto max-w-6xl px-4 py-8 text-sm text-grey3">
    © M3alam — Artisans vérifiés au Maroc.
  </div>
</footer>
```

```html
<!-- m3alam/templates/base.html -->
{% include "components/nav.html" %}
<main class="mx-auto min-h-[70vh] w-full max-w-6xl px-4 py-8">{% block content %}{% endblock %}</main>
{% include "components/footer.html" %}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_render.py::test_home_has_premium_nav_and_footer -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/templates/components/nav.html m3alam/templates/components/footer.html m3alam/templates/base.html m3alam/tests/ui/test_ui_render.py
git commit -m "feat: implement premium global layout with sticky nav and footer"
```

### Task 3: Redesign homepage for conversion and trust

**Files:**
- Create: `m3alam/templates/components/hero.html`
- Create: `m3alam/templates/components/trust_strip.html`
- Modify: `m3alam/templates/home.html`
- Test: `m3alam/tests/ui/test_ui_french_copy.py`

- [ ] **Step 1: Write the failing test**

```python
# m3alam/tests/ui/test_ui_french_copy.py
from django.test import Client

def test_home_shows_conversion_cta_and_trust_items():
    response = Client().get("/")
    assert b"Publier ma demande" in response.content
    assert b"Artisans verifies" not in response.content
    assert b"Artisans verifi\xc3\xa9s" in response.content
    assert b"R\xc3\xa9ponse rapide" in response.content
    assert b"Garantie service" in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_french_copy.py::test_home_shows_conversion_cta_and_trust_items -v`
Expected: FAIL because trust UI is not implemented.

- [ ] **Step 3: Write minimal implementation**

```html
<!-- m3alam/templates/components/hero.html -->
<section class="grid gap-6 rounded-3xl bg-gradient-to-br from-primary to-primaryLight p-8 text-white1 md:grid-cols-2">
  <div>
    <h1 class="text-3xl font-bold">Trouvez un artisan fiable en quelques minutes</h1>
    <p class="mt-3 text-white1/90">Publiez votre besoin et recevez des offres qualifiées rapidement.</p>
    <a href="/travaux/nouveau/" class="mt-6 inline-flex rounded-xl bg-white1 px-5 py-3 font-semibold text-primary">Publier ma demande</a>
  </div>
</section>
```

```html
<!-- m3alam/templates/components/trust_strip.html -->
<section class="mt-6 grid gap-3 md:grid-cols-3">
  <div class="rounded-2xl border border-grey5 bg-white1 p-4">Artisans vérifiés</div>
  <div class="rounded-2xl border border-grey5 bg-white1 p-4">Réponse rapide</div>
  <div class="rounded-2xl border border-grey5 bg-white1 p-4">Garantie service</div>
</section>
```

```html
<!-- m3alam/templates/home.html -->
{% extends "base.html" %}
{% block content %}
  {% include "components/hero.html" %}
  {% include "components/trust_strip.html" %}
{% endblock %}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_french_copy.py::test_home_shows_conversion_cta_and_trust_items -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/templates/components/hero.html m3alam/templates/components/trust_strip.html m3alam/templates/home.html m3alam/tests/ui/test_ui_french_copy.py
git commit -m "feat: redesign homepage hero and trust strip for conversion"
```

### Task 4: Redesign jobs list and detail with premium cards

**Files:**
- Create: `m3alam/templates/components/card_job.html`
- Create: `m3alam/templates/components/card_offer.html`
- Modify: `m3alam/templates/jobs/job_list.html`
- Modify: `m3alam/templates/jobs/job_detail.html`
- Test: `m3alam/tests/ui/test_ui_render.py`

- [ ] **Step 1: Write the failing test**

```python
def test_job_pages_use_card_layout_classes(admin_client):
    list_response = admin_client.get("/travaux/")
    assert b"job-card" in list_response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_render.py::test_job_pages_use_card_layout_classes -v`
Expected: FAIL because job card component does not exist.

- [ ] **Step 3: Write minimal implementation**

```html
<!-- m3alam/templates/components/card_job.html -->
<article class="job-card rounded-2xl border border-grey5 bg-white1 p-5 shadow-sm">
  <h3 class="text-lg font-semibold text-grey1">{{ job.title }}</h3>
  <p class="mt-1 text-sm text-grey3">{{ job.city }} • {{ job.category }}</p>
  <a href="/travaux/{{ job.id }}/" class="mt-4 inline-flex text-sm font-semibold text-primary">Voir la demande</a>
</article>
```

```html
<!-- m3alam/templates/jobs/job_list.html -->
{% extends "base.html" %}
{% block content %}
<section class="grid gap-4 md:grid-cols-2">
  {% for job in jobs %}
    {% include "components/card_job.html" %}
  {% empty %}
    <p>Aucune demande pour le moment.</p>
  {% endfor %}
</section>
{% endblock %}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_render.py::test_job_pages_use_card_layout_classes -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/templates/components/card_job.html m3alam/templates/components/card_offer.html m3alam/templates/jobs/job_list.html m3alam/templates/jobs/job_detail.html m3alam/tests/ui/test_ui_render.py
git commit -m "feat: redesign job listing and detail with premium cards"
```

### Task 5: Redesign forms (auth, job, offer, admin dashboard) with consistent states

**Files:**
- Modify: `m3alam/templates/accounts/login.html`
- Modify: `m3alam/templates/accounts/signup_client.html`
- Modify: `m3alam/templates/accounts/signup_artisan.html`
- Modify: `m3alam/templates/jobs/job_form.html`
- Modify: `m3alam/templates/offers/offer_form.html`
- Modify: `m3alam/templates/admin_portal/dashboard.html`
- Test: `m3alam/tests/ui/test_ui_french_copy.py`

- [ ] **Step 1: Write the failing test**

```python
def test_signup_page_has_french_heading_and_no_english():
    response = Client().get("/comptes/inscription-client/")
    assert b"Inscription client" in response.content
    assert b"Sign up" not in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui/test_ui_french_copy.py::test_signup_page_has_french_heading_and_no_english -v`
Expected: FAIL until new form template text is fully updated.

- [ ] **Step 3: Write minimal implementation**

```html
<!-- m3alam/templates/accounts/signup_client.html -->
{% extends "base.html" %}
{% block content %}
<section class="mx-auto max-w-xl rounded-2xl border border-grey5 bg-white1 p-6 shadow-sm">
  <h1 class="text-2xl font-bold text-grey1">Inscription client</h1>
  <p class="mt-1 text-sm text-grey3">Créez votre compte et publiez votre demande.</p>
  <form method="post" class="mt-6 space-y-4">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="w-full rounded-xl bg-primary px-4 py-3 font-semibold text-white1 hover:bg-primaryLight">Créer mon compte client</button>
  </form>
</section>
{% endblock %}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/ui/test_ui_french_copy.py::test_signup_page_has_french_heading_and_no_english -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/templates/accounts/login.html m3alam/templates/accounts/signup_client.html m3alam/templates/accounts/signup_artisan.html m3alam/templates/jobs/job_form.html m3alam/templates/offers/offer_form.html m3alam/templates/admin_portal/dashboard.html m3alam/tests/ui/test_ui_french_copy.py
git commit -m "feat: redesign forms and admin dashboard with premium french UI"
```

### Task 6: Add full UI smoke tests and final polish

**Files:**
- Modify: `m3alam/tests/ui/test_ui_render.py`
- Modify: `m3alam/tests/ui/test_ui_french_copy.py`
- Modify: `m3alam/static/css/input.css`
- Modify: `m3alam/templates/offers/client_contact.html`

- [ ] **Step 1: Write the failing test**

```python
def test_primary_pages_are_french_and_render_ok(client):
    paths = ["/", "/travaux/", "/comptes/connexion/"]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200
        assert b"Book now" not in response.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/ui -v`
Expected: FAIL until all remaining copy and classes are aligned.

- [ ] **Step 3: Write minimal implementation**

```css
/* m3alam/static/css/input.css */
@layer components {
  .panel { @apply rounded-2xl border border-grey5 bg-white1 p-6 shadow-sm; }
  .btn-primary { @apply rounded-xl bg-primary px-4 py-2 font-semibold text-white1 hover:bg-primaryLight; }
  .btn-secondary { @apply rounded-xl border border-grey5 bg-white1 px-4 py-2 font-semibold text-grey1 hover:bg-creme; }
}
```

```html
<!-- m3alam/templates/offers/client_contact.html -->
<section class="panel">
  <h1 class="text-2xl font-bold">Coordonnées du client</h1>
  <p class="mt-2 text-grey2"><strong>Email:</strong> {{ offer.job.client.email }}</p>
  <p class="text-grey2"><strong>Téléphone:</strong> {{ offer.job.client.phone }}</p>
</section>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && npm run build:css && pytest tests/ui -v`
Expected: PASS for all UI tests.

- [ ] **Step 5: Commit**

```bash
git add m3alam/tests/ui/test_ui_render.py m3alam/tests/ui/test_ui_french_copy.py m3alam/static/css/input.css m3alam/templates/offers/client_contact.html
git commit -m "test: finalize premium ui polish and french-only smoke coverage"
```

## Self-Review Checklist (completed)

1. **Spec coverage:** plan includes premium layout, conversion-focused home, trust signals, card-based jobs/offers, French-only copy, brand colors, and UI tests.
2. **Placeholder scan:** removed TBD/TODO and provided concrete code and commands in every task step.
3. **Type consistency:** uses consistent file paths, component names (`hero`, `trust_strip`, `card_job`, `card_offer`), and CSS utility naming (`btn-primary`, `panel`) across tasks.
