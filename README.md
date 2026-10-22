# SentimentAI — V1.0

SentimentAI est une application web d’atelier DevOps pour enregistrer des textes et les retrouver dans un historique persistant. Cette version ne réalise aucune classification et n’intègre aucun modèle d’intelligence artificielle.

## Objectifs pédagogiques

- Structurer une application Python avec FastAPI et une interface HTML/CSS/JavaScript.
- Persister les données dans SQLite et isoler la base de test.
- Tester les routes et pages avec Pytest et FastAPI TestClient.
- Construire une image non privilégiée et conserver les données par volume Docker.
- Automatiser validation et publication GHCR avec GitHub Actions.

## Fonctionnalités

Page d’accueil, tableau de bord avec statistiques calculées, formulaire limité à 5 000 caractères, historique, détail et suppression confirmée. API REST documentée par OpenAPI. La classification intelligente est prévue pour une prochaine version, sans sentiment simulé en V1.

## Technologies et architecture

Python 3.12, FastAPI, Pydantic, Jinja2, SQLite, HTML/CSS/JavaScript, Pytest, Docker Compose et GitHub Actions.

- `app/main.py` : fabrique et assemblage FastAPI.
- `app/database.py` : initialisation et accès SQLite.
- `app/routers/` : routes API, santé et pages web.
- `app/templates/`, `app/static/` : interface.
- `tests/` : tests utilisant des bases temporaires.
- `.github/workflows/ci-cd.yml` : validation et publication.

## Prérequis et installation locale

Python 3.12 ou compatible, pip et Git. Docker Engine/Desktop avec Compose v2 pour le lancement conteneurisé.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux : source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Ouvrir http://localhost:8000. La base locale est `data/sentimentai.db`; `SENTIMENTAI_DATABASE_PATH` permet de la déplacer.

## Docker Compose

```bash
docker compose up --build
```

Ouvrir http://localhost:8000. Le volume nommé `sentimentai-data` garde les données après redémarrage.

```bash
docker compose logs -f sentimentai
docker compose down
```

Éviter `docker compose down -v` sauf pour supprimer aussi les données persistées.

## Tests

```bash
pytest -v
```

Chaque test dispose d’un fichier SQLite temporaire indépendant. Le test de persistance réutilise le fichier entre deux instances applicatives.

## API

Documentation interactive : `/docs`. Schéma : `/openapi.json`.

| Méthode | Route | Résultat |
| --- | --- | --- |
| GET | `/api/health` | État de l’application |
| GET | `/api/texts?limit=100&offset=0` | Liste, du plus récent |
| POST | `/api/texts` | Créer avec JSON `{"content":"…"}`, statut 201 |
| GET | `/api/texts/{id}` | Détail, ou 404 |
| DELETE | `/api/texts/{id}` | Supprimer, 204 ou 404 |

Le texte doit contenir un caractère non blanc et faire au plus 5 000 caractères. Les entrées invalides répondent 422.

## CI/CD et publication GHCR

Les pushs sur `main`/`master` et les pull requests exécutent installation, tests et build Docker. Le job de publication est séparé, dépend de la validation et ne s’exécute que pour un push sur ces branches. Il n’y a pas de publication depuis les pull requests externes.

Le job GHCR utilise `GITHUB_TOKEN` et `packages: write` uniquement dans le job de publication. L’image cible est `ghcr.io/<OWNER>/sentimentai`, avec un tag SHA complet et un tag de branche; `main` reçoit aussi `v1.0`. Vérifier que Actions et la publication de packages sont autorisés pour le dépôt.

## Versionnement Git et premier push

Le dossier de départ ne contenait pas de dépôt Git. Après vérification du dépôt distant et de son URL, exécuter :

```bash
git init
git add .
git commit -m "feat: deliver SentimentAI v1.0"
git branch -M main
git remote add origin https://github.com/OWNER/sentimentai.git
git push -u origin main
```

Remplacer OWNER. Pour les versions suivantes, travailler sur une branche par fonctionnalité et intégrer après validation. Exemple : `git tag v1.0.0 && git push origin v1.0.0`.

## Cloudflare

La publication GHCR ne déploie pas automatiquement sur Cloudflare. Cloudflare Containers est une piste si cette offre et l’architecture conviennent. Cloudflare Workers demanderait une adaptation de l’application et de son modèle d’exécution. Définir au préalable stockage persistant, réseau et pipeline. Selon l’option, fournir les identifiants du compte et la configuration Wrangler dans les secrets du dépôt ou de l’environnement cloud, jamais dans le code.

## Limites connues

- Aucun classement de sentiment, prétraitement, modèle ML ou API d’IA.
- SQLite convient au périmètre mono-instance; le multi-instance nécessitera un stockage partagé.
- Pas d’authentification ni de séparation par utilisateur dans cette V1.
- Dates stockées et affichées en UTC.

## Roadmap proposée

- **V1.0** : application web, stockage, historique, Docker et CI.
- **V2.0** : nettoyage et prétraitement.
- **V3.0** : première classification avec un modèle ML.
- **V4.0** : évaluation, métriques et tests.
- **V5.0** : visualisation des résultats et statistiques.
- **V6.0** : déploiement cloud automatisé et observabilité.
