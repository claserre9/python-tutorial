# Solution : Tests Unitaires avec pytest ✅
import pytest

def calculer_aire_rectangle(largeur: float, hauteur: float) -> float:
    """Calcule l'aire d'un rectangle et lève une erreur si dimensions négatives."""
    if largeur <= 0 or hauteur <= 0:
        raise ValueError("Les dimensions doivent être positives.")
    return largeur * hauteur

# --- Les Tests ---

def test_aire_cas_entier():
    assert calculer_aire_rectangle(10, 5) == 50

def test_aire_cas_flottant():
    # Rappel : pytest.approx() est utile pour comparer les flottants (précision machine)
    assert calculer_aire_rectangle(2.5, 4) == 10.0

def test_aire_erreur_negative():
    with pytest.raises(ValueError):
        calculer_aire_rectangle(-5, 10)

def test_aire_erreur_zero():
    with pytest.raises(ValueError):
        calculer_aire_rectangle(0, 10)

# Pour lancer : 'pytest solutions/10_tests_qualite/test_math.py'
if __name__ == "__main__":
    print("Exécutez ce fichier avec la commande 'pytest' !")
