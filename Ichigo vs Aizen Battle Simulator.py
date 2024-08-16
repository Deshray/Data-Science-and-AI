import matplotlib.pyplot as plt

# Define transformations with their power multipliers for each character
ichigo_transformations = {
    "Base": 1,
    "Shinigami": 2,
    "Bankai": 5,
    "Fullbring": 10,
    "Vasto Lorde": 40,
    "Mugetsu": 100,
    "Quincy Powers": 200,
    "Hollowfication": 300,
    "Final Getsuga Tensho": 500
}

aizen_transformations = {
    "Base": 1,
    "Shinigami": 2,
    "Sakanade": 5,
    "Kyoka Suigetsu": 10,
    "Hogyoku": 20,
    "Awakened Hogyoku": 80,
    "Perfect Form": 200,
    "Espada Powers": 300,
    "Final Form": 500
}

# Define moves with base damage values and cooldowns (in rounds)
ichigo_moves = {
    "Getsuga Tensho": {"damage": 15, "cooldown": 0},
    "Cero": {"damage": 20, "cooldown": 2},
    "Grand Ray Cero": {"damage": 50, "cooldown": 3},
    "Tensa Zangetsu": {"damage": 30, "cooldown": 2}
}

aizen_moves = {
    "Kurohitsugi": {"damage": 15, "cooldown": 0},
    "Sokatsui": {"damage": 20, "cooldown": 2},
    "Mugestu": {"damage": 50, "cooldown": 3},
    "Hado 90": {"damage": 30, "cooldown": 2}
}

# Function to calculate move effectiveness
def calculate_damage(attacker, move, transformation):
    base_damage = move["damage"]
    power_multiplier = transformation
    return base_damage * power_multiplier

# Function to conduct a battle round
def battle_round(player1, player2, move1, move2, transformation1, transformation2):
    damage1 = calculate_damage(player1, move1, transformation1)
    damage2 = calculate_damage(player2, move2, transformation2)

    # Apply damage to each player's health
    player1["health"] -= damage2
    player2["health"] -= damage1

    # Handle move cooldowns
    player1["cooldowns"][move1_name] = move1["cooldown"]
    player2["cooldowns"][move2_name] = move2["cooldown"]

    print(f"\n{player1['name']} used {move1_name} ({player1['transformation_name']}) and dealt {damage1} damage.")
    print(f"{player2['name']} used {move2_name} ({player2['transformation_name']}) and dealt {damage2} damage.")
    print(f"{player1['name']}'s Health: {player1['health']}")
    print(f"{player2['name']}'s Health: {player2['health']}\n")

    return player1["health"], player2["health"]

# Function to get player's choice
def get_choice(prompt, choices):
    choice = None
    while choice not in choices:
        choice = input(prompt).title()
        if choice not in choices:
            print(f"Invalid choice. Choose from {choices}.")
    return choice

# Initialize players
player1 = {"name": "", "health": 50000, "cooldowns": {}}
player2 = {"name": "", "health": 50000, "cooldowns": {}}

# Player 1 chooses character and transformation
print("Player 1, choose your character: Ichigo or Aizen")
player1["name"] = get_choice("Character: ", ["Ichigo", "Aizen"])

if player1["name"] == "Ichigo":
    transformations1 = ichigo_transformations
    moves1 = ichigo_moves
else:
    transformations1 = aizen_transformations
    moves1 = aizen_moves

# Display available transformations
print("\nAvailable transformations:")
for transformation in transformations1:
    print(transformation)

transformation1_name = get_choice("\nChoose your transformation: ", list(transformations1.keys()))
player1["transformation_name"] = transformation1_name
transformation1 = transformations1[transformation1_name]

# Player 2 chooses character and transformation
print("\nPlayer 2, choose your character: Ichigo or Aizen")
player2["name"] = get_choice("Character: ", ["Ichigo", "Aizen"])

if player2["name"] == "Ichigo":
    transformations2 = ichigo_transformations
    moves2 = ichigo_moves
else:
    transformations2 = aizen_transformations
    moves2 = aizen_moves

# Display available transformations
print("\nAvailable transformations:")
for transformation in transformations2:
    print(transformation)

transformation2_name = get_choice("\nChoose your transformation: ", list(transformations2.keys()))
player2["transformation_name"] = transformation2_name
transformation2 = transformations2[transformation2_name]

# Initialize health history for plotting
health_history = {
    "rounds": [],
    "player1_health": [],
    "player2_health": []
}

# Battle until one player's health is zero or less
round_number = 1
while player1["health"] > 0 and player2["health"] > 0:
    print(f"\n--- Round {round_number} ---")

    # Display available moves considering cooldowns
    print(f"\n{player1['name']}, choose your move:")
    available_moves1 = {move: details for move, details in moves1.items() if player1["cooldowns"].get(move, 0) == 0}
    for move in available_moves1.keys():
        print(move)
    move1_name = get_choice("Move: ", list(available_moves1.keys()))
    move1 = available_moves1[move1_name]

    print(f"\n{player2['name']}, choose your move:")
    available_moves2 = {move: details for move, details in moves2.items() if player2["cooldowns"].get(move, 0) == 0}
    for move in available_moves2.keys():
        print(move)
    move2_name = get_choice("Move: ", list(available_moves2.keys()))
    move2 = available_moves2[move2_name]

    # Conduct battle round
    health1, health2 = battle_round(player1, player2, move1, move2, transformation1, transformation2)

    # Update cooldowns
    player1["cooldowns"] = {move: max(0, cooldown - 1) for move, cooldown in player1["cooldowns"].items()}
    player2["cooldowns"] = {move: max(0, cooldown - 1) for move, cooldown in player2["cooldowns"].items()}

    # Update health history for plotting
    health_history["rounds"].append(round_number)
    health_history["player1_health"].append(health1)
    health_history["player2_health"].append(health2)

    round_number += 1

# Determine winner and display quote
if player1["health"] > 0:
    print(f"{player1['name']} wins!")
    if player1["name"] == "Ichigo":
        print("I am not a hero. I'm just a guy with a lot of power.")
    else:
        print("My ambition knows no bounds. Victory is inevitable.")
else:
    print(f"{player2['name']} wins!")
    if player2["name"] == "Ichigo":
        print("I am not a hero. I'm just a guy with a lot of power.")
    else:
        print("My ambition knows no bounds. Victory is inevitable.")

# Plot health over rounds
plt.figure(figsize=(10, 6))
plt.plot(health_history["rounds"], health_history["player1_health"], label=f"{player1['name']}'s Health")
plt.plot(health_history["rounds"], health_history["player2_health"], label=f"{player2['name']}'s Health")
plt.xlabel('Round Number')
plt.ylabel('Health')
plt.title('Ichigo vs Aizen Battle Health Over Rounds')
plt.legend()
plt.grid(True)
plt.show()
