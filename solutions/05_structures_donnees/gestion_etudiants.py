# Solution : Gestion d'Étudiants 🎓

etudiants = {
    "Alice": [12, 15, 18],
    "Bob": [8, 10, 9],
    "Charles": [14, 16, 12]
}

# Parcourir et calculer les moyennes
for nom, notes in etudiants.items():
    moyenne = sum(notes) / len(notes)
    print(f"L'étudiant {nom} a une moyenne de {moyenne:.2f}")

# Bonus : List Comprehension pour filtrer
# On crée une liste des noms dont la moyenne (sum/len) est >= 10
etudiants_admis = [nom for nom, notes in etudiants.items() if (sum(notes)/len(notes)) >= 10]

print(f"\nÉtudiants admis : {', '.join(etudiants_admis)}")
