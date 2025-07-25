# 💰 Personal Finance Dashboard

An interactive dashboard to track and analyze personal income and expenses using **Python** (Jupyter & Streamlit).  
Built using a synthetic dataset from Kaggle:  
 [Personal Finance Data by ramyapintchy](https://www.kaggle.com/datasets/ramyapintchy/personal-finance-data)

---

## Features

- 📂 Upload your own CSV file with transactions
- 🧾 Preview the first 10 rows of uploaded data
- 📅 Filter by year or view all-time statistics
- 📊 Summary metrics:
  - Total income
  - Total expenses
  - Net balance (income - expenses)
- 📉 Visualizations:
  - Monthly income and expenses (separate and combined)
  - Net monthly balance
  - Expense breakdown by category (bar and pie charts)
  - Year-over-year financial trends
- 📈 Interactive & responsive charts (powered by Plotly)
- 🧠 Automatically detects date formats and groups transactions by month

---

## 🖼️ Sample Visuals

-  **Monthly Trends**
-  **Category Breakdown**
-  **Net Balance Over Time**
---

##  How to Run

### Clone the repository

```bash
git clone https://github.com/bagaruzhan/personal-finance-dashboard.git
```

---
### Install dependencies
```bash
pip install -r requirements.txt
```
---
### Launch the Streamlit app
```bash
streamlit run app.py
```
