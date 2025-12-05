"""
risk_rules.py

This module defines simple rule based logic to detect suspicious ACH
transactions and assign a risk score. Each rule returns the subset of
rows that match, and we then combine all rule hits to produce a
risk_score per transaction.

The goal is to show how a payments risk analyst might think in rules.
"""

import pandas as pd


def rule_high_instant_ach_for_new_users(df):
    """
    Flag transactions where:
    - funding_speed is instant
    - account_age_days is less than 30 (new user)
    - amount_usd is above a threshold (here 500)

    This simulates risk from instant ACH for new users with larger tickets.
    """

    mask = (
        (df["funding_speed"] == "instant") &
        (df["account_age_days"] < 30) &
        (df["amount_usd"] > 500)
    )

    # Return only matching rows with a rule_name column added
    return df[mask].assign(rule_name="high_instant_ach_for_new_users")


def rule_rapid_high_risk_returns(df):
    """
    Flag transactions where:
    - there is a return
    - return occurs within 5 days
    - return_code is one of R01, R10, or R29

    These codes are often associated with insufficient funds or authorization issues.
    Fast returns on these codes can indicate fraud or risky behavior.
    """

    mask = (
        (df["returned"] == True) &
        (df["days_to_return"].notna()) &
        (df["days_to_return"] <= 5) &
        (df["return_code"].isin(["R01", "R10", "R29"]))
    )

    return df[mask].assign(rule_name="rapid_high_risk_returns")


def rule_device_shared_by_many_users(df, min_users=5):
    """
    Flag transactions that come from devices used by many different user_ids.

    This can indicate:
    - account farms
    - synthetic identity rings
    - shared devices abused to create multiple accounts

    min_users controls how many distinct users must share a device
    before we consider it suspicious.
    """

    # Count distinct users per device_id
    device_user_counts = (
        df.groupby("device_id")["user_id"]
        .nunique()
        .reset_index()
        .rename(columns={"user_id": "unique_users"})
    )

    # Devices used by at least min_users distinct users
    suspicious_devices = device_user_counts[
        device_user_counts["unique_users"] >= min_users
    ]["device_id"]

    # Flag all transactions that come from those devices
    mask = df["device_id"].isin(suspicious_devices)

    return df[mask].assign(rule_name="device_shared_by_many_users")


def score_transactions(df):
    """
    Apply all rules to the DataFrame and compute a risk_score per transaction.

    Steps:
    1. Run each rule function to get its alerts.
    2. Concatenate all alerts into a single DataFrame.
    3. Count how many rules fired per transaction_id.
    4. Merge that count back onto the original DataFrame as risk_score.

    Returns:
    - df_scored: original df with a risk_score column added.
    - alerts_df: long table of every rule hit (for audit and debugging).
    """

    # List of rule functions to apply
    rules = [
        rule_high_instant_ach_for_new_users,
        rule_rapid_high_risk_returns,
        rule_device_shared_by_many_users,
    ]

    # Apply each rule and collect the results in a list
    alerts_list = []

    for rule in rules:
        rule_alerts = rule(df)
        alerts_list.append(rule_alerts)

    # Combine all rule hits into one DataFrame
    alerts_df = pd.concat(alerts_list, ignore_index=True)

    # Each row in alerts_df is a rule hit. Count how many hits per transaction.
    scores = (
        alerts_df.groupby("transaction_id")["rule_name"]
        .count()
        .reset_index()
        .rename(columns={"rule_name": "risk_score"})
    )

    # Merge the scores back to the original df
    df_scored = df.merge(scores, on="transaction_id", how="left")

    # Transactions with no rule hits get NaN risk_score, set those to 0
    df_scored["risk_score"] = df_scored["risk_score"].fillna(0).astype(int)

    return df_scored, alerts_df
