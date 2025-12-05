"""
run_scoring.py

This script ties things together:
- Reads the generated synthetic ACH transactions
- Applies the risk rules to compute a risk_score
- Writes the scored data and alerts to CSV files
- Prints a small sample to the console
"""

import pandas as pd
from risk_rules import score_transactions


def main():
    """
    Main function that reads the input data, scores it, and saves outputs.
    """

    # Read the synthetic transactions created by generate_synthetic_data.py
    df = pd.read_csv("data/ach_transactions.csv")

    print(f"Loaded {len(df)} transactions")

    # Apply the risk scoring logic
    df_scored, alerts_df = score_transactions(df)

    # Show a small sample of scored transactions for quick inspection
    print("Sample of scored transactions:")
    print(
        df_scored[
            [
                "transaction_id",
                "user_id",
                "amount_usd",
                "funding_speed",
                "return_code",
                "risk_score",
            ]
        ].head(10)
    )

    # Save the scored transactions so we can use them in notebooks and analysis
    df_scored.to_csv("data/ach_transactions_scored.csv", index=False)

    # Save the detailed alerts table which contains every rule hit
    alerts_df.to_csv("data/alerts.csv", index=False)

    print("Saved data/ach_transactions_scored.csv and data/alerts.csv")


if __name__ == "__main__":
    main()
