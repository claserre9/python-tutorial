"""TODO : définir User et Tache en SQLAlchemy 2.0 async.

User :
- id (PK)
- email (unique, indexed)
- hashed_password

Tache :
- id (PK)
- titre
- terminee (bool, défaut False)
- created_at (datetime, défaut utcnow)
- owner_id (FK -> users.id)

Relation 1-N : User.taches <-> Tache.owner (cascade delete).
"""
