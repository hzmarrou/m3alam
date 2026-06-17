---
title: "M3alam — Marketplace artisans au Maroc"
subtitle: "Pourquoi, parcours client, parcours artisan et supervision admin"
lang: fr
---

# M3alam

## Marketplace artisans · Maroc

Une plateforme pour publier une demande de travaux, recevoir des offres claires et choisir un artisan fiable.

**Capture à ajouter :** page d'accueil — `http://127.0.0.1:8010/`

---

# Le problème : pourquoi M3alam ?

Trouver un artisan fiable reste souvent informel, lent et peu transparent.

- Les clients demandent autour d'eux, comparent difficilement les offres et manquent de visibilité.
- Les artisans sérieux dépendent du bouche-à-oreille et perdent du temps à chercher des demandes qualifiées.
- La plateforme doit créer confiance, clarté et suivi sans compliquer l'expérience.

**Idée clé :** structurer la relation sans remplacer le contact humain.

---

# La solution

M3alam organise trois parcours simples :

1. **Client** — publie une demande claire.
2. **Artisan** — répond avec une offre lisible.
3. **Admin** — supervise la qualité et modère la plateforme.

La valeur vient de la mise en relation contrôlée : les coordonnées restent masquées jusqu'à l'acceptation d'une offre.

**Capture à ajouter :** section “Processus” — `http://127.0.0.1:8010/`

---

# Parcours client — 1/2

## Créer un compte et publier une demande

Le client arrive sur une interface premium, choisit le métier adapté, puis décrit son besoin en français.

Étapes principales :

- inscription client ;
- choix de la catégorie de travaux ;
- description du besoin, ville et budget éventuel ;
- publication de la demande.

**Pages à montrer :**

- inscription client — `http://127.0.0.1:8010/comptes/inscription-client/`
- nouvelle demande — `http://127.0.0.1:8010/travaux/nouveau/`

---

# Parcours client — 2/2

## Comparer les offres et choisir

Après publication, le client consulte les offres reçues sur la demande.

Il peut comparer :

- le prix proposé ;
- le message de l'artisan ;
- le statut de l'offre ;
- l'action d'acceptation.

Une fois l'offre acceptée, la relation peut sortir de la plateforme avec les coordonnées débloquées.

**Pages à montrer :**

- détail demande avec offres — `http://127.0.0.1:8010/travaux/<id>/`
- accepter une offre — `http://127.0.0.1:8010/offres/accepter/<offer_id>/`

---

# Parcours artisan — 1/2

## Créer son espace professionnel

L'artisan crée un compte dédié et renseigne son profil professionnel.

Le parcours met en avant :

- le métier ;
- la ville ;
- les compétences ;
- la disponibilité ;
- la vérification email/téléphone.

Objectif : aider les artisans sérieux à être visibles et mieux qualifiés.

**Page à montrer :** inscription artisan — `http://127.0.0.1:8010/comptes/inscription-artisan/`

---

# Parcours artisan — 2/2

## Trouver des demandes et envoyer une offre

L'artisan consulte les demandes ouvertes, ouvre une fiche de travaux, puis envoie une offre.

Étapes principales :

- voir les demandes disponibles ;
- ouvrir le détail d'une demande ;
- comprendre catégorie, ville et description ;
- envoyer une offre avec prix et message.

**Pages à montrer :**

- demandes ouvertes — `http://127.0.0.1:8010/travaux/`
- détail demande — `http://127.0.0.1:8010/travaux/<id>/`
- envoyer une offre — `http://127.0.0.1:8010/offres/creer/<job_id>/`

---

# Parcours admin — 1/2

## Superviser la plateforme

L'admin dispose d'un portail simple pour voir l'activité clé.

Indicateurs affichés :

- nombre d'utilisateurs ;
- nombre d'artisans ;
- demandes ouvertes ;
- derniers logs d'administration.

Objectif : garder une vue rapide sur la santé de la marketplace.

**Page à montrer :** portail admin — `http://127.0.0.1:8010/portail-admin/`

---

# Parcours admin — 2/2

## Modération et confiance

Le rôle admin soutient la qualité du réseau.

Actions prévues :

- masquer une demande non conforme ;
- suspendre un utilisateur problématique ;
- conserver un historique des actions sensibles ;
- maintenir une expérience fiable pour clients et artisans.

**Pages/actions à mentionner :**

- masquer une demande — `http://127.0.0.1:8010/portail-admin/masquer-travail/<job_id>/`
- suspendre un utilisateur — `http://127.0.0.1:8010/portail-admin/suspendre-utilisateur/<user_id>/`

---

# Pages à capturer pour la démo

1. **Accueil / proposition de valeur** — `http://127.0.0.1:8010/`
2. **Services** — `http://127.0.0.1:8010/`
3. **Inscription client** — `/comptes/inscription-client/`
4. **Publier une demande** — `/travaux/nouveau/`
5. **Demandes ouvertes** — `/travaux/`
6. **Détail demande + offres** — `/travaux/<id>/`
7. **Inscription artisan** — `/comptes/inscription-artisan/`
8. **Envoyer une offre** — `/offres/creer/<job_id>/`
9. **Contact client après acceptation** — `/offres/contact-client/<offer_id>/`
10. **Portail admin** — `/portail-admin/`

Pour les URLs avec `<id>`, créez une demande et une offre de test avant de prendre les captures.

