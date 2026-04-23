# Solution : Lecteur Sécurisé de Données 📖🛡️

# 1. Création du fichier pour le test (si absent)
with open("nombres.txt", "w") as f:
    f.write("10\n20\nabc\n30\n")

# 2. Lecture et calcul
somme = 0
try:
    with open("nombres.txt", "r") as f:
        for ligne in f:
            try:
                # .strip() retire les espaces et sauts de ligne (\n)
                nombre = int(ligne.strip())
                somme += nombre
            except ValueError:
                print(f"Ignoré : '{ligne.strip()}' n'est pas un nombre.")
    
    print(f"\nLa somme finale est : {somme}")

except FileNotFoundError:
    print("Erreur : Le fichier 'nombres.txt' est introuvable !")
except Exception as e:
    print(f"Une erreur inconnue est survenue : {e}")
