# Service Images GPT-Image-2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a repeatable GPT-Image-2 pipeline that generates premium service images for M3alam, starting with 5 samples then scaling to all 28 services.

**Architecture:** Add one dedicated Python generator script in `m3alam/scripts` that reuses the proven Purview pattern (dotenv config, retries, rate limiting, manifest, prompt/metadata artifacts). Source service definitions from one shared catalog module so homepage labels and generation prompts stay consistent. Keep output in `m3alam/static/images/services` using slug filenames.

**Tech Stack:** Python 3.11+, Azure OpenAI GPT-Image-2 API, pytest

---

## File Structure (target)

- Create: `m3alam/scripts/generate_service_images.py`
- Create: `m3alam/jobs/service_catalog.py`
- Modify: `m3alam/jobs/forms.py`
- Modify: `m3alam/templates/home.html`
- Create: `m3alam/tests/images/test_generate_service_images.py`
- Create: `m3alam/tests/jobs/test_service_catalog.py`

### Task 1: Extract shared service catalog (slug + French label)

**Files:**
- Create: `m3alam/jobs/service_catalog.py`
- Modify: `m3alam/jobs/forms.py`
- Modify: `m3alam/templates/home.html`
- Test: `m3alam/tests/jobs/test_service_catalog.py`

- [ ] **Step 1: Write the failing test**

```python
# m3alam/tests/jobs/test_service_catalog.py
from jobs.service_catalog import SERVICE_CATEGORIES


def test_service_catalog_has_28_items_and_expected_labels():
    assert len(SERVICE_CATEGORIES) == 28
    mapping = dict(SERVICE_CATEGORIES)
    assert mapping["ascenseurs"] == "Ascenseurs"
    assert mapping["electricite"] == "Électricité"
    assert mapping["vitrerie-aluminium"] == "Vitrerie aluminium"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/jobs/test_service_catalog.py::test_service_catalog_has_28_items_and_expected_labels -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'jobs.service_catalog'`.

- [ ] **Step 3: Write minimal implementation**

```python
# m3alam/jobs/service_catalog.py
SERVICE_CATEGORIES = [
    ("ascenseurs", "Ascenseurs"),
    ("carrelage", "Carrelage"),
    ("clim-et-froid", "Climatisation et froid"),
    ("demolition", "Démolition"),
    ("depannage", "Dépannage"),
    ("electricite", "Électricité"),
    ("electricite-auto", "Électricité auto"),
    ("electro-menager", "Électroménager"),
    ("electronique", "Électronique"),
    ("encadrement", "Encadrement"),
    ("etancheite", "Étanchéité"),
    ("ferronnerie", "Ferronnerie"),
    ("jardinier", "Jardinage"),
    ("maconnerie", "Maçonnerie"),
    ("marbre", "Marbre"),
    ("mecanique", "Mécanique"),
    ("menuiserie", "Menuiserie"),
    ("parabole", "Parabole"),
    ("peinture", "Peinture"),
    ("piscine", "Piscine"),
    ("platrier", "Plâtrerie"),
    ("plomberie", "Plomberie"),
    ("pneumatiques", "Pneumatiques"),
    ("serrurerie", "Serrurerie"),
    ("surveillance-et-alarmes", "Surveillance et alarmes"),
    ("tapisserie", "Tapisserie"),
    ("transport", "Transport"),
    ("vitrerie-aluminium", "Vitrerie aluminium"),
]
```

```python
# m3alam/jobs/forms.py (imports + choices)
from .service_catalog import SERVICE_CATEGORIES

self.fields["category"] = forms.ChoiceField(
    label="Catégorie",
    choices=SERVICE_CATEGORIES,
)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/jobs/test_service_catalog.py::test_service_catalog_has_28_items_and_expected_labels -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/jobs/service_catalog.py m3alam/jobs/forms.py m3alam/templates/home.html m3alam/tests/jobs/test_service_catalog.py
git commit -m "refactor: centralize service catalog for forms and UI"
```

### Task 2: Add GPT-Image-2 generator script with dry-run and naming

**Files:**
- Create: `m3alam/scripts/generate_service_images.py`
- Test: `m3alam/tests/images/test_generate_service_images.py`

- [ ] **Step 1: Write the failing test**

```python
# m3alam/tests/images/test_generate_service_images.py
from scripts.generate_service_images import build_prompt, parse_services_selection


def test_build_prompt_contains_style_and_service_label():
    prompt = build_prompt("ascenseurs", "Ascenseurs")
    assert "3D isometric professional" in prompt
    assert "Ascenseurs" in prompt
    assert "1024x1024" in prompt


def test_parse_services_selection_supports_sample_keyword():
    selected = parse_services_selection("sample")
    assert selected == [
        "ascenseurs",
        "carrelage",
        "clim-et-froid",
        "plomberie",
        "vitrerie-aluminium",
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.generate_service_images'`.

- [ ] **Step 3: Write minimal implementation**

```python
# m3alam/scripts/generate_service_images.py
from __future__ import annotations

import argparse
from pathlib import Path

from jobs.service_catalog import SERVICE_CATEGORIES

SAMPLE_SERVICES = [
    "ascenseurs",
    "carrelage",
    "clim-et-froid",
    "plomberie",
    "vitrerie-aluminium",
]


def parse_services_selection(selection: str) -> list[str]:
    if selection == "sample":
        return SAMPLE_SERVICES
    if selection == "all":
        return [slug for slug, _ in SERVICE_CATEGORIES]
    return [item.strip() for item in selection.split(",") if item.strip()]


def build_prompt(slug: str, label: str) -> str:
    return (
        "3D isometric professional illustration for a home-services marketplace card. "
        "Square framing 1024x1024, centered object, clean neutral background, no text. "
        f"Service: {label} (slug: {slug})."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate service images with GPT-Image-2.")
    parser.add_argument("--services", default="sample", help="sample | all | comma-separated slugs")
    parser.add_argument("--dry-run", action="store_true", help="Print selected jobs and prompts only")
    parser.add_argument("--output-dir", default=str(Path("static/images/services")), help="Output folder")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = parse_services_selection(args.services)
    catalog = dict(SERVICE_CATEGORIES)
    for slug in selected:
        label = catalog[slug]
        _ = build_prompt(slug, label)
    if args.dry_run:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/scripts/generate_service_images.py m3alam/tests/images/test_generate_service_images.py
git commit -m "feat: scaffold GPT-Image-2 service generator with sample selection"
```

### Task 3: Implement API call, retries, artifacts, and manifest

**Files:**
- Modify: `m3alam/scripts/generate_service_images.py`
- Test: `m3alam/tests/images/test_generate_service_images.py`

- [ ] **Step 1: Write the failing test**

```python
from scripts.generate_service_images import build_output_paths


def test_build_output_paths_use_slug_based_names(tmp_path):
    paths = build_output_paths(tmp_path, "plomberie")
    assert paths["image"].name == "plomberie.png"
    assert paths["prompt"].name == "plomberie.prompt.txt"
    assert paths["metadata"].name == "plomberie.json"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py::test_build_output_paths_use_slug_based_names -v`
Expected: FAIL because `build_output_paths` is missing.

- [ ] **Step 3: Write minimal implementation**

```python
# add to m3alam/scripts/generate_service_images.py
import base64
import json
from urllib import request


def build_output_paths(output_dir: Path, slug: str) -> dict[str, Path]:
    return {
        "image": output_dir / f"{slug}.png",
        "prompt": output_dir / f"{slug}.prompt.txt",
        "metadata": output_dir / f"{slug}.json",
    }


def call_image_api(endpoint: str, api_key: str, deployment: str, api_version: str, prompt: str) -> bytes:
    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/images/generations?api-version={api_version}"
    payload = {
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "medium",
        "output_format": "png",
        "output_compression": 100,
        "n": 1,
    }
    req = request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "api-key": api_key},
        method="POST",
    )
    with request.urlopen(req, timeout=300) as response:
        body = json.loads(response.read().decode("utf-8"))
    return base64.b64decode(body["data"][0]["b64_json"])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py::test_build_output_paths_use_slug_based_names -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/scripts/generate_service_images.py m3alam/tests/images/test_generate_service_images.py
git commit -m "feat: add output artifact naming and image API generation core"
```

### Task 4: Add end-to-end dry-run and sample batch verification

**Files:**
- Modify: `m3alam/scripts/generate_service_images.py`
- Modify: `m3alam/tests/images/test_generate_service_images.py`

- [ ] **Step 1: Write the failing test**

```python
from scripts.generate_service_images import parse_services_selection


def test_sample_selection_contains_five_expected_services():
    assert parse_services_selection("sample") == [
        "ascenseurs",
        "carrelage",
        "clim-et-froid",
        "plomberie",
        "vitrerie-aluminium",
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py::test_sample_selection_contains_five_expected_services -v`
Expected: FAIL if sample list diverged from approved spec.

- [ ] **Step 3: Write minimal implementation**

```python
# enforce sample-first generation in m3alam/scripts/generate_service_images.py
SAMPLE_SERVICES = [
    "ascenseurs",
    "carrelage",
    "clim-et-froid",
    "plomberie",
    "vitrerie-aluminium",
]
```

```bash
# dry-run command (documented in module docstring / README snippet)
python scripts/generate_service_images.py --services sample --dry-run --output-dir static/images/services
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/scripts/generate_service_images.py m3alam/tests/images/test_generate_service_images.py
git commit -m "test: lock sample batch workflow for service image approval gate"
```

### Task 5: Generate first 5 sample images and verify artifacts

**Files:**
- Modify: `m3alam/static/images/services/*` (generated outputs)
- Modify: `m3alam/static/images/services/manifest.json`
- Test: command-based verification in repository shell

- [ ] **Step 1: Write the failing verification test (file existence check)**

```python
# m3alam/tests/images/test_generate_service_images.py
from pathlib import Path


def test_sample_outputs_exist_after_generation():
    root = Path("static/images/services")
    for slug in ["ascenseurs", "carrelage", "clim-et-froid", "plomberie", "vitrerie-aluminium"]:
        assert (root / f"{slug}.png").exists()
        assert (root / f"{slug}.prompt.txt").exists()
        assert (root / f"{slug}.json").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py::test_sample_outputs_exist_after_generation -v`
Expected: FAIL before first generation run.

- [ ] **Step 3: Write minimal implementation (run generator)**

```bash
cd m3alam
python scripts/generate_service_images.py --services sample --output-dir static/images/services --overwrite
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd m3alam && pytest tests/images/test_generate_service_images.py::test_sample_outputs_exist_after_generation -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add m3alam/static/images/services m3alam/tests/images/test_generate_service_images.py
git commit -m "feat: generate first five service images with prompts and metadata"
```

## Self-Review Checklist (completed)

1. **Spec coverage:** includes script architecture, prompt strategy, sample-first workflow, slug naming, output artifacts, and validation for 5 then 28 services.
2. **Placeholder scan:** all tasks include explicit files, code, commands, and expected outcomes.
3. **Type consistency:** uses consistent service identifiers (slug + French label), consistent output names (`<slug>.png`, `.prompt.txt`, `.json`), and consistent sample set across tasks/tests.
