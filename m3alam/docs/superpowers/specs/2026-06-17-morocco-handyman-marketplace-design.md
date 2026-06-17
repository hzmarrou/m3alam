# Design Spec — Plateforme de mise en relation artisans/clients (Maroc, FR)

## 1. Objectif
Construire une plateforme web (MVP) pour le marché marocain, en français, similaire au modèle de marketplace de services à domicile:
- Les **artisans** s'inscrivent et créent leur profil.
- Les **clients** publient des demandes de travaux.
- Les **admins** gèrent et modèrent la plateforme via un portail dédié.

**Exigence de langue:** toute l'interface (site public, espace client, espace artisan, portail admin, emails système) est en **français** pour le MVP.

## 2. Portée MVP
### Inclus
- Application web uniquement.
- Authentification multi-rôles: `client`, `artisan`, `admin`.
- Inscription artisan avec vérification email/téléphone.
- Publication de demandes de travaux par les clients.
- Soumission d'offres par les artisans.
- Acceptation d'une offre par le client.
- Déverrouillage des coordonnées après acceptation.
- Portail admin: gestion utilisateurs/artisans + modération demandes/offres.

### Exclu (MVP)
- Chat in-app.
- Applications mobiles natives.
- Paiements intégrés et facturation avancée.

## 3. Architecture technique (recommandée et validée)
- **Backend + Frontend:** Django (monolithe Python).
- **Base de données:** PostgreSQL.
- **Approche:** applications Django séparées par domaine.

### Apps Django proposées
1. `accounts` — comptes, rôles, authentification, vérification contact.
2. `jobs` — demandes de travaux publiées par les clients.
3. `offers` — offres soumises par les artisans.
4. `admin_portal` — écrans admin personnalisés et actions de modération.
5. `core_ui` — composants UI, thème, pages publiques.

## 4. Modèle de données (niveau conceptuel)
### User
- `id`, `email`, `phone`, `password_hash`
- `role` (`client|artisan|admin`)
- `is_active`, `created_at`, `updated_at`

### ArtisanProfile
- `user_id` (1-1 avec User)
- `full_name`, `skills[]`, `city`, `bio`
- `verification_status` (`pending|verified`)
- `availability_status`

### JobRequest
- `id`, `client_id`
- `category`, `title`, `description`, `city`
- `budget_min` (optionnel), `budget_max` (optionnel)
- `status` (`open|assigned|closed|hidden`)
- `created_at`

### JobOffer
- `id`, `job_id`, `artisan_id`
- `proposed_price`, `message`
- `status` (`pending|accepted|rejected|withdrawn`)
- `created_at`

### AdminAuditLog
- `id`, `admin_id`, `action_type`, `target_type`, `target_id`, `reason`, `created_at`

## 5. Parcours utilisateur
### 5.1 Parcours artisan
1. Création de compte artisan.
2. Vérification email/téléphone.
3. Complétion du profil (métier, ville, disponibilité).
4. Consultation des demandes ouvertes.
5. Envoi d'offres.

### 5.2 Parcours client
1. Création de compte client.
2. Publication d'une demande (catégorie, description, ville, photos optionnelles).
3. Réception d'offres d'artisans.
4. Acceptation d'une offre.
5. Déverrouillage des coordonnées pour prise de contact hors plateforme.

### 5.3 Parcours admin
1. Gestion comptes (activation/suspension).
2. Vérification qualité profils artisans.
3. Modération demandes/offres (spam, abus, contenu non conforme).
4. Suivi activité via vues de supervision simples.
5. Historisation des actions sensibles dans un audit log.

## 6. Règles métier clés
- Un client peut avoir plusieurs demandes ouvertes.
- Un artisan peut soumettre plusieurs offres, mais au plus une offre par demande.
- Une seule offre peut être acceptée par demande.
- L'acceptation d'une offre passe la demande à `assigned`.
- Les coordonnées complètes restent masquées jusqu'à acceptation.
- Les admins peuvent masquer/fermer du contenu non conforme.

## 7. Gestion des erreurs et sécurité
- Validation stricte des champs côté serveur.
- Messages d'erreur utilisateur en français, explicites et non techniques.
- Contrôles d'accès par rôle sur chaque vue/endpoint.
- Réponses claires pour 401/403/404.
- Journalisation des erreurs serveur et des actions admin sensibles.

## 8. Localisation (FR obligatoire)
- Langue par défaut et unique du MVP: `fr`.
- Aucun texte UI en anglais dans les templates, validations, emails, pages d'erreur et notifications.
- Formatage localisé: dates, heures et libellés adaptés au français.
- Les données libres saisies par utilisateurs peuvent rester multilingues, mais le produit parle français.

## 9. UI/Branding (palette validée)
### Tokens couleurs
- `--color-black: #000000`
- `--color-white: #FFFFFF`
- `--color-grey-1: #29282A`
- `--color-creme: #F7F6F9`
- `--color-primary: #8142FF`
- `--color-primary-light: #AA80FF`
- `--color-grey-3: #706D72`
- `--color-grey-2: #434045`
- `--color-grey-5: #CAC9CF`
- `--color-lime: #DAFF01` (optionnel)
- `--color-link: #8142FF`

### Principes
- Interface majoritairement claire (`#FFFFFF`/`#F7F6F9`) avec accents violets.
- Contraste texte élevé pour lisibilité.
- Liens et CTA principaux en `#8142FF`.
- Version responsive mobile-first pour usage terrain.

## 10. Tests (MVP)
- Tests modèles: contraintes et transitions d'état.
- Tests permissions: séparation stricte client/artisan/admin.
- Tests flux principal:
  - publication demande
  - soumission offre
  - acceptation offre
  - déverrouillage coordonnées
- Tests admin: modération et audit log.
- Tests i18n: vérification qu'aucune clé/chaîne anglaise n'apparaît dans les parcours principaux.

## 11. Critères de succès MVP
- Un artisan peut s'inscrire et proposer une offre sans intervention manuelle.
- Un client peut publier une demande et accepter une offre.
- Un admin peut suspendre un compte et masquer un contenu.
- L'expérience est 100% en français et respecte la palette de marque définie.
