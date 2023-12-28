word = str(input("Player 1, enter a word:"))
x = [str(a) for a in str(word)]
gaps = len(x)

line = []
for i in range (gaps):
    line.append("_")
    y = " ".join(line)
print y

chance = ["H" , "A" , "N" , "G" , "M" , "A" , "N"]
print (chance)

wrong = 0
while wrong < 7:
    letter = str(input("Player 2, please enter a letter:"))
    c = 0
    counter = 0
    empty = line
    pos = 0
    for c in x:
        if c == letter:
            line[pos] = letter
            counter = counter + 1
        pos = pos + 1
    if counter == 0:
        chance[wrong] = "X"
        wrong = wrong + 1
        print ("You guessed wrong")
    else:
        print("You guessed right")
    print (line)
    print (chance)
    if line == x:
        print ("Congratulation Player 2, you guessed the word")
print ("You lose")
