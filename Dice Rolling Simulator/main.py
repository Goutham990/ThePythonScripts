import random

def dice_simulator():
    n = int(input("How many dice do you want to roll? "))
    result = [random.randint(1, 6) for _ in range(n)]
    print("You rolled:", result, "Total:", sum(result))

dice_simulator()
