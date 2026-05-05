# Solution : L'Inspecteur Gadget 🕵️‍♂️

def inspecter_objet(obj):
    """Affiche dynamiquement les attributs d'un objet et leurs valeurs."""
    print(f"--- Inspection de l'objet de type : {type(obj).__name__} ---")
    
    # 1. On récupère TOUT ce qu'il y a dans l'objet
    tout_le_contenu = dir(obj)
    
    # 2. On filtre pour ne garder que ce qui nous intéresse
    for nom in tout_le_contenu:
        # On ignore les méthodes spéciales (__init__, etc.)
        if nom.startswith("__"):
            continue
            
        valeur = getattr(obj, nom)
        
        # On ne veut pas les méthodes (ce qui est "appelable"), seulement les données
        if not callable(valeur):
            print(f"- Attribut '{nom}' : {valeur}")

# --- Test ---
class Voiture:
    def __init__(self, marque, modele, annee):
        self.marque = marque
        self.modele = modele
        self.annee = annee
    
    def rouler(self):
        print("Vroum !")

ma_auto = Voiture("Tesla", "Model 3", 2023)
inspecter_objet(ma_auto)
