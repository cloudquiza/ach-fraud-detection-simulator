# **ACH Fraud Detection Simulator**

Synthetic ACH transaction data, fraud patterns, rule-based scoring, and an interactive dashboard — built to simulate the workflow of a **Payments Risk Analyst** at a modern fintech or crypto exchange (e.g., Coinbase).

This project demonstrates:

- Understanding of **ACH rails**, returns, and fraud signals.
- Ability to generate and analyze large datasets.
- Development of **explainable risk rules** and scoring logic.
- Building **interactive dashboards** for monitoring high-risk patterns.
- Translating raw analysis into a clear, stakeholder-ready narrative.

---

# **🎯 Project Goals**

This project was built as part of a personal portfolio for roles in **Payments Risk**, **Fraud Operations**, and **Risk Analytics**.

It aims to demonstrate that I can:

- Analyze ACH behavior and return codes
- Detect patterns like instant ACH abuse, first-party fraud, and synthetic identity activity
- Build a rule-based scoring engine
- Evaluate rule performance
- Create visual dashboards that mirror internal tooling
- Communicate findings in a structured, risk-analyst format

---

# **📂 Project Structure**

```text
ach-fraud-detection-simulator/
├─ data/
│  ├─ users.csv                     # Generated synthetic users
│  ├─ ach_transactions.csv          # Raw ACH transactions (generated)
│  ├─ ach_transactions_scored.csv   # Scored transactions (generated)
│  └─ alerts.csv                    # Rule hits (generated)
│
├─ src/
│  ├─ generate_synthetic_data.py    # Creates users + transactions
│  ├─ risk_rules.py                 # Fraud rule engine + scoring
│  └─ run_scoring.py                # Runs scoring + writes outputs
│
├─ dashboard/
│  └─ streamlit_app.py              # Interactive ACH fraud dashboard
│
├─ notebooks/
│  └─ ach_fraud_analysis.ipynb      # EDA, charts, precision/recall
│
└─ docs/
   ├─ ACH_Fraud_Report.md           # Written analysis + recommendations
   └─ Case_Studies/
        └─ ...                      # Optional case write-ups
```

---

# **⚙️ SETUP INSTRUCTIONS (START HERE)**

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

# **🏗️ STEP 1 — Generate Synthetic ACH Data**

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

# **🧠 STEP 2 — Apply Risk Rules & Score Transactions**

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

# **📊 STEP 3 — Launch the Interactive Dashboard**

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

# **📓 STEP 4 — Explore Data in the Notebook**

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

# **📝 STEP 5 — Read the Fraud Report**

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

Perfect for linking on your portfolio or discussing during interviews.

---

# **🧪 STEP 6 — Optional Case Studies**

Inside:

`docs/Case_Studies/`

Examples you can add:

- `case_001_instant_ach_abuse.md`
- `case_002_first_party_fraud.md`
- `case_003_synthetic_identity.md`

These show your ability to write **investigation-style narratives**, which Coinbase and other risk teams value a _lot_.

---

# **🌐 Deployment (Optional)**

You can deploy the dashboard publicly on:

- **Streamlit Community Cloud** (free)
- **Hugging Face Spaces**
- **Render**

This allows you to link the dashboard from your portfolio website:

> **Live Demo →** [https://your-dashboard.streamlit.app](https://your-dashboard.streamlit.app)

---

# **🔍 Why This Project Is Relevant for Coinbase or Fintech Risk Roles**

Modern fraud/risk teams look for analysts who can:

- Think in **payment rails**, especially ACH
- Understand return codes and dispute patterns
- Recognize **synthetic identity signals**
- Build and evaluate **risk rules**
- Communicate findings clearly
- Use data tools (SQL/Python/Looker-style dashboards)
- Work with ambiguity
- Measure performance of controls

This project demonstrates exactly that.

It shows:

- Data analysis
- Fraud intuition
- Rule design
- KPI tracking
- Dashboarding
- Documentation and storytelling

All key skills for teams like:

- Payments Risk
- Fraud Operations
- Financial Crimes
- Trust & Safety
- Risk Analytics

---

# **🚀 Future Enhancements**

Planned additions:

- Add ACH return time modeling
- Add anomaly detection models
- Add user-level risk scores
- Add cohort analysis (new users vs existing)
- Expand dashboard with time-series charts
- Add synthetic KYC signals (address similarity, email patterns)

---

# **📫 Contact**

If you'd like to know more about this project or my work in Payments Risk / Fraud, feel free to reach out.

---
