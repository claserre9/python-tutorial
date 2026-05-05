# Solution : Gestion Bancaire Simple 🏦

class CompteBancaire:
    """Modélise un compte bancaire avec dépôt et retrait."""
    
    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self.titulaire = titulaire
        self.solde = solde_initial

    def deposer(self, montant: float):
        self.solde += montant
        print(f"Dépôt de {montant}€ effectué.")

    def retirer(self, montant: float):
        if montant <= self.solde:
            self.solde -= montant
            print(f"Retrait de {montant}€ effectué.")
        else:
            print(f"Retrait refusé : solde insuffisant ({self.solde}€).")

    def afficher_solde(self):
        print(f"Le solde de {self.titulaire} est de {self.solde:.2f}€.")

# --- Tests ---
compte_alice = CompteBancaire("Alice", 100.0)
compte_alice.deposer(50.0)
compte_alice.retirer(30.0)
compte_alice.retirer(200.0) # Doit afficher "Refusé"
compte_alice.afficher_solde()
