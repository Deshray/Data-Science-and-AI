import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
anime_ratings_df = pd.read_csv(r"C:/Users/Dibyendu Kumar Ray/Desktop/Anime_ratings.csv")

# Function to identify the top 10 highest-rated anime
def top_rated_anime(df):
    top_anime = df.nlargest(10, 'Score')[['Title', 'Score']]
    print("Top 10 Highest-Rated Anime:")
    print(top_anime)

# Function to visualize genre distribution
def genre_distribution(df):
    # Split the genres into a list of genres for each anime
    genre_list = df['Genres'].dropna().str.split(',')
    genre_series = pd.Series([genre.strip() for sublist in genre_list for genre in sublist])
    
    # Plot the distribution of genres
    genre_series.value_counts().plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title('Distribution of Genres in Anime Dataset')
    plt.xlabel('Genre')
    plt.ylabel('Number of Anime')
    plt.xticks(rotation=45, ha='right')
    plt.show()

# Function to filter and display anime by release year
def anime_by_release_year(df):
    # Prompt the user to input the year
    year = input("Enter the year you want to explore: ")
    
    # Filter the DataFrame based on the input year
    filtered_anime = df[df['Release Date'].str.contains(str(year), na=False)][['Title', 'Score', 'Genres']]
    
    # Check if any anime were found for the given year
    if not filtered_anime.empty:
        print(f"Anime Released in {year}:")
        print(filtered_anime)
        
        # Optionally, show the top 10 most popular anime by score for the given year
        top_anime_year = filtered_anime.nlargest(10, 'Score')[['Title', 'Score', 'Genres']]
        print(f"\nTop 10 Highest-Rated Anime Released in {year}:")
        print(top_anime_year)
    else:
        print(f"No anime found for the year {year}.")

# Apply the functions
top_rated_anime(anime_ratings_df)
genre_distribution(anime_ratings_df)
anime_by_release_year(anime_ratings_df)
