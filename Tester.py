import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import the data
df = pd.read_csv(r"C:\Users\big-w\OneDrive\Desktop\Data\Euro2024.csv")

# Ask for input
team = input("What team do you want to know about?: ").strip()

# Find the games (case-insensitive)
df = df[df["home_team"].str.contains(team, case=False, na=False) | df["away_team"].str.contains(team, case=False, na=False)]

# Clean the attendance column
df["attendance"] = df["attendance"].str.replace(",", "")
df["attendance"] = pd.to_numeric(df["attendance"])

# Reset the index and start from 1
df = df.reset_index(drop=True)
df.index += 1

# Total goals scored (case-insensitive match)
df["Total_goals"] = df.apply(
    lambda row: row["home_goals"] if team.lower() in row["home_team"].lower() else row["away_goals"], axis=1
)
total_goals = df["Total_goals"].sum()
print(f"Total goals scored by {team.title()}: {total_goals}")

# Total goals conceded
df["Goals_conceded"] = df.apply(
    lambda row: row["away_goals"] if team.lower() in row["home_team"].lower() else row["home_goals"], axis=1
)
total_conceded = df["Goals_conceded"].sum()
print(f"Total goals conceded by {team.title()}: {total_conceded}")

# Display the data
print(df[["home_team", "home_goals", "away_goals", "away_team"]])
