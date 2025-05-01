import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    # Load the data
    df = pd.read_csv(r"C:\Users\big-w\OneDrive\Desktop\Data\Euro2024.csv")

    # Ask for input
    team = input("What team do you want to know about?: ").strip()

    # Filter for matches where the team played
    df = df[df["home_team"].str.contains(team, case=False, na=False) | df["away_team"].str.contains(team, case=False, na=False)]

    # Validate input
    if df.empty:
        print(f"\nNo matches found for '{team}'. Please check the team name.")
        return

    # Clean attendance
    df["attendance"] = df["attendance"].str.replace(",", "")
    df["attendance"] = pd.to_numeric(df["attendance"])

    # Reset index to start from 1
    df = df.reset_index(drop=True)
    df.index += 1

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
    goal_difference = total_goals - total_conceded

    # Average attendance
    avg_attendance = df["attendance"].mean()

    # Output summary
    print(f"\n📊 Summary for {team.title()}:")
    print(f"Total goals scored: {total_goals}")
    print(f"Total goals conceded: {total_conceded}")
    print(f"Goal difference: {goal_difference:+}")  # + sign shows +/- automatically
    print(f"Average attendance: {round(avg_attendance):,}")

    # Display match results
    print("\nMatch Results:")
    for _, row in df.iterrows():
        print(f"{row['home_team']} {row['home_goals']} - {row['away_goals']} {row['away_team']}")

if __name__ == "__main__":
    main()
