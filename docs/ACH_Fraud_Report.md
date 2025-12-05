# ACH Fraud Analysis Report

## 1. Objective

Simulate ACH transaction activity and identify fraud patterns such as instant ACH abuse, first party fraud, and synthetic identity behavior. Use rule based detection to assign a risk score to each transaction and evaluate how well the rules capture the synthetic patterns.

## 2. Dataset and Methodology

- 500 synthetic users
- 5,000 synthetic ACH transactions
- Key fields:
  - amount_usd
  - funding_speed
  - account_age_days
  - return_code
  - device_id
  - is_fraud_pattern

Method:

- Generate synthetic data with known fraud patterns.
- Apply rule based logic to flag risky behavior.
- Aggregate rule hits into a risk_score per transaction.
- Compare risk_score to the ground truth label is_fraud_pattern.

## 3. Key Findings

- Overall ACH return rate: _[fill in from notebook]_.
- High risk return codes (R01, R10, R29) occur more frequently in instant ACH than in standard ACH.
- New users funded via instant ACH tend to show a higher concentration of high risk returns.
- A small number of devices are used by many distinct users, which may indicate synthetic identity or account farming.

## 4. Rules Implemented

1. **High instant ACH for new users**  
   Flags transactions where funding_speed is instant, account_age_days is less than 30, and amount_usd is above 500.

2. **Rapid high risk returns**  
   Flags transactions with R01, R10, or R29 return codes where the return occurs within 5 days.

3. **Device shared by many users**  
   Flags transactions from devices associated with at least 5 distinct user_ids.

## 5. Detection Performance

For transactions with risk_score >= 2:

- Precision: _[fill in from notebook]_.
- Recall: _[fill in from notebook]_.

**Strengths**

- Rules effectively surface synthetic patterns such as instant ACH abuse.
- Simple rules provide clear operational explanations for alerts.

**Gaps**

- Some fraud patterns may not trigger rules when signals are weak.
- Rules can generate false positives on legitimate but unusual behavior.

## 6. Recommendations

- Introduce stricter limits on instant ACH for very new accounts.
- Add device and IP based monitoring to identify clusters of related accounts.
- Consider combining rule based logic with machine learning models to improve coverage and reduce false positives.

## 7. Next Steps

- Add more signals such as bank account tenure, chargeback history, and IP reputation.
- Expand the synthetic dataset to include more nuanced fraud behaviors.
- Integrate this analysis into a simple monitoring or alerting pipeline.
