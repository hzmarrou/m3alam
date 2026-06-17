# Design Spec — Refonte UI Premium M3alam (FR, Maroc)

## 1. Objectif
Transformer l'interface actuelle en site web premium, moderne et orienté conversion, tout en gardant le backend métier existant (inscription artisan, demande client, portail admin).

## 2. Résultat attendu
- Design attractif et crédible dès le premier écran.
- Conversion prioritaire: pousser le client à publier une demande rapidement.
- Respect strict de la langue française sur toute l'interface.
- Respect strict de la palette marque:
  - `#000000`, `#FFFFFF`, `#29282A`, `#F7F6F9`
  - `#8142FF`, `#AA80FF`, `#706D72`, `#434045`, `#CAC9CF`
  - `#DAFF01` (optionnel)
  - liens: `#8142FF`

## 3. Approche validée
Approche retenue: **Tailwind + style shadcn-like (sans casser Django templates)**.

Concrètement:
- Conserver les templates Django server-side.
- Ajouter une couche design system inspirée shadcn:
  - composants propres,
  - hiérarchie visuelle nette,
  - cartes/panneaux premium,
  - états UI cohérents.
- Migrer le CSS minimal actuel vers une architecture utilitaire moderne et réutilisable.

## 4. Architecture UI
### 4.1 Fondations
- `base.html` devient layout principal premium:
  - header sticky,
  - container responsive,
  - footer crédibilité.
- Système de tokens design centralisé (couleurs, radius, ombres, spacing, typographie).
- Variables marque exposées et utilisées partout.

### 4.2 Composants
- `navbar`: navigation claire + CTA principal visible.
- `hero`: message fort + CTA “Publier ma demande”.
- `trust-strip`: preuves de confiance (artisans vérifiés, réponse rapide, garantie).
- `service-cards`: catégories de travaux.
- `step-cards`: parcours 3 étapes.
- `testimonial/ratings`: bloc crédibilité.
- `job-card` + `offer-card`: cartes lisibles et actionnables.
- `form-kit`: champs, labels, erreurs, focus/hover states.
- `badge-kit`: statuts visuels (ouverte, attribuée, etc.).

### 4.3 Pages concernées (MVP redesign)
- `home.html`
- `jobs/job_list.html`
- `jobs/job_detail.html`
- `jobs/job_form.html`
- `accounts/login.html`
- `accounts/signup_client.html`
- `accounts/signup_artisan.html`
- `offers/offer_form.html`
- `offers/client_contact.html`
- `admin_portal/dashboard.html`

## 5. UX et conversion
### 5.1 Home (priorité conversion client)
- Above-the-fold:
  - proposition de valeur claire,
  - CTA primaire très visible,
  - trust badges immédiats.
- Ensuite:
  - catégories populaires,
  - “comment ça marche” en 3 étapes,
  - bloc confiance.

### 5.2 Job list / detail
- Passage liste brute -> cartes premium.
- CTA “Envoyer une offre” plus clair pour artisans.
- CTA “Accepter” mieux mis en avant pour client propriétaire de la demande.

### 5.3 Formulaires
- Inputs modernisés (taille, paddings, contraste, focus ring).
- Messages d'erreur clairs en français.
- CTA distinct primaire/secondaire.

## 6. Règles de non-régression
- Aucune modification de logique métier backend.
- Aucune modification des permissions/rôles.
- Aucune modification des routes.
- UI seulement (templates + static assets + copy).

## 7. Accessibilité et responsive
- Mobile-first (320+), puis tablet/desktop.
- Contraste suffisant texte/fond.
- Focus visible clavier.
- Hiérarchie H1/H2/H3 propre.
- Cibles clic confortables.

## 8. Gestion des erreurs (UI)
- Uniformiser style des erreurs/forbidden dans un design cohérent.
- Garder wording français explicite.
- Pas de fallback silencieux visuel; afficher un état clair.

## 9. Stratégie test
- Tests de rendu pages clés (status 200).
- Assertions de présence CTA attendus.
- Assertions anti-anglais sur pages critiques.
- Tests smoke responsive visuel manuel (mobile + desktop).

## 10. Critères d'acceptation
- Le site paraît premium et moderne (niveau marketplace production-ready).
- Home pousse clairement à publier une demande.
- Les preuves de confiance sont visibles au-dessus de la ligne de flottaison.
- Le style est cohérent sur toutes les pages principales.
- 100% français.
- Palette marque respectée partout.
