# Solution : Convertisseur de Devises 💶➡️💵

# Utilisation du Type Hinting pour plus de clarté
def convertir_euros_en_dollars(montant_eur: float, taux_change: float = 1.10) -> float:
    """Convertit un montant d'euros vers dollars selon un taux de change."""
    return montant_eur * taux_change

# Cas 1 : Utilisation du taux par défaut (1.10)
montant = 100
resultat_defaut = convertir_euros_en_dollars(montant)
print(f"{montant}€ équivalent à {resultat_defaut:.2f}$ au taux par défaut.")

# Cas 2 : Utilisation d'un taux spécifique (ex: 1.05)
resultat_specifique = convertir_euros_en_dollars(montant, 1.05)
print(f"{montant}€ équivalent à {resultat_specifique:.2f}$ au taux spécifique de 1.05.")
