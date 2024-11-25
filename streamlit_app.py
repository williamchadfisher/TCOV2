import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def get_fuel_consumption(eco_mode):
    """Get fuel consumption rate based on eco mode."""
    consumption_map = {
        1: 5,   # eco1
        2: 5.5,   # eco2
        3: 6,   # eco3
        4: 6.5,   # eco4
        5: 7,   # eco5
        6: 8,  # eco6
        7: 10,  # eco7
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

]

def calculate_co2_savings(fuel_savings_liters):
    """
    Calculate CO2 savings based on fuel savings.
    1 liter of diesel burned produces approximately 2.68 kg of CO2.
    """
    co2_per_liter = 2.68  # kg of CO2 per liter of diesel
    return fuel_savings_liters * co2_per_liter

def translate_co2_to_trees(co2_kg):
    """
    Translate CO2 savings into the number of trees planted.
    One tree absorbs approximately 21.77 kg of CO2 per year.
    """
    co2_absorbed_per_tree = 21.77  # kg of CO2 per tree per year
    return co2_kg / co2_absorbed_per_tree

def translate_co2_to_plastic_bottles(co2_kg):
    """
    Translate CO2 savings into the number of plastic bottles manufactured.
    Manufacturing one plastic bottle produces approximately 0.082 kg of CO2.
    """
    co2_per_bottle = 0.082  # kg of CO2 per plastic bottle
    return co2_kg / co2_per_bottle

def compare_fuel_and_co2_savings(jcb_fuel_rate, competitor_fuel_rate, daily_hours):
    """
    Compare JCB fuel savings with the competitor and translate the fuel savings into CO2 savings.
    Then translate the CO2 savings into a mixture of comparisons such as trees planted and plastic bottles manufactured.
    """
    # Calculate monthly and annual fuel savings
    monthly_fuel_savings = (competitor_fuel_rate - jcb_fuel_rate) * daily_hours * 30
    annual_fuel_savings = monthly_fuel_savings * 12
    
    # Calculate CO2 savings
    annual_co2_savings = calculate_co2_savings(annual_fuel_savings)
    
    # Translate CO2 savings into trees planted and plastic bottles manufactured
    trees_planted = translate_co2_to_trees(annual_co2_savings)
    plastic_bottles_manufactured = translate_co2_to_plastic_bottles(annual_co2_savings)
    
    return {
        "monthly_fuel_savings": monthly_fuel_savings,
        "annual_fuel_savings": annual_fuel_savings,
        "annual_co2_savings": annual_co2_savings,
        "trees_planted": trees_planted,
        "plastic_bottles_manufactured": plastic_bottles_manufactured
    }

# Example usage
jcb_fuel_rate = 7  # L/hr for JCB in eco mode 7
competitor_fuel_rate = 16  # L/hr for competitor
daily_hours = 8  # hours per day

savings_comparison = compare_fuel_and_co2_savings(jcb_fuel_rate, competitor_fuel_rate, daily_hours)

print(f"Monthly Fuel Savings: {savings_comparison['monthly_fuel_savings']} liters")
print(f"Annual Fuel Savings: {savings_comparison['annual_fuel_savings']} liters")
print(f"Annual CO2 Savings: {savings_comparison['annual_co2_savings']} kg")
print(f"Equivalent Trees Planted: {savings_comparison['trees_planted']}")
print(f"Equivalent Plastic Bottles Manufactured: {savings_comparison['plastic_bottles_manufactured']}")

