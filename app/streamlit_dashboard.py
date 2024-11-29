import streamlit as st
import pandas as pd
import plotly.express as px
from elasticsearch import Elasticsearch

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from dotenv import load_dotenv
import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Elasticsearch setup
es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "mynameisvatsal"), verify_certs=False)

# Load environment variables
load_dotenv()

# Elasticsearch setup
es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "mynameisvatsal"), verify_certs=False)

# Streamlit Layout
st.set_page_config(page_title="Financial Tracker Dashboard", layout="wide")
st.title("Financial Tracker Dashboard")

# Buttons to Add Balance and Expense
st.sidebar.header("Actions")

# Add Balance Popup
if st.sidebar.button("Add Balance"):
    st.session_state.show_form = True

if 'show_form' in st.session_state and st.session_state.show_form:
    with st.form(key="add_balance_form"):
        st.subheader("Add Balance")
        bank_name = st.text_input("Bank Name", help="Enter the name of your bank.")
        account_no = st.text_input("Account Number", help="Enter your account number.")
        balance = st.number_input("Balance", min_value=0.0, step=1.0, help="Enter your current account balance.")
        
        # Submit button inside the form
        submitted = st.form_submit_button("Submit")
        
        # Debug statement to check if the form is being displayed
        st.write("Form is displayed")
        
        # Debug statement to check the value of submitted
        st.write(f"Submitted value: {submitted}")
        
        # This block runs when the form is submitted
        if submitted:
            # Debug statement to check if the form is submitted
            st.write("Form submitted!")
            st.write(f"Bank Name: {bank_name}, Account Number: {account_no}, Balance: {balance}")
            try:
                # API endpoint for adding balance
                api_url = "http://127.0.0.1:5000/net_worth/add_balance"

                # Payload to send to the API
                document = {
                    "bank_name": bank_name,
                    "account_no": account_no,
                    "balance": balance
                }

                st.info(f"Calling API with: {document}")  # Log the request data
                response = requests.post(api_url, json=document)
                
                if response.status_code == 201:
                    st.success("Balance added successfully!")
                else:
                    st.error(f"Failed to add balance. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            # Reset the form state
            st.session_state.show_form = False

# Add Expense Popup
# Add Expense Popup
if st.sidebar.button("Add Expense"):
    st.session_state.show_expense_form = True

# Display the form if `show_expense_form` is True
if 'show_expense_form' in st.session_state and st.session_state.show_expense_form:
    with st.form(key="add_expense_form"):
        st.subheader("Add Expense")
        amount = st.number_input("Amount", min_value=0.0, step=1.0, help="Enter the expense amount.")
        category = st.text_input("Category", help="Enter the category for this expense.")
        
        # Submit button inside the form
        submitted = st.form_submit_button("Submit")
        
        # Debug statement to check the value of submitted
        st.write(f"Submitted value: {submitted}")
        
        if submitted:
            # Debug statement to confirm the form submission
            st.write("Form submitted!")
            st.write(f"Amount: {amount}, Category: {category}")
            try:
                # API endpoint for adding expense
                api_url = "http://127.0.0.1:5000/income_expenses/expense"

                # Payload to send to the API
                document = {
                    "type": "expense",
                    "amount": amount,
                    "category": category,
                    "date": pd.Timestamp.now().isoformat()
                }

                st.info(f"Calling API with: {document}")  # Log the request data
                response = requests.post(api_url, json=document)
                
                if response.status_code == 201:
                    st.success("Expense added successfully!")
                else:
                    st.error(f"Failed to add expense. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            # Reset the form state to hide the form after submission
            st.session_state.show_expense_form = False




# Add Income Popup
if st.sidebar.button("Add Income"):
    st.session_state.show_income_form = True

# Display the form if `show_income_form` is True
if 'show_income_form' in st.session_state and st.session_state.show_income_form:
    with st.form(key="add_income_form"):
        st.subheader("Add Income")
        amount = st.number_input("Amount", min_value=0.0, step=1.0, help="Enter the income amount.")
        category = st.text_input("Category", help="Enter the category for this income.")
        
        # Submit button inside the form
        submitted = st.form_submit_button("Submit")
        
        # Debug statement to check the value of submitted
        st.write(f"Submitted value: {submitted}")
        
        if submitted:
            # Debug statement to confirm the form submission
            st.write("Form submitted!")
            st.write(f"Amount: {amount}, Category: {category}")
            try:
                # API endpoint for adding income
                api_url = "http://127.0.0.1:5000/income_expenses/income"

                # Payload to send to the API
                document = {
                    "type": "income",
                    "amount": amount,
                    "category": category,
                    "date": pd.Timestamp.now().isoformat()
                }

                st.info(f"Calling API with: {document}")  # Log the request data
                response = requests.post(api_url, json=document)
                
                if response.status_code == 201:
                    st.success("Income added successfully!")
                else:
                    st.error(f"Failed to add income. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            # Reset the form state to hide the form after submission
            st.session_state.show_income_form = False






# Section 1: Net Worth Overview
st.header("Net Worth Overview")

# Fetch balance and expenses data from Elasticsearch
def get_networth_data():
    try:
        # Fetch total balance
        balance_response = es.get(index="bank_accounts", id="total_balance")
        total_balance = balance_response["_source"]["balance"]

        # Fetch total expenses
        expenses_response = es.search(index="income_expenses", body={
            "query": {"match": {"type": "expense"}},
            "aggs": {"total_expenses": {"sum": {"field": "amount"}}},
            "size": 0
        })
        total_expenses = expenses_response["aggregations"]["total_expenses"]["value"]

        # Calculate net worth
        net_worth = total_balance - total_expenses
        return total_balance, total_expenses, net_worth

    except Exception as e:
        st.error(f"Error fetching net worth data: {e}")
        return 0, 0, 0

total_balance, total_expenses, net_worth = get_networth_data()

# Display Net Worth Overview
st.metric("Total Balance", f"${total_balance:,.2f}")
st.metric("Total Expenses", f"${total_expenses:,.2f}")
st.metric("Net Worth", f"${net_worth:,.2f}")

# Pie chart for Net Worth
pie_data = pd.DataFrame({
    "Category": ["Balance", "Expenses"],
    "Amount": [total_balance, total_expenses]
})
fig = px.pie(pie_data, names="Category", values="Amount", title="Net Worth Distribution")
st.plotly_chart(fig)

# Section 2: Income vs. Expenses
st.header("Income vs. Expenses")

def get_income_expenses_data():
    try:
        response = es.search(index="income_expenses", body={
            "aggs": {
                "monthly_income": {
                    "filter": {"term": {"type": "income"}},
                    "aggs": {"total_income": {"sum": {"field": "amount"}}}
                },
                "monthly_expenses": {
                    "filter": {"term": {"type": "expense"}},
                    "aggs": {"total_expenses": {"sum": {"field": "amount"}}}
                }
            },
            "size": 0
        })

        monthly_income = response["aggregations"]["monthly_income"]["total_income"]["value"]
        monthly_expenses = response["aggregations"]["monthly_expenses"]["total_expenses"]["value"]
        return monthly_income, monthly_expenses

    except Exception as e:
        st.error(f"Error fetching income vs. expenses data: {e}")
        return 0, 0

monthly_income, monthly_expenses = get_income_expenses_data()

# Bar Chart for Income vs. Expenses
income_expenses_data = pd.DataFrame({
    "Category": ["Income", "Expenses"],
    "Amount": [monthly_income, monthly_expenses]
})
fig = px.bar(income_expenses_data, x="Category", y="Amount", title="Monthly Income vs. Expenses", text="Amount")
st.plotly_chart(fig)



st.header("Show All Transactions")

# Session state to manage table visibility and button state
if "show_table" not in st.session_state:
    st.session_state["show_table"] = False
if "dataframe" not in st.session_state:
    st.session_state["dataframe"] = pd.DataFrame()

# Function to fetch all balances from the API
def fetch_all_balances():
    try:
        # Call the API
        api_url = "http://127.0.0.1:5000/net_worth/get_all_balances"
        response = requests.get(api_url)

        if response.status_code == 200:
            # Parse the API response
            data = response.json().get("records", [])

            # Return data as a DataFrame
            if data:
                return pd.DataFrame(data)
            else:
                st.info("No records found.")
                return pd.DataFrame()  # Return empty DataFrame if no data
        else:
            st.error(f"API Call Failed: {response.status_code} - {response.text}")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Error fetching balances: {e}")
        return pd.DataFrame()

# Fetch All Balances Button
if st.button("Fetch All Balances"):
    df = fetch_all_balances()
    if not df.empty:
        st.session_state["dataframe"] = df
        st.session_state["show_table"] = True
    else:
        st.session_state["show_table"] = False

# Conditional Clear Table Button
if st.session_state["show_table"]:
    if st.button("Clear Table"):
        st.session_state["dataframe"] = pd.DataFrame()
        st.session_state["show_table"] = False

# Display the table if data is available
if st.session_state["show_table"] and not st.session_state["dataframe"].empty:
    
    
    


    st.write("### Transaction List: ")
    st.dataframe(st.session_state["dataframe"])
    
    


# Section: Income by Category
st.header("Income by Category")

def fetch_income_by_category():
    try:
        # Elasticsearch query to aggregate income by category
        response = es.search(index="income_expenses", body={
            "query": {
                "term": {"type": "income"}
            },
            "aggs": {
                "income_by_category": {
                    "terms": {"field": "category.keyword", "size": 10},  # Aggregate by category
                    "aggs": {
                        "total_income": {"sum": {"field": "amount"}}
                    }
                }
            },
            "size": 0  # No need to return individual documents
        })

        # Extract the aggregation results
        buckets = response["aggregations"]["income_by_category"]["buckets"]
        categories = [bucket["key"] for bucket in buckets]
        incomes = [bucket["total_income"]["value"] for bucket in buckets]

        # Return as a DataFrame
        return pd.DataFrame({"Category": categories, "Total Income": incomes})

    except Exception as e:
        st.error(f"Error fetching income data by category: {e}")
        return pd.DataFrame()

# Fetch the data
income_df = fetch_income_by_category()

# Display the bar chart if data is available
if not income_df.empty:
    st.write("### Total Income by Category")
    fig = px.bar(income_df, x="Category", y="Total Income", title="Income by Category", text="Total Income")
    st.plotly_chart(fig)
else:
    st.info("No income data available to display.")
    
    


