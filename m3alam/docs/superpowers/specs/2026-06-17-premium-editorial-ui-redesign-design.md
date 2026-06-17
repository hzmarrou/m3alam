# Design Spec — Refonte UI premium éditoriale M3alam

## 1. Objectif
Refondre uniquement l’interface M3alam pour obtenir une plateforme plus premium, moderne, cohérente et intentionnellement designée, sans changer la logique métier ni les flux existants.

## 2. Audit UI actuel
- Le hero actuel utilise trop de violet et donne une impression de template.
- Les cartes services sont textuelles, répétitives et n’exploitent pas les images générées.
- La hiérarchie typographique manque de contraste éditorial.
- Les espacements, bordures, boutons et formulaires ne sont pas assez systématisés.
- Les écrans opérationnels (jobs, offres, admin) ne partagent pas encore une vraie grammaire premium.

## 3. Direction validée
Utiliser un système visuel premium éditorial dans les templates Django existants:
- base neutre: blanc, crème, noir, gris foncé;
- violet contrôlé pour CTA, focus, liens et accents;
- pas de surcharge de gradients;
- surfaces calmes, bordures fines, ombres très subtiles;
- typographie plus affirmée, espacements plus généreux;
- intégration cohérente des images services.

## 4. Contraintes
- Garder Django server-rendered templates.
- Ne pas introduire un nouveau framework.
- Ne pas modifier les permissions, routes ou logique métier.
- Garder l’expérience française.
- Utiliser les images existantes dans `static/images/services`.

## 5. Système visuel
### 5.1 Tokens
- Couleurs: respecter la palette validée.
- Rayons: plus sobres et cohérents.
- Ombres: rares, douces, utilisées pour profondeur contrôlée.
- Espacement: rythme vertical plus généreux sur pages publiques, plus compact sur écrans opérationnels.
- Typographie: titres plus éditoriaux, body calme et lisible, metadata secondaire.

### 5.2 Composants
- `site-header`: nav sticky plus sobre, CTA clair.
- `hero-editorial`: hero premium neutre avec accent violet contrôlé.
- `trust-bar`: preuves de confiance en grille.
- `service-card`: image service + libellé FR + CTA/metadata.
- `form-panel`: formulaires plus lisibles, champs stables, focus violet.
- `job-card` / `offer-card`: cartes structurées par titre, metadata, statut, action.
- `admin-kpi`: panneaux admin opérationnels.
- `badge`: statuts lisibles et cohérents.

## 6. Intégration images services
- Source: `m3alam/static/images/services/<slug>.png`.
- Correspondance via `jobs.service_catalog.SERVICE_CATEGORIES`.
- Landing page: chaque service affiche son image dans une zone visuelle propre.
- Les images doivent être recadrées avec `object-fit: contain`, fond neutre, et préserver un rendu premium responsive.
- Les formulaires gardent les libellés texte pour simplicité et accessibilité.

## 7. Écrans à traiter
Priorité haute:
- `base.html`
- `home.html`
- `jobs/job_form.html`
- `accounts/login.html`
- `accounts/signup_client.html`
- `accounts/signup_artisan.html`

Priorité moyenne:
- `jobs/job_list.html`
- `jobs/job_detail.html`
- `offers/offer_form.html`
- `offers/client_contact.html`

Priorité cohérence:
- `admin_portal/dashboard.html`

## 8. Accessibilité et responsive
- Contraste fort pour texte et CTA.
- Focus visible sur liens, boutons, inputs.
- Cartes services: grille responsive desktop, 2 colonnes tablette, 1 colonne mobile.
- Formulaires: largeur maximale contrôlée, champs confortables, labels lisibles.
- Admin: panels empilables mobile.

## 9. Tests et validation
- Tests de rendu pour la page d’accueil.
- Tests que les images services sont présentes avec bons slugs.
- Tests que les libellés français restent visibles.
- `python manage.py check`.
- Inspection live sur `http://127.0.0.1:8010/`.

## 10. Critères d’acceptation
- L’interface est nettement plus premium, sobre et professionnelle.
- Les services utilisent les images générées.
- Le violet est contrôlé, pas dominant.
- Les pages publiques, formulaires, cartes et admin partagent le même système visuel.
- Les flux existants restent fonctionnels.
