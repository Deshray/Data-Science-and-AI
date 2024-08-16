import matplotlib.pyplot as plt

# Sagas and transformations
sagas = [
    "Saiyan Saga", "Namek Saga", "Frieza Saga", 
    "Android Saga", "Cell Saga", "Buu Saga", 
    "Battle of Gods", "Resurrection F", "Universe 6", 
    "Future Trunks", "Universe Survival"
]

# Goku's power levels and transformations
goku_power_levels = [
    8000,    # Kaio-Ken (Saiyan Saga)
    90000,   # Base (Namek Saga)
    3000000, # Super Saiyan (Frieza Saga)
    150000000, # Super Saiyan (Android Saga)
    300000000, # Super Saiyan 2 (Cell Saga)
    1500000000, # Super Saiyan 3 (Buu Saga)
    15000000000, # Super Saiyan God (Battle of Gods)
    20000000000, # Super Saiyan Blue (Resurrection F)
    30000000000, # Super Saiyan Blue (Universe 6)
    50000000000, # Super Saiyan Blue + Kaioken (Future Trunks)
    100000000000, # Ultra Instinct (Universe Survival)
]
goku_transformations = [
    "Kaio-Ken", "Base", "Super Saiyan", 
    "Super Saiyan", "Super Saiyan 2", "Super Saiyan 3", 
    "Super Saiyan God", "Super Saiyan Blue", "Super Saiyan Blue",
    "SSB + Kaioken", "Ultra Instinct"
]

# Vegeta's power levels and transformations
vegeta_power_levels = [
    18000,   # Base (Saiyan Saga)
    24000,   # Zenkai Boost (Namek Saga)
    250000,  # Super Saiyan (Frieza Saga)
    150000000, # Super Saiyan (Android Saga)
    225000000, # Super Vegeta (Cell Saga)
    1500000000, # Majin Vegeta (Buu Saga)
    12000000000, # Super Saiyan God-like (Battle of Gods)
    19000000000, # Super Saiyan Blue (Resurrection F)
    25000000000, # Super Saiyan Blue (Universe 6)
    45000000000, # Super Saiyan Blue (Future Trunks)
    80000000000, # Super Saiyan Blue Evolution (Universe Survival)
]
vegeta_transformations = [
    "Base", "Zenkai Boost", "Super Saiyan", 
    "Super Saiyan", "Super Vegeta", "Majin Vegeta", 
    "SSG-like", "Super Saiyan Blue", "Super Saiyan Blue", 
    "Super Saiyan Blue", "SSB Evolution"
]

plt.figure(figsize=(12, 8))

# Plotting the power levels
plt.plot(sagas, goku_power_levels, label='Goku', marker='o')
plt.plot(sagas, vegeta_power_levels, label='Vegeta', marker='o')

# Adding annotations for Goku's transformations
for i, txt in enumerate(goku_transformations):
    plt.annotate(txt, (sagas[i], goku_power_levels[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Adding annotations for Vegeta's transformations
for i, txt in enumerate(vegeta_transformations):
    plt.annotate(txt, (sagas[i], vegeta_power_levels[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Logarithmic scale for better visualization
plt.yscale('log')

plt.xlabel('Saga')
plt.ylabel('Power Level (log scale)')
plt.title('Goku vs. Vegeta Power Level Tracker')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.show()