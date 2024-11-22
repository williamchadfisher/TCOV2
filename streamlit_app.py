import streamlit as st
import plotly.graph_objects as go

# Function to calculate monthly cost
def calculate_monthly_cost(price, interest_rate, loan_length, downpayment, daily_hours):
    loan_amount = price - (price * downpayment / 100)
    monthly_interest_rate = interest_rate / 12 / 100
    monthly_payment = loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -loan_length)
    
    # Calculate principal and interest payments
    principal_payment = loan_amount / loan_length
    interest_payment = monthly_payment - principal_payment
    
    operator_salary = 500
    machine_insurance = 100
    
    # Calculate fuel cost
    fuel_cost_per_hour = 14 * 1  # 14 litres per hour at 1 dollar per litre
    monthly_fuel_cost = daily_hours * fuel_cost_per_hour * 30  # Assuming 30 days in a month
    
    # Calculate warranty and service package cost (valid for 3 years)
    warranty_service_package_total = 9485
    warranty_service_package_monthly = warranty_service_package_total / (3 * 12)
    
    total_monthly_cost = monthly_payment + operator_salary + machine_insurance + monthly_fuel_cost + warranty_service_package_monthly
    return total_monthly_cost, monthly_payment, principal_payment, interest_payment, operator_salary, machine_insurance, monthly_fuel_cost, warranty_service_package_monthly

# Streamlit app
st.title("JCB Excavator Monthly Cost Calculator")

# Input fields
price = st.number_input("Total Cash Price of Machine (USD)", min_value=0.0, value=80000.0, step=1000.0, format="%0.0f")
interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=5.0, step=0.5)
loan_length = st.slider("Loan Length (months)", min_value=36, max_value=60, value=48, step=3)
downpayment = st.slider("Downpayment (%)", min_value=10, max_value=50, value=20, step=1)
daily_hours = st.number_input("Daily Operating Hours", min_value=0.0, value=8.0, step=0.5)

# Calculate costs
total_monthly_cost, monthly_payment, principal_payment, interest_payment, operator_salary, machine_insurance, monthly_fuel_cost, warranty_service_package_monthly = calculate_monthly_cost(price, interest_rate, loan_length, downpayment, daily_hours)

# Display results
st.write(f"Total Monthly Cost: ${total_monthly_cost:,.0f}")
st.write(f"Monthly Principal Payment: ${principal_payment:,.0f}")
st.write(f"Monthly Interest Payment: ${interest_payment:,.0f}")
st.write(f"Operator Salary: ${operator_salary:,.0f}")
st.write(f"Machine Insurance: ${machine_insurance:,.0f}")
st.write(f"Monthly Fuel Cost: ${monthly_fuel_cost:,.0f}")
st.write(f"Warranty and Service Package: ${warranty_service_package_monthly:,.0f}")

# Sankey diagram
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",  # Use snap arrangement to avoid twisted nodes
    node=dict(
        pad=15,
        thickness=30,
        line=dict(color="black", width=0.5),
        label=[
            "Total Monthly Cost", 
            f"Principal Payment (USD {principal_payment:,.0f})", 
            f"Interest Payment (USD {interest_payment:,.0f})", 
            f"Operator Salary (USD {operator_salary:,.0f})", 
            f"Machine Insurance (USD {machine_insurance:,.0f})", 
            f"Fuel Cost (USD {monthly_fuel_cost:,.0f})", 
            f"Warranty and Service Package (USD {warranty_service_package_monthly:,.0f})"
        ],
        color=["blue", "green", "red", "purple", "orange", "brown", "pink"]
    ),
    link=dict(
        source=[0, 0, 0, 0, 0, 0],
        target=[1, 2, 3, 4, 5, 6],
        value=[principal_payment, interest_payment, operator_salary, machine_insurance, monthly_fuel_cost, warranty_service_package_monthly]
    )
)])

fig.update_layout(
    title_text="Monthly Outgoings Sankey Diagram",
    width=800,
    height=600,
    font=dict(size=12)
)

st.plotly_chart(fig)