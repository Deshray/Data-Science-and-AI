play = int(input("Press 1 to play against computer, press 2 to play against a friend:"))
rounds = int(input("How many rounds do you want to play?"))

rps = ["r", "p", "s"]
rcount = 0
score_comp = 0
score_player1 = 0
score_player2 = 0

if play == 1:
    while rcount != rounds:
        print ("Press 's' for scissors, 'p' for paper, and 'r' for rock")
        player1 = str(input("Player 1, what do you choose?"))
        import random
        a = random.randint(0,2)
        computer = rps[a]
        print("The computer chose:", computer)
        if player1 == computer:
            print("This round is a tie")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
            score_comp = score_comp + 1
        elif computer == "r" and player1 == "s":
            print("The computer wins this round")
            rcount = rcount + 1
            score_comp = score_comp + 1
        elif computer == "r" and player1 == "p":
            print("You win this round")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
        elif computer == "s" and player1 == "r":
            print("You win this round")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
        elif computer == "s" and player1 == "p":
            print("The computer wins this round")
            rcount = rcount + 1 
            score_comp = score_comp + 1
        elif computer == "p" and player1 == "r":
            print("The computer wins this round")
            rcount = rcount + 1
            score_comp = score_comp + 1
        elif computer == "p" and player1 == "s":
            print("You win this round")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
        else:
            print("Please enter a valid option")
    if score_player1 == score_comp:
        print("It's a tie between both players")
    elif score_comp > score_player1:
        print("The computer wins the game:", score_player1, "-", score_comp)
    elif score_comp < score_player1:
        print("You win the game:", score_player1, "-", score_comp)
    
if play == 2:
    while rcount != rounds:
        print ("Press 's' for scissors, 'p' for paper, and 'r' for rock")
        player1 = str(input("Player 1, what do you choose?"))
        player2 = str(input("Player 2, what do you choose?"))
        if player1 == player2:
            print("This round is a draw")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
            score_player2 = score_player2 + 1
        elif player2 == "r" and player1 == "s":
            print("Player 2 wins this round")
            rcount = rcount + 1
            score_player2 = score_player2 + 1
        elif player2 == "r" and player1 == "p":
            print("Player 1 wins this round")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
        elif player2 == "s" and player1 == "r":
            print("Player 1 wins this round")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
        elif player2 == "s" and player1 == "p":
            print("Player 2 wins this round")
            rcount = rcount + 1
            score_player2 = score_player2 + 1
        elif player2 == "p" and player1 == "r":
            print("Player 2 wins this round")
            rcount = rcount + 1
            score_player2 = score_player2 + 1
        elif player2 == "p" and player1 == "s":
            print("Player 1 wins this round")
            rcount = rcount + 1
            score_player1 = score_player1 + 1
        else:
            print("Please enter a valid option")
    if score_player2 == score_player1:
        print("It's a tie between both players")
    elif score_player2 > score_player1:
        print("Player 2 wins the game:", score_player1, "-", score_player2)
    elif score_player1 > score_player2:
        print("Player 1 wins the game:", score_player1, "-", score_player2)
