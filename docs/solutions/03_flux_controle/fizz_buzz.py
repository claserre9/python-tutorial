# Solution : FizzBuzz 🐝

# Utilisation de range(1, 51) car la borne de fin est EXCLUE
for n in range(1, 51):
    # Important : Vérifier la condition la plus restrictive EN PREMIER
    if n % 3 == 0 and n % 5 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

# Alternative moderne (Python 3.10+) :
# for n in range(1, 51):
#     match (n % 3 == 0, n % 5 == 0):
#         case (True, True): print("FizzBuzz")
#         case (True, False): print("Fizz")
#         case (False, True): print("Buzz")
#         case _: print(n)
