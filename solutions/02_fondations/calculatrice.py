# Solution : Calculatrice Simple 🧮

# 1. Demander les nombres à l'utilisateur
# Note : input() renvoie TOUJOURS une chaîne (str). 
# On doit donc la convertir en float pour faire des calculs.
nombre1 = float(input("Entrez le premier nombre : "))
nombre2 = float(input("Entrez le deuxième nombre : "))

# 2. Calculs et Affichage
print(f"Addition : {nombre1} + {nombre2} = {nombre1 + nombre2}")
print(f"Soustraction : {nombre1} - {nombre2} = {nombre1 - nombre2}")
print(f"Multiplication : {nombre1} * {nombre2} = {nombre1 * nombre2}")

# Gérer le cas de la division par zéro (concept que nous verrons plus tard)
if nombre2 != 0:
    print(f"Division : {nombre1} / {nombre2} = {nombre1 / nombre2}")
    print(f"Division entière : {nombre1} // {nombre2} = {nombre1 // nombre2}")
    print(f"Modulo : {nombre1} % {nombre2} = {nombre1 % nombre2}")
else:
    print("Division impossible par zéro !")
