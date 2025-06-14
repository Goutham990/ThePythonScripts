import random

def rock_paper_scissors():
    choices = ['rock', 'paper', 'scissors']
    while True:
        user = input("Choose rock, paper, or scissors (or 'quit'): ").lower()
        if user == 'quit':
            break
        if user not in choices:
            print("Invalid choice!")
            continue
        computer = random.choice(choices)
        print(f"Computer chose: {computer}")
        if user == computer:
            print("Tie!")
        elif (user == 'rock' and computer == 'scissors') or \
             (user == 'scissors' and computer == 'paper') or \
             (user == 'paper' and computer == 'rock'):
            print("You win!")
        else:
            print("Computer wins!")

rock_paper_scissors()

