# M3alam

Marketplace de mise en relation entre clients et artisans au Maroc, avec une interface en français et un portail de supervision admin.

## Exécution locale

### Prérequis
- Python 3.11+
- Git

### Lancer l'application en local (Windows PowerShell)

```powershell
git clone https://github.com/hzmarrou/m3alam.git
cd m3alam\m3alam
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8010
```

Ouvrir ensuite : `http://127.0.0.1:8010/`

## Parcours des personas

### Client
1. S’inscrire (`/comptes/inscription-client/`)
2. Publier une demande (`/travaux/nouveau/`)
3. Consulter les offres (`/travaux/<id>/`)
4. Accepter une offre (`/offres/accepter/<offer_id>/`)

### Artisan
1. S’inscrire (`/comptes/inscription-artisan/`)
2. Parcourir les demandes (`/travaux/`)
3. Ouvrir un détail de demande (`/travaux/<id>/`)
4. Envoyer une offre (`/offres/creer/<job_id>/`)

### Admin
1. Superviser la plateforme (`/portail-admin/`)
2. Masquer une demande non conforme (`/portail-admin/masquer-travail/<job_id>/`)
3. Suspendre un utilisateur (`/portail-admin/suspendre-utilisateur/<user_id>/`)
