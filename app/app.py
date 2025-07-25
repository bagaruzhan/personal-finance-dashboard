import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title='Personal Finance Dashboard', layout='wide')

# Load function
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period("M").astype(str)
    return df

# Sidebar
with st.sidebar:
    st.header("Upload and Filter")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        df = load_data(uploaded_file)
        years = ['All'] + sorted(df['Year'].unique(), reverse=True)
        selected_year = st.selectbox('Select year:', years)

        if selected_year == 'All':
            df_filtered = df.copy()
        else:
            df_filtered = df[df['Year'] == selected_year]
    else:
        df_filtered = pd.DataFrame()

# Main section
st.title("Personal Finance Dashboard")

if uploaded_file is None:
    st.info("Upload a CSV file to begin.")
else:
    st.subheader("First 10 Rows of Uploaded Data")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader(f"Summary for {selected_year if selected_year != 'All' else 'All Time'}")
    income_total = df_filtered[df_filtered["Type"] == "Income"]["Amount"].sum()
    expense_total = df_filtered[df_filtered["Type"] == "Expense"]["Amount"].sum()
    net_total = income_total - expense_total

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${income_total:,.2f}")
    col2.metric("Total Expenses", f"${expense_total:,.2f}")
    col3.metric("Net Balance", f"${net_total:,.2f}", delta=f"{net_total:,.2f}")

    monthly = df_filtered.groupby(['Month', 'Type'])['Amount'].sum().unstack().fillna(0).reset_index()

    st.subheader("Monthly Income and Expenses (Separate)")
    col_inc, col_exp = st.columns(2)
    with col_inc:
        fig_income = px.bar(monthly, x='Month', y='Income', title='Monthly Income',
                            labels={'Income': 'Amount'}, height=400)
        st.plotly_chart(fig_income, use_container_width=True)

    with col_exp:
        fig_expense = px.bar(monthly, x='Month', y='Expense', title='Monthly Expenses',
                             labels={'Expense': 'Amount'}, height=400)
        st.plotly_chart(fig_expense, use_container_width=True)

    st.subheader("Monthly Income vs Expenses (Combined)")
    fig_combined = px.bar(monthly, x='Month', y=['Income', 'Expense'],
                          barmode='group', title='Income vs Expenses',
                          labels={'value': 'Amount', 'Month': 'Month'}, height=450)
    st.plotly_chart(fig_combined, use_container_width=True)

    st.subheader("Net Balance Over Time")
    monthly['Net'] = monthly['Income'] - monthly['Expense']
    fig_net = px.line(monthly, x='Month', y='Net', markers=True,
                      title="Monthly Net Balance", labels={'Net': 'Net Amount'}, height=450)
    st.plotly_chart(fig_net, use_container_width=True)

    st.subheader(f'Expenses by Category - {selected_year if selected_year != "All" else "All Time"}')
    expense_df = df_filtered[df_filtered['Type'] == 'Expense'].groupby('Category')['Amount'].sum().reset_index()

    col_bar, col_pie = st.columns(2)
    with col_bar:
        fig_cat_bar = px.bar(expense_df.sort_values('Amount'), x='Amount', y='Category',
                             orientation='h', title='Expenses by Category',
                             labels={'Amount': 'Amount'}, height=500)
        st.plotly_chart(fig_cat_bar, use_container_width=True)

    with col_pie:
        fig_cat_pie = px.pie(expense_df, names='Category', values='Amount',
                             title='Category Share of Expenses', height=500)
        st.plotly_chart(fig_cat_pie, use_container_width=True)

    if selected_year == 'All':
        st.subheader("Yearly Trends")
        yearly = df.groupby(['Year', 'Type'])['Amount'].sum().unstack().fillna(0).reset_index()
        yearly['Net'] = yearly['Income'] - yearly['Expense']

        col_y1, col_y2 = st.columns(2)
        with col_y1:
            fig_year = px.bar(yearly, x='Year', y=['Income', 'Expense', 'Net'],
                              title='Yearly Income, Expenses, Net',
                              labels={'value': 'Amount'}, barmode='group', height=450)
            st.plotly_chart(fig_year, use_container_width=True)

        with col_y2:
            year_cat = df[df['Type'] == 'Expense'].groupby(['Year', 'Category'])['Amount'].sum().reset_index()
            fig_ycat = px.bar(year_cat, x='Year', y='Amount', color='Category',
                              title='Yearly Expenses by Category', height=450)
            fig_ycat.update_layout(barmode='stack')
            st.plotly_chart(fig_ycat, use_container_width=True)

