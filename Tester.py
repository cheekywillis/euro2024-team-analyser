import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv(r"C:\Users\big-w\OneDrive\Desktop\Data\Euro2024.csv")

# Keep asking until a valid team is entered
while True:
    team = input("What team do you want to know about?: ").strip()

    team_matches = df[df["home_team"].str.contains(team, case=False, na=False) |
                      df["away_team"].str.contains(team, case=False, na=False)]

    if team_matches.empty:
        print(f"No matches found for '{team}'. Please try again.\n")
    else:
        df = team_matches
        break

# Clean attendance column
df["attendance"] = df["attendance"].str.replace(",", "")
df["attendance"] = pd.to_numeric(df["attendance"], errors='coerce')

# Reset index to start from 1
df = df.reset_index(drop=True)
df.index += 1

# List available stadiums
unique_stadiums = df["stadium"].dropna().unique()
print("\nStadiums this team has played at:")
for stadium in unique_stadiums:
    print(f"- {stadium}")

# Ask if user wants to filter by stadium
chosen_stadium = input("\nWant to filter by a specific stadium? Type its name or press Enter to skip: ").strip()

if chosen_stadium:
    df = df[df["stadium"].str.lower() == chosen_stadium.lower()]
    if df.empty:
        print(f"\nNo matches found for {team.title()} at '{chosen_stadium}'.")
        exit()

# Calculate goals scored
df["Total_goals"] = df.apply(
    lambda row: row["home_goals"] if team.lower() in row["home_team"].lower() else row["away_goals"],
    axis=1
)
total_goals = df["Total_goals"].sum()

# Calculate goals conceded
df["Goals_conceded"] = df.apply(
    lambda row: row["away_goals"] if team.lower() in row["home_team"].lower() else row["home_goals"],
    axis=1
)
total_conceded = df["Goals_conceded"].sum()

# Goal difference
goal_diff = total_goals - total_conceded

# Average attendance
avg_attendance = df["attendance"].mean()

# Output summary
print(f"\n📊 Summary for {team.title()}:")
if chosen_stadium:
    print(f"(Filtered to: {chosen_stadium})")
print(f"Total goals scored: {total_goals}")
print(f"Total goals conceded: {total_conceded}")
print(f"Goal difference: {goal_diff:+}")
print(f"Average attendance: {round(avg_attendance):,}")

# Display match results
print("\nMatch Results:")
for _, row in df.iterrows():
    print(f"{row['home_team']} {row['home_goals']} - {row['away_goals']} {row['away_team']}")

# Line chart of goals per match
plt.figure(figsize=(8, 4))
plt.plot(df.index, df["Total_goals"], marker='o', linestyle='-', label="Goals Scored")
plt.title(f"{team.title()} Goals Scored Per Match")
plt.xlabel("Match Number")
plt.ylabel("Goals")
plt.xticks(df.index)
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()
