import matplotlib.pyplot as plt

# Define transformations with their power multipliers for each character
goku_transformations = {
    "Base": 1,
    "Kaio-Ken": 2,
    "Super Saiyan": 5,
    "Super Saiyan 2": 10,
    "Super Saiyan 3": 40,
    "Super Saiyan God": 100,
    "Super Saiyan Blue": 200,
    "Ssb Kaioken": 300,
    "Ultra Instinct": 500
}

vegeta_transformations = {
    "Base": 1,
    "Zenkai Boost": 2,
    "Super Saiyan": 5,
    "Super Vegeta": 10,
    "Majin Vegeta": 20,
    "SSG-like": 80,
    "Super Saiyan Blue": 200,
    "Ssb Evo": 300,
    "Ultra Ego": 500
}

# Define moves with base damage values and cooldowns (in rounds)
goku_moves = {
    "Kamehameha": {"damage": 10, "cooldown": 0},
    "Spirit Bomb": {"damage": 15, "cooldown": 2},
    "Dragon Fist": {"damage": 50, "cooldown": 3},
    "Kaioken Attack": {"damage": 25, "cooldown": 2}
}

vegeta_moves = {
    "Galick Gun": {"damage": 10, "cooldown": 0},
    "Final Flash": {"damage": 15, "cooldown": 2},
    "Big Bang Attack": {"damage": 25, "cooldown": 2},
    "Final Shine Attack": {"damage": 50, "cooldown": 3}
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
print("Player 1, choose your character: Goku or Vegeta")
player1["name"] = get_choice("Character: ", ["Goku", "Vegeta"])

if player1["name"] == "Goku":
    transformations1 = goku_transformations
    moves1 = goku_moves
else:
    transformations1 = vegeta_transformations
    moves1 = vegeta_moves

# Display available transformations
print("\nAvailable transformations:")
for transformation in transformations1:
    print(transformation)

transformation1_name = get_choice("\nChoose your transformation: ", list(transformations1.keys()))
player1["transformation_name"] = transformation1_name
transformation1 = transformations1[transformation1_name]

# Player 2 chooses character and transformation
print("\nPlayer 2, choose your character: Goku or Vegeta")
player2["name"] = get_choice("Character: ", ["Goku", "Vegeta"])

if player2["name"] == "Goku":
    transformations2 = goku_transformations
    moves2 = goku_moves
else:
    transformations2 = vegeta_transformations
    moves2 = vegeta_moves

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
    if player1["name"] == "Goku":
        print("Even the Lowest-Born Can Outdo the Elite.")
    else:
        print("My Motivation Was to Be the Best, as I Always Have Been.")
else:
    print(f"{player2['name']} wins!")
    if player2["name"] == "Goku":
        print("Even the Lowest-Born Can Outdo the Elite.")
    else:
        print("My Motivation Was to Be the Best, as I Always Have Been.")

# Plot health over rounds
plt.figure(figsize=(10, 6))
plt.plot(health_history["rounds"], health_history["player1_health"], label=f"{player1['name']}'s Health")
plt.plot(health_history["rounds"], health_history["player2_health"], label=f"{player2['name']}'s Health")
plt.xlabel('Round Number')
plt.ylabel('Health')
plt.title('Goku vs Vegeta Battle Health Over Rounds')
plt.legend()
plt.grid(True)
plt.show()
