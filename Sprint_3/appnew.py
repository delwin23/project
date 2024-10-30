import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

# Load the RandomForest model
with open('rf_new_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

# Title and description
st.title("Employee Attrition Prediction")
st.write("""
This app predicts whether an employee will leave the company based on certain factors.
""")

# Collect user input
st.header("Enter the employee details:")

monthly_income = st.number_input("Monthly Income", min_value=0)
overtime = st.selectbox("OverTime", ['No', 'Yes'])
age = st.number_input("Age", min_value=18, max_value=100)
total_working_years = st.number_input("Total Working Years", min_value=0)
years_at_company = st.number_input("Years at Company", min_value=0)
stock_option_level = st.selectbox("Stock Option Level", [0, 1, 2, 3])
job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])
job_role = st.number_input("Job Role (encoded value)", min_value=0)  # Direct input for encoded JobRole
distance_from_home = st.number_input("Distance from Home", min_value=0)
work_life_balance = st.selectbox("Work Life Balance", [1, 2, 3, 4])

# Map 'Yes'/'No' to 1/0 for OverTime
overtime = 1 if overtime == 'Yes' else 0

# When the user clicks the "Predict" button
if st.button("Predict"):
    try:
        # Prepare the input as a DataFrame for prediction
        input_data = pd.DataFrame([[monthly_income, overtime, age, total_working_years,
                                    years_at_company, stock_option_level, job_level,
                                    job_role, distance_from_home, work_life_balance]],
                                  columns=['MonthlyIncome', 'OverTime', 'Age',
                                           'TotalWorkingYears', 'YearsAtCompany',
                                           'StockOptionLevel', 'JobLevel', 'JobRole',
                                           'DistanceFromHome', 'WorkLifeBalance'])

        # Check the type of the model and input_data
        st.write(f"Model Type: {type(rf_model)}")  # Debugging line
        st.write(f"Input Data: {input_data}")  # Debugging line

        # Perform prediction
        prediction = rf_model.predict(input_data)

        # Show result
        result = 'Yes' if prediction[0] == 1 else 'No'
        st.success(f"The prediction is: {result} (Will the employee leave?)")

    except Exception as e:
        st.error(f"Error: {str(e)}")
