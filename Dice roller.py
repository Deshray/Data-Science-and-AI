import random
#print("\u25CF \u250C \u2500 \u2510 \u2502 \u2514 \u2518")
#┌ ─ ┐ │ └ ┘
"┌────────────┐"
"│            │"
"│            │"
"│            │"
"│            │"
"└────────────┘"
dicetable = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘",),
    2: ("┌─────────┐",
        "│    ●    │",
        "│         │",
        "│    ●    │",
        "└─────────┘",),
    3: ("┌─────────┐",
        "│    ●    │",
        "│    ●    │",
        "│    ●    │",
        "└─────────┘",),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘",),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘",),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘",),
}

numobtained = []
total = 0
numofdice = int(input("How many dice?"))
for die in range (numofdice):
    numobtained.append(random.randint(1,6))
for line in range(5):
    for die in numobtained:
        print(dicetable.get(die)[line], end = "")
    print()

for die in numobtained:
    total += die
print("Total = ", total)