"""
generate_synthetic_data.py

This script creates synthetic ACH transaction data and user data.
The goal is to simulate realistic looking ACH activity with some
built in fraud patterns that you can detect later with risk rules.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Number of fake users to create
NUM_USERS = 500

# Number of fake transactions to create
NUM_TRANSACTIONS = 5000

# Random number generator with a fixed seed
# This makes the data reproducible each time you run the script
RNG = np.random.default_rng(42)


def generate_users(num_users):
    """
    Create a DataFrame of synthetic users with:
    - user_id: unique identifier
    - account_age_days: how long they have had the account
    - is_new_user: flag for accounts younger than 30 days
    """

    # Create simple user ids like user_1, user_2, etc.
    user_ids = [f"user_{i + 1}" for i in range(num_users)]

    # Randomly assign account age between 0 and 365 days
    account_age_days = RNG.integers(0, 365, size=num_users)

    # Build DataFrame
    users = pd.DataFrame({
        "user_id": user_ids,
        "account_age_days": account_age_days,
    })

    # Boolean flag for new users
    users["is_new_user"] = users["account_age_days"] < 30

    return users


def random_background_return_code():
    """
    Assign a background ACH return code with some probability.
    Most transactions will not return at all. A small percentage
    get normal returns not tied to the specific fraud patterns.
    """

    # List of possible codes including None for no return
    codes = [None, "R01", "R02", "R03", "R10", "R29", "R51"]

    # Probabilities for each code
    # 90 percent of the time there is no return
    # Others are distributed across different codes
    weights = [0.9, 0.03, 0.02, 0.02, 0.015, 0.01, 0.005]

    return RNG.choice(codes, p=weights)


def generate_transactions(users, num_transactions):
    """
    Generate synthetic ACH transactions. This is where we inject
    specific fraud patterns:

    Pattern 1 - Instant ACH abuse
    Pattern 2 - First party fraud (R10 and R29)
    Pattern 3 - Synthetic identity (R02 and R03)
    """

    # Start all timestamps from a fixed base date
    base_time = datetime(2025, 1, 1)

    # List to hold each transaction as a dictionary
    records = []

    for i in range(num_transactions):
        # Randomly pick one user for this transaction
        user = users.sample(1).iloc[0]

        user_id = user["user_id"]
        account_age_days = int(user["account_age_days"])

        # Random timestamp within about 60 days
        minutes_offset = int(RNG.integers(0, 60 * 24 * 60))
        timestamp = base_time + timedelta(minutes=minutes_offset)

        # Random transaction amount between 10 and 1500 dollars
        amount = round(float(RNG.uniform(10, 1500)), 2)

        # Direction of movement from the platform perspective
        # debit: money going out of user account
        # credit: money coming into user account
        direction = RNG.choice(["debit", "credit"], p=[0.7, 0.3])

        # ACH type: PULL means pull from bank, PUSH means send to bank
        ach_type = RNG.choice(["PULL", "PUSH"], p=[0.8, 0.2])

        # Funding speed: instant vs standard
        funding_speed = RNG.choice(["standard", "instant"], p=[0.8, 0.2])

        # Device and IP info. These are where we will later
        # look for suspicious clustering.
        device_id = f"device_{RNG.integers(1, 300)}"
        ip_country = RNG.choice(["US", "CA", "GB", "MX", "BR"])

        # Default values for return behavior and labels
        return_code = None
        returned = False
        days_to_return = None
        fraud_pattern_type = None
        is_fraud_pattern = False

        # ----------------------------
        # Fraud pattern injection
        # ----------------------------

        # Pattern 1 - Instant ACH abuse for very new users
        # Logic: New users with instant funding and larger amounts
        # have a higher chance of NSF (R01) in a few days.
        if funding_speed == "instant" and account_age_days < 10 and amount > 500:
            if RNG.random() < 0.4:
                # About 40 percent of these risky transactions bounce
                return_code = "R01"        # Insufficient funds
                returned = True
                days_to_return = int(RNG.integers(1, 5))
                fraud_pattern_type = "instant_ach_abuse"
                is_fraud_pattern = True

        # Pattern 2 - First party fraud
        # Logic: Occasionally mark a transaction as unauthorized by customer.
        # R10 and R29 are "customer advises not authorized" type codes.
        if RNG.random() < 0.02:
            return_code = RNG.choice(["R10", "R29"])
            returned = True
            days_to_return = int(RNG.integers(1, 10))
            fraud_pattern_type = "first_party_fraud"
            is_fraud_pattern = True

        # Pattern 3 - Synthetic identity
        # Logic: Smaller percentage of transactions that fail because
        # the account is closed or does not exist. R02 and R03.
        if RNG.random() < 0.01:
            return_code = RNG.choice(["R02", "R03"])
            returned = True
            days_to_return = int(RNG.integers(1, 15))
            fraud_pattern_type = "synthetic_identity"
            is_fraud_pattern = True

        # If none of the fraud patterns triggered,
        # maybe assign a background return code
        if return_code is None:
            return_code = random_background_return_code()
            if return_code is not None:
                returned = True
                days_to_return = int(RNG.integers(1, 30))

        # Append the transaction record
        records.append({
            "transaction_id": f"txn_{i + 1}",
            "user_id": user_id,
            "timestamp_utc": timestamp.isoformat(),
            "direction": direction,
            "amount_usd": amount,
            "ach_type": ach_type,
            "funding_speed": funding_speed,
            "device_id": device_id,
            "ip_country": ip_country,
            "return_code": return_code,
            "returned": returned,
            "days_to_return": days_to_return,
            "fraud_pattern_type": fraud_pattern_type,
            "is_fraud_pattern": is_fraud_pattern,
            "account_age_days": account_age_days,
        })

    # Convert list of records into a DataFrame
    return pd.DataFrame(records)


def main():
    """
    Main entry point when the script is run directly.
    Generates users and transactions and writes them to CSV
    files in the data folder.
    """

    # Create users
    users = generate_users(NUM_USERS)

    # Create transactions based on users
    transactions = generate_transactions(users, NUM_TRANSACTIONS)

    # Save to CSV so we can load them in other scripts and notebooks
    users.to_csv("data/users.csv", index=False)
    transactions.to_csv("data/ach_transactions.csv", index=False)

    print("Generated data/users.csv and data/ach_transactions.csv")


if __name__ == "__main__":
    main()
