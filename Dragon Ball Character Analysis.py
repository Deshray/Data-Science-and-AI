import pandas as pd
import matplotlib.pyplot as plt

dragon_ball_df = pd.read_csv(r"C:\Users\Dibyendu Kumar Ray\Desktop\Dragon_Ball_Data_Set.csv")

dragon_ball_df['Power_Level'] = pd.to_numeric(dragon_ball_df['Power_Level'], errors='coerce')
dragon_ball_df = dragon_ball_df.dropna(subset=['Power_Level'])

def top_power_levels(df):
    top_characters = df.nlargest(10, 'Power_Level')[['Character', 'Power_Level', 'Saga_or_Movie']]
    print("Top 10 Characters by Power Level:")
    print(top_characters)

# Apply the function
top_power_levels(dragon_ball_df)
# Function to visualize power levels within a specific saga
def power_level_distribution(df, saga):
    saga_data = df[df['Saga_or_Movie'] == saga]
    plt.figure(figsize=(10, 6))
    plt.barh(saga_data['Character'], saga_data['Power_Level'], color='orange')
    plt.xlabel('Power Level')
    plt.ylabel('Character')
    plt.title(f'Power Level Distribution in {saga}')
    plt.show()

power_level_distribution(dragon_ball_df, 'Saiyan Saga')

def compare_sagas(df):
    saga_comparison = df.groupby('Saga_or_Movie')['Power_Level'].mean().sort_values()
    saga_comparison.plot(kind='bar', figsize=(12, 7), color='lightgreen')
    plt.title('Average Power Level Across Different Sagas')
    plt.xlabel('Saga or Movie')
    plt.ylabel('Average Power Level')
    plt.xticks(rotation=45, ha='right')
    plt.show()

compare_sagas(dragon_ball_df)
