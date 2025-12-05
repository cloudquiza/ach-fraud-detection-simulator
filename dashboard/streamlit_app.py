"""
streamlit_app.py

Interactive ACH Fraud Dashboard

This Streamlit app reads the scored ACH transaction data and displays:
- High level KPIs (total transactions, return rate, high risk rate)
- Filters (risk score, funding speed, return code)
- Charts (risk score distribution, return code distribution)
- Tables (top risky users, suspicious devices)

This simulates the kind of internal dashboard a Payments Risk Analyst
might use at a company like Coinbase.
"""

import pandas as pd
import streamlit as st
from pathlib import Path


# ----------------------------------------------------
# DATA LOADING
# ----------------------------------------------------
@st.cache_data
def load_data():
    """
    Load the scored transactions and alerts from the data folder.
    Cached for performance.
    """

    # Resolve project root: this file is in /dashboard, so go up one directory
    base_path = Path(__file__).resolve().parents[1]

    scored_path = base_path / "data" / "ach_transactions_scored.csv"
    alerts_path = base_path / "data" / "alerts.csv"

    df_scored = pd.read_csv(scored_path)
    alerts_df = pd.read_csv(alerts_path)

    return df_scored, alerts_df


# ----------------------------------------------------
# MAIN APP
# ----------------------------------------------------
def main():
    st.set_page_config(
        page_title="ACH Fraud Dashboard",
        layout="wide",
    )

    st.title("ACH Fraud Detection Simulator")
    st.caption(
        "Synthetic ACH data, rule-based scoring, fraud pattern detection — "
        "built as a practice project for a Payments Risk Analyst role."
    )

    # Load data
    df_scored, alerts_df = load_data()

    # ----------------------------------------------------
    # TOP KPIs
    # ----------------------------------------------------
    total_tx = len(df_scored)
    total_users = df_scored["user_id"].nunique()
    overall_return_rate = df_scored["returned"].mean()

    # Define high risk as risk_score >= 2 (adjustable)
    high_risk_rate = (df_scored["risk_score"] >= 2).mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Transactions", f"{total_tx:,}")
    k2.metric("Unique Users", f"{total_users:,}")
    k3.metric("Overall Return Rate", f"{overall_return_rate:.2%}")
    k4.metric("High Risk Transaction Rate", f"{high_risk_rate:.2%}")

    st.markdown("---")

    # ----------------------------------------------------
    # SIDEBAR FILTERS
    # ----------------------------------------------------
    st.sidebar.header("Filters")

    # Minimum risk_score
    min_score = st.sidebar.slider(
        "Minimum Risk Score",
        min_value=int(df_scored["risk_score"].min()),
        max_value=int(df_scored["risk_score"].max()),
        value=0,
        step=1,
    )

    # Funding speed filter
    funding_opts = sorted(df_scored["funding_speed"].dropna().unique())
    selected_funding = st.sidebar.multiselect(
        "Funding Speed",
        options=funding_opts,
        default=funding_opts,
    )

    # Return code filter
    return_opts = sorted(df_scored["return_code"].dropna().unique())
    return_opts_display = ["(No Return)"] + list(return_opts)

    selected_returns = st.sidebar.multiselect(
        "Return Code",
        options=return_opts_display,
        default=return_opts_display,
    )

    # ----------------------------------------------------
    # APPLY FILTERS
    # ----------------------------------------------------
    df_filtered = df_scored.copy()

    df_filtered = df_filtered[df_filtered["risk_score"] >= min_score]
    df_filtered = df_filtered[df_filtered["funding_speed"].isin(selected_funding)]

    # Handle return code filtering (include NaN as "(No Return)")
    if "(No Return)" in selected_returns:
        # include rows with NaN OR selected codes
        real_codes = [c for c in selected_returns if c != "(No Return)"]
        df_filtered = df_filtered[
            df_filtered["return_code"].isin(real_codes)
            | df_filtered["return_code"].isna()
        ]
    else:
        # Only real return codes selected
        df_filtered = df_filtered[df_filtered["return_code"].isin(selected_returns)]

    st.subheader("Filtered Transaction Summary")
    st.write(
        f"Showing **{len(df_filtered):,}** transactions after applying filters."
    )

    st.markdown("---")

    # ----------------------------------------------------
    # CHARTS
    # ----------------------------------------------------
    c1, c2 = st.columns(2)

    # ---- Risk Score Distribution ----
    with c1:
        st.markdown("#### Risk Score Distribution")

        risk_score_counts = (
            df_filtered["risk_score"]
            .value_counts()
            .sort_index()
            .to_frame(name="count")
        )

        # Name index so Streamlit uses it as x-axis
        risk_score_counts.index.name = "risk_score"

        st.bar_chart(risk_score_counts)

    # ---- Return Code Distribution ----
    with c2:
        st.markdown("#### Return Code Distribution")

        rc_display = df_filtered["return_code"].fillna("(No Return)")

        return_code_counts = (
            rc_display.value_counts()
            .sort_index()
            .to_frame(name="count")
        )
        return_code_counts.index.name = "return_code"

        st.bar_chart(return_code_counts)

    st.markdown("---")

    # ----------------------------------------------------
    # TABLES: HIGH-RISK USERS & DEVICES
    # ----------------------------------------------------
    t1, t2 = st.columns(2)

    # ---- Top Risky Users ----
    with t1:
        st.markdown("#### Top High-Risk Users")

        user_risk = (
            df_filtered.groupby("user_id")["risk_score"]
            .sum()
            .reset_index()
            .sort_values("risk_score", ascending=False)
            .head(10)
        )

        st.dataframe(user_risk, use_container_width=True)

    # ---- Suspicious Devices ----
    with t2:
        st.markdown("#### Devices Shared by Many Users")

        device_stats = (
            df_filtered.groupby("device_id")["user_id"]
            .nunique()
            .reset_index()
            .rename(columns={"user_id": "unique_users"})
            .sort_values("unique_users", ascending=False)
        )

        suspicious_devices = device_stats[device_stats["unique_users"] >= 5]

        st.dataframe(suspicious_devices.head(10), use_container_width=True)

    st.markdown("---")

    # ----------------------------------------------------
    # RAW DATA (OPTIONAL)
    # ----------------------------------------------------
    with st.expander("View sample of filtered transactions"):
        st.dataframe(df_filtered.head(50), use_container_width=True)

    st.caption(
        "Built as a practice project to demonstrate ACH risk analysis, "
        "fraud pattern detection, rule-based scoring, and dashboarding."
    )


# ----------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------
if __name__ == "__main__":
    main()
