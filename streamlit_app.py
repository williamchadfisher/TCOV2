import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def get_fuel_consumption(eco_mode):
    """Get fuel consumption rate based on eco mode."""
    consumption_map = {
        1: 5,   # eco1
        2: 6,   # eco2
        3: 7,   # eco3
        4: 8,   # eco4
        5: 9,   # eco5
        6: 10,  # eco6
        7: 11,  # eco7
        8: 12   # eco8
    }
    return consumption_map.get(eco_mode, 5)  # Default to eco1 if invalid mode

def validate_inputs(price, interest_rate, loan_length, downpayment, daily_hours):
    """Validate all inputs and return a list of error messages."""
    errors = []
    
    # Price validation
    if price <= 0:
        errors.append("Machine price must be greater than 0")
        
    # Interest rate validation
    if interest_rate <= 0:
        errors.append("Interest rate must be greater than 0")
    elif interest_rate > 20:
        errors.append("Interest rate seems unusually high. Please verify.")
        
    # Loan length validation
    if loan_length < 12:
        errors.append("Loan length must be at least 12 months")
    elif loan_length > 84:
        errors.append("Loan length cannot exceed 84 months")
        
    # Down payment validation
    if downpayment < 10:
        errors.append("Minimum down payment is 10%")
    elif downpayment > 50:
        errors.append("Maximum down payment is 50%")
        
    # Daily hours validation
    if daily_hours <= 0:
        errors.append("Daily operating hours must be greater than 0")
    elif daily_hours > 24:
        errors.append("Daily operating hours cannot exceed 24")
        
    return errors

def calculate_monthly_cost(price, interest_rate, loan_length, downpayment, daily_hours, fuel_rate):
    """Calculate monthly costs with emphasis on fuel consumption."""
    try:
        # Loan calculations
        loan_amount = price - (price * downpayment / 100)
        monthly_interest_rate = interest_rate / 12 / 100
        monthly_payment = loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -loan_length)
        
        principal_payment = loan_amount / loan_length
        interest_payment = monthly_payment - principal_payment
        
        operator_salary = 500
        machine_insurance = 100
        
        # Fuel cost calculation
        fuel_cost_per_liter = 1  # Assuming $1 per liter, make this configurable if needed
        monthly_fuel_cost = daily_hours * fuel_rate * fuel_cost_per_liter * 30
        
        # Annual fuel cost for comparison
        annual_fuel_cost = monthly_fuel_cost * 12
        
        warranty_service_package_total = 9485
        warranty_service_package_monthly = warranty_service_package_total / (3 * 12)
        
        total_monthly_cost = (monthly_payment + operator_salary + machine_insurance + 
                            monthly_fuel_cost + warranty_service_package_monthly)
        
        return (total_monthly_cost, monthly_payment, principal_payment, interest_payment,
                operator_salary, machine_insurance, monthly_fuel_cost, 
                warranty_service_package_monthly, annual_fuel_cost)
                
    except Exception as e:
        st.error(f"Calculation error: {str(e)}")
        return None

# Streamlit app
st.set_page_config(page_title="JCB Excavator Cost Calculator", 
                   page_icon=":construction:", 
                   layout="wide")

st.title("JCB 215 NXT Excavator Cost Calculator")
st.markdown("""
    This calculator demonstrates the significant impact of fuel efficiency on total operating costs.
    The JCB 215 NXT's superior fuel efficiency can lead to substantial savings over time.
""")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Machine Details")
    price = st.number_input(
        "Total Cash Price of Machine (USD)", 
        min_value=0.0, 
        value=100000.0, 
        step=1000.0, 
        format="%0.0f",
        help="Enter the full purchase price of the JCB excavator"
    )

    interest_rate = st.number_input(
        "Interest Rate (%)", 
        min_value=0.0, 
        max_value=20.0,
        value=12.0, 
        step=0.5,
        help="Annual interest rate for financing"
    )

    loan_length = st.slider(
        "Loan Length (months)", 
        min_value=12, 
        max_value=84, 
        value=48, 
        step=12,
        help="Duration of the loan in months"
    )

with col2:
    st.subheader("Operating Parameters")
    downpayment = st.slider(
        "Downpayment (%)", 
        min_value=10, 
        max_value=50, 
        value=20, 
        step=5,
        help="Percentage of total price paid upfront"
    )

    daily_hours = st.number_input(
        "Daily Operating Hours", 
        min_value=0.1, 
        max_value=24.0, 
        value=8.0, 
        step=0.5,
        help="Average number of hours the excavator is used per day"
    )

    # Add JCB eco mode selector
    st.subheader("JCB Fuel Consumption")
    eco_mode = st.slider(
        "Working Mode", 
        min_value=1, 
        max_value=8, 
        value=7, 
        step=1,
        help="Select eco mode (1-8) to determine fuel consumption"
    )
    
    jcb_fuel_rate = get_fuel_consumption(eco_mode)
    st.write(f"Current Fuel Consumption (eco{eco_mode}): {jcb_fuel_rate} L/hr")

    # Add competitor fuel consumption
    st.subheader("Competitor Fuel Consumption")
    competitor_fuel_rate = st.number_input(
        "Competitor Fuel Consumption (L/hr)", 
        min_value=10.0,
        max_value=30.0,
        value=16.0,
        step=0.5,
        help="Average fuel consumption of competitor machines"
    )

# Validate inputs
errors = validate_inputs(price, interest_rate, loan_length, downpayment, daily_hours)

if errors:
    for error in errors:
        st.error(error)
else:
    # Calculate costs for both JCB and competitor
    jcb_result = calculate_monthly_cost(price, interest_rate, loan_length, downpayment, daily_hours, fuel_rate=jcb_fuel_rate)
    competitor_result = calculate_monthly_cost(price, interest_rate, loan_length, downpayment, daily_hours, fuel_rate=competitor_fuel_rate)
    
    if jcb_result and competitor_result:
        st.header("Cost Analysis")
        
        # Unpack results
        (jcb_total, jcb_monthly, jcb_principal, jcb_interest,
         jcb_operator, jcb_insurance, jcb_fuel, jcb_warranty, jcb_annual_fuel) = jcb_result
        
        (comp_total, comp_monthly, comp_principal, comp_interest,
         comp_operator, comp_insurance, comp_fuel, comp_warranty, comp_annual_fuel) = competitor_result

        # Calculate fuel savings
        monthly_fuel_savings = comp_fuel - jcb_fuel
        annual_fuel_savings = monthly_fuel_savings * 12
        
        # Display savings prominently
        savings_col1, savings_col2 = st.columns(2)
        with savings_col1:
            st.metric("Monthly Fuel Savings with JCB 215 NXT", 
                     f"${monthly_fuel_savings:,.2f}")
        with savings_col2:
            st.metric("Annual Fuel Savings with JCB 215 NXT", 
                     f"${annual_fuel_savings:,.2f}")

        # Create comparison table
        comparison_data = {
            'Cost Component': ['Total Monthly Cost', 'Monthly Fuel Cost', 'Annual Fuel Cost'],
            'JCB 215 NXT': [jcb_total, jcb_fuel, jcb_annual_fuel],
            'Competitor': [comp_total, comp_fuel, comp_annual_fuel],
            'Savings': [comp_total - jcb_total, monthly_fuel_savings, annual_fuel_savings]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        df_comparison = df_comparison.style.format({
            'JCB 215 NXT': '${:,.2f}',
            'Competitor': '${:,.2f}',
            'Savings': '${:,.2f}'
        })
        
        st.subheader("Cost Comparison")
        st.dataframe(df_comparison)

        # Detailed breakdown in expandable section
        with st.expander("See detailed cost breakdown"):
            st.write(f"Monthly Principal Payment: ${jcb_principal:,.2f}")
            st.write(f"Monthly Interest Payment: ${jcb_interest:,.2f}")
            st.write(f"Operator Salary: ${jcb_operator:,.2f}")
            st.write(f"Machine Insurance: ${jcb_insurance:,.2f}")
            st.write(f"Warranty and Service Package: ${jcb_warranty:,.2f}")

        # Create comparative Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            arrangement="snap",
            node=dict(
                pad=15,
                thickness=30,
                line=dict(color="black", width=0.5),
                label=[
                    "Total Monthly Cost", 
                    f"Principal (${jcb_principal:,.0f})", 
                    f"Interest (${jcb_interest:,.0f})", 
                    f"Operator (${jcb_operator:,.0f})", 
                    f"Insurance (${jcb_insurance:,.0f})", 
                    f"Fuel (${jcb_fuel:,.0f})", 
                    f"Warranty (${jcb_warranty:,.0f})"
                ],
                color=["blue", "green", "red", "purple", "orange", "brown", "pink"]
            ),
            link=dict(
                source=[0, 0, 0, 0, 0, 0],
                target=[1, 2, 3, 4, 5, 6],
                value=[jcb_principal, jcb_interest, jcb_operator, 
                      jcb_insurance, jcb_fuel, jcb_warranty]
            )
        )])

        fig.update_layout(
            title_text="JCB 215 NXT Monthly Cost Breakdown",
            width=800,
            height=600,
            font=dict(size=12)
        )

        st.plotly_chart(fig)

        # Add ROI calculation
        years_to_roi = price / annual_fuel_savings
        st.subheader("Return on Investment Analysis")
        st.write(f"Based on fuel savings alone, the JCB 215 NXT will pay for itself in {years_to_roi:.1f} years compared to competitor machines.")