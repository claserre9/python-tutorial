# Solution Final : Votre Mini-API de Tâches 📝🌐
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# 1. On crée l'application FastAPI
app = FastAPI(title="Ma To-Do API")

# 2. Définition du modèle de données (Schema)
class Task(BaseModel):
    id: int
    titre: str
    complete: bool = False

# 3. Base de données factice (en mémoire)
tasks_db: List[Task] = []

# 4. Route pour récupérer toutes les tâches
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

# 5. Route pour ajouter une tâche
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    tasks_db.append(task)
    return {"message": "Tâche ajoutée avec succès !", "task": task}

# --- Pour lancer le serveur ---
# uvicorn solutions.11_dev_web.api_tasks:app --reload
# Allez sur http://127.0.0.1:8000/docs pour tester !

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
