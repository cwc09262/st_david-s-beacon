import pandas as pd
import random

INPUT_CSV = "full_results.csv"
OUTPUT_CSV = "results_scored.csv"


# Columns that define uniqueness
UNIQUE_COLS = ["Query", "Method", "Similarity Score (%)", "Text", "Psalm Num", "Verse"]

def add_new_results():
    """
    Merge new rows from INPUT_CSV into OUTPUT_CSV
    without overwriting existing HumanScore values,
    using the combination of UNIQUE_COLS as identity.
    """
    input_df = pd.read_csv(INPUT_CSV)
    if "HumanScore" not in input_df.columns:
        input_df["HumanScore"] = pd.NA

    try:
        scored_df = pd.read_csv(OUTPUT_CSV)
        print(f"Loaded existing scored file: {OUTPUT_CSV}")
    except FileNotFoundError:
        # First run — just save input
        input_df.to_csv(OUTPUT_CSV, index=False)
        print("Created new scored file.")
        return

    # Identify new rows by checking all UNIQUE_COLS
    merged = scored_df.merge(
        input_df,
        on=UNIQUE_COLS,
        how='right',
        indicator=True
    )

    new_rows = merged[merged['_merge'] == 'right_only'].drop(columns=['_merge'])

    if new_rows.empty:
        print("No new results to add.")
        return

    # Append new rows
    combined = pd.concat([scored_df, new_rows], ignore_index=True)
    combined.to_csv(OUTPUT_CSV, index=False)
    print(f"Added {len(new_rows)} new results for scoring.")

def load_data():
    # try loading the scored file first
    try:
        df = pd.read_csv(OUTPUT_CSV)
        print(f"Loaded existing scored file: {OUTPUT_CSV}")
        return df
    except FileNotFoundError:
        pass

    # otherwise load the original input
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"Loaded input CSV: {INPUT_CSV}")
    except FileNotFoundError:
        print("Could not find input CSV:", INPUT_CSV)
        exit()

    # add HumanScore column if missing
    if "HumanScore" not in df.columns:
        df["HumanScore"] = pd.NA

    return df

def save_data(df):
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Progress saved to {OUTPUT_CSV}")

def get_unscored_index(df):
    df_unscored = df[df["HumanScore"].isna()]
    if df_unscored.empty:
        return None, 0
    return random.choice(df_unscored.index.tolist()), len(df_unscored)

def show_row(df, idx, remaining, percent):
    row = df.loc[idx]
    print("\n======================================")
    print(f"UNSCORED PSALMS LEFT: {remaining}, ({percent}%)")
    print("QUERY:")
    print(row["Query"])
    print("\nRESULT:")
    print(row["Verse"])
    print(f"\nPsalm: {row['Psalm Num']}")
    print("======================================")
    print("Rate this result 0–10 (or 'q' to quit)")

def get_score():
    while True:
        x = input("Score: ").strip()
        if x.lower() == "q":
            return None
        if x.isdigit() and 0 <= int(x) <= 10:
            return int(x)
        print("Invalid input — enter a number 0–10 or 'q' to quit.")

    
def main():
    add_new_results()
    df = load_data()
    print("\nReady to evaluate!")
    print("Press 'q' to quit at any time.\n")

    while True:
        idx, remaining = get_unscored_index(df)
        if idx is None:
            print("\nAll rows have been scored. 🎉")
            save_data(df)
            break

        show_row(df, idx, remaining, remaining/len(df))
        score = get_score()

        if score is None:
            print("\nQuitting. Saving progress…")
            save_data(df)
            break

        df.at[idx, "HumanScore"] = score
        save_data(df)

if __name__ == "__main__":
    main()
