# **ACH Fraud Detection Simulator**

Synthetic ACH transaction data, fraud patterns, rule-based scoring, and an interactive dashboard — built to simulate the workflow of a **Payments Risk Analyst** at a modern fintech.

This project demonstrates:

- Understanding of **ACH rails**, returns, and fraud signals.
- Ability to generate and analyze large datasets.
- Development of **explainable risk rules** and scoring logic.
- Building **interactive dashboards** for monitoring high-risk patterns.
- Translating raw analysis into a clear, stakeholder-ready narrative.

---

# **Project Goals**

This project was built as part of a personal portfolio for roles in **Payments Risk**, **Fraud Operations**, and **Risk Analytics**.

It aims to demonstrate that I can:

- Analyze ACH behavior and return codes
- Detect patterns like instant ACH abuse, first-party fraud, and synthetic identity activity
- Build a rule-based scoring engine
- Evaluate rule performance
- Create visual dashboards that mirror internal tooling
- Communicate findings in a structured, risk-analyst format

---

# **SETUP INSTRUCTIONS (START HERE)**

### **1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/ach-fraud-detection-simulator.git
cd ach-fraud-detection-simulator
```

---

### **2. Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows
```

---

### **3. Install required packages**

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pandas numpy jupyter streamlit
```

---

# **STEP 1 — Generate Synthetic ACH Data**

This script creates:

- 500 synthetic users
- 5,000 ACH transactions
- Built-in fraud patterns:

  - Instant ACH abuse
  - First-party fraud
  - Synthetic identity behavior

Run:

```bash
python src/generate_synthetic_data.py
```

Output files created:

- `data/users.csv`
- `data/ach_transactions.csv`

---

# **STEP 2 — Apply Risk Rules & Score Transactions**

This script:

- Loads ACH data
- Applies risk rules
- Assigns a `risk_score`
- Outputs:

  - `data/ach_transactions_scored.csv`
  - `data/alerts.csv`

Run:

```bash
python src/run_scoring.py
```

### **Current Rules Implemented**

1. **High Instant ACH for New Users**

   - Instant funding
   - Account age < 30 days
   - Amount > $500

2. **Rapid High-Risk Returns**

   - Return within 5 days
   - Return codes: R01, R10, R29

3. **Device Shared by Many Users**

   - Device used by ≥5 distinct users

---

# **STEP 3 — Launch the Interactive Dashboard**

Run:

```bash
streamlit run dashboard/streamlit_app.py
```

This opens a dashboard with:

### **KPIs**

- Total transactions
- Unique users
- Return rate
- High-risk transaction rate

### **Filters**

- Minimum risk score
- Funding speed (instant/standard)
- Return codes (including “No Return”)

### **Visualizations**

- Risk score distribution
- Return code distribution
- Top high-risk users
- Devices shared by many accounts

This dashboard simulates what an internal risk analytics tool might look like.

---

# **STEP 4 — Explore Data in the Notebook**

Open:

```bash
jupyter notebook notebooks/ach_fraud_analysis.ipynb
```

Includes:

- Return rate analysis
- Trend charts
- Risk score distribution
- Precision/recall vs synthetic ground truth
- Commentary explaining the results

---

# **STEP 5 — Read the Fraud Report**

Located at:

```
docs/ACH_Fraud_Report.md
```

This report is written in the style of a **risk analyst evaluating ACH fraud exposure**.

Sections include:

- Objective
- Dataset summary
- Injected fraud patterns
- Detection results
- Rule performance
- Recommendations
- Next steps

---
