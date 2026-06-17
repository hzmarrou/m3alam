# Design Spec — Génération d’images services (GPT-Image-2) pour M3alam

## 1. Objectif
Générer des images premium pour chaque service M3alam, en s’inspirant du workflow existant dans `purview-learn/slides`, avec GPT-Image-2 (Azure OpenAI), afin d’alimenter les cartes services de l’UI.

## 2. Contexte validé
- Style visuel: **3D isométrique professionnel**.
- Format: **carré 1024x1024** (adapté aux cartes services type Zoofy).
- Dossier de sortie: `m3alam/static/images/services`.
- Nommage: **slug** (`plomberie.png`, `ascenseurs.png`, etc.).
- Processus: générer **5 échantillons d’abord**, puis lot complet 28 services après validation.

## 3. Approche validée
Réutiliser le pattern du script Purview (rate-limit, retries, manifest, prompt files, metadata) avec une adaptation orientée “services”.

## 4. Architecture de génération
### 4.1 Script principal
Créer un script Python dédié dans M3alam qui:
- lit la config Azure OpenAI depuis `.env`,
- charge la liste de services (slug + libellé FR),
- assemble prompt partagé + prompt spécifique service,
- appelle l’API images Azure OpenAI (GPT-Image-2),
- écrit image + prompt + metadata + manifest.

### 4.2 Entrées
- Variables env:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_IMAGE_DEPLOYMENT` (défaut `gpt-image-2`)
  - `AZURE_OPENAI_IMAGE_API_VERSION` (défaut `2024-02-01`)
- Liste de services M3alam (28 entrées):
  - ascenseurs, carrelage, clim-et-froid, demolition, depannage, electricite, electricite-auto, electro-menager, electronique, encadrement, etancheite, ferronnerie, jardinier, maconnerie, marbre, mecanique, menuiserie, parabole, peinture, piscine, platrier, plomberie, pneumatiques, serrurerie, surveillance-et-alarmes, tapisserie, transport, vitrerie-aluminium.

### 4.3 Sorties
Dans `m3alam/static/images/services`:
- `<slug>.png`
- `<slug>.prompt.txt`
- `<slug>.json`
- `manifest.json`

## 5. Stratégie de prompts
### 5.1 Prompt partagé (style global)
- 3D isometric professional icon/scene,
- clean neutral background,
- high contrast for marketplace card usage,
- centered subject with safe margins,
- premium modern visual language consistent across all services.

### 5.2 Prompt spécifique service
Injecter pour chaque service:
- nom du métier en français,
- outils/objets représentatifs,
- éviter texte dans l’image (ou texte minimal),
- garder cohérence de lumière et angle.

## 6. Paramètres d’exécution
- `--services`: `all` ou liste (`plomberie,carrelage,...`)
- `--size`: `1024x1024`
- `--quality`: configurable (par défaut qualité adaptée coût/qualité)
- `--output-dir`: `m3alam/static/images/services`
- `--overwrite`: regénération volontaire
- `--dry-run`: validation sans appel API

## 7. Qualité et validation
### 7.1 Étape 1 — échantillon
Générer 5 services:
- ascenseurs
- carrelage
- clim-et-froid
- plomberie
- vitrerie-aluminium

### 7.2 Validation humaine
Confirmer:
- cohérence style,
- lisibilité en carte,
- adéquation métier.

### 7.3 Étape 2 — lot complet
Générer les 28 services après approbation.

## 8. Non-régression
- Aucun changement backend métier.
- Aucun changement route/permissions.
- Changement limité au pipeline d’assets visuels et intégration front.

## 9. Critères d’acceptation
- 5 échantillons générés dans le bon dossier avec noms slug.
- Prompts + metadata + manifest présents.
- Après validation, 28 images générées et complètes.
- Images homogènes, premium, exploitables en cartes services.
