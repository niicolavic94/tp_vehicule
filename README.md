# tp_vehicule

L'API utilise SQLAlchemy ORM : les modèles de base sont déclarés dans
`src/parc_vehicule/database/models.py`, et les services CRUD exécutent leurs
opérations directement avec une session SQLAlchemy. Aucun dépôt intermédiaire
n'est utilisé par les routes.

## Lancement

Le projet nécessite Python 3.14 ou supérieur et une base MySQL configurée.
Copiez `.env.example` vers `.env`, puis adaptez les paramètres de connexion.
La création ou la mise à jour du schéma se fait avec Alembic :

```powershell
poetry install
poetry run alembic upgrade head
poetry run uvicorn --app-dir src parc_vehicule.main:app --reload
```

Pour exécuter les tests :

```powershell
poetry run pytest
```
