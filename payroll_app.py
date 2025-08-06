import streamlit as st
import pandas as pd
import os

EMPLOYEE_FILE = 'employees.csv'
PAYROLL_FILE = 'payroll.csv'

# --- Initialize files if not exist ---
def init_files():
    if not os.path.exists(EMPLOYEE_FILE):
        pd.DataFrame(columns=['ID', 'Name', 'Department', 'Position', 'Email']).to_csv(EMPLOYEE_FILE, index=False)
    if not os.path.exists(PAYROLL_FILE):
        pd.DataFrame(columns=['ID', 'Month', 'Basic', 'Allowance', 'Overtime Hours', 'Overtime Rate', 'Deductions', 'Net Salary']).to_csv(PAYROLL_FILE, index=False)

init_files()

# --- Load data ---
employees_df = pd.read_csv(EMPLOYEE_FILE)
payroll_df = pd.read_csv(PAYROLL_FILE)

# --- App layout ---
st.title("💼 Payroll Management Web App")

menu = st.sidebar.selectbox("Menu", ["Add Employee", "View Employees", "Add Payroll", "View Payroll"])

# --- Add employee ---
if menu == "Add Employee":
    st.header("➕ Add New Employee")
    with st.form("employee_form"):
        emp_id = st.text_input("Employee ID")
        name = st.text_input("Full Name")
        dept = st.text_input("Department")
        position = st.text_input("Position")
        email = st.text_input("Email")

        submitted = st.form_submit_button("Add Employee")
        if submitted:
            if emp_id in employees_df['ID'].values:
                st.warning("Employee ID already exists.")
            else:
                new_emp = pd.DataFrame([[emp_id, name, dept, position, email]], columns=employees_df.columns)
                employees_df = pd.concat([employees_df, new_emp], ignore_index=True)
                employees_df.to_csv(EMPLOYEE_FILE, index=False)
                st.success("Employee added successfully!")

# --- View employees ---
elif menu == "View Employees":
    st.header("📋 Employee List")
    st.dataframe(employees_df)

# --- Add payroll ---
elif menu == "Add Payroll":
    st.header("🧮 Add Payroll Information")
    if employees_df.empty:
        st.warning("No employees found. Please add employees first.")
    else:
        selected_id = st.selectbox("Select Employee ID", employees_df['ID'].unique())
        month = st.text_input("Month (e.g. August 2025)")
        basic = st.number_input("Basic Salary", min_value=0.0)
        allowance = st.number_input("Allowances", min_value=0.0)
        overtime_hours = st.number_input("Overtime Hours", min_value=0.0)
        overtime_rate = st.number_input("Overtime Rate (per hour)", min_value=0.0)
        deductions = st.number_input("Deductions", min_value=0.0)

        if st.button("Calculate & Save"):
            overtime_pay = overtime_hours * overtime_rate
            net_salary = basic + allowance + overtime_pay - deductions

            new_payroll = pd.DataFrame([[
                selected_id, month, basic, allowance, overtime_hours, overtime_rate, deductions, net_salary
            ]], columns=payroll_df.columns)

            payroll_df = pd.concat([payroll_df, new_payroll], ignore_index=True)
            payroll_df.to_csv(PAYROLL_FILE, index=False)
            st.success(f"Payroll saved. Net Salary: ${net_salary:.2f}")

# --- View payroll ---
elif menu == "View Payroll":
    st.header("📊 Payroll Records")
    st.dataframe(payroll_df)

