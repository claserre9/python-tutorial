# Solution : Le Zoo Polygone 🦁🦁

class Animal:
    def __init__(self, nom: str):
        self.nom = nom
    
    def parler(self):
        # On définit l'interface, mais on ne l'implémente pas encore
        pass

class Lion(Animal):
    def parler(self):
        print(f"{self.nom} rugit : Roar !")

class Oiseau(Animal):
    def parler(self):
        print(f"{self.nom} siffle : Cui cui !")

class Serpent(Animal):
    def parler(self):
        print(f"{self.nom} siffle : Sss !")

# Liste d'animaux (Polymorphisme)
animaux = [
    Lion("Simba"),
    Oiseau("Tweety"),
    Serpent("Kaa")
]

# Une seule boucle pour tous les types d'animaux !
for animal in animaux:
    animal.parler()
