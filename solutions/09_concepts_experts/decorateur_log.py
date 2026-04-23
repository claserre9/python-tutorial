# Solution : Décorateur de Log 📝
from functools import wraps

def log(fonction):
    # @wraps(fonction) permet de conserver les métadonnées de la fonction d'origine
    @wraps(fonction)
    def wrapper(*args, **kwargs):
        print(f"--- Appel de '{fonction.__name__}' ---")
        print(f"Arguments positionnels : {args}")
        print(f"Arguments par mot-clé : {kwargs}")
        
        # On appelle la fonction d'origine
        resultat = fonction(*args, **kwargs)
        
        print(f"Résultat retourné : {resultat}")
        return resultat
    
    return wrapper

# --- Tests ---
@log
def calculer(a, b):
    return a + b

@log
def saluer(nom, politesse="Bonjour"):
    return f"{politesse} {nom} !"

calculer(10, 5)
print("\n")
saluer("Alice", politesse="Salut")
