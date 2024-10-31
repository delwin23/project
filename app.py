from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model
with open('models/rf_new_3.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the label encoders
with open('models/encoders/label_encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

# Define feature names
feature_names = [
    'MonthlyIncome', 'OverTime', 'Age', 'TotalWorkingYears',
    'YearsAtCompany', 'StockOptionLevel', 'JobLevel', 'JobRole',
    'DistanceFromHome', 'WorkLifeBalance'
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict-form')
def predict_form():
    overtime_options = list(encoders['OverTime'].classes_)
    job_role_options = list(encoders['JobRole'].classes_)
    return render_template('predict.html', 
                         overtime_options=overtime_options, 
                         job_role_options=job_role_options)

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    input_data = {
        'monthly_income': int(request.form['monthly_income']),
        'overtime': request.form['overtime'],
        'age': int(request.form['age']),
        'total_working_years': int(request.form['total_working_years']),
        'years_at_company': int(request.form['years_at_company']),
        'stock_option_level': int(request.form['stock_option_level']),
        'job_level': int(request.form['job_level']),
        'job_role': request.form['job_role'],
        'distance_from_home': int(request.form['distance_from_home']),
        'work_life_balance': int(request.form['work_life_balance'])
    }
    
    # Encode categorical features
    input_data['overtime'] = encoders['OverTime'].transform([input_data['overtime']])[0]
    input_data['job_role'] = encoders['JobRole'].transform([input_data['job_role']])[0]
    
    # Prepare data for prediction
    input_df = pd.DataFrame([[
        input_data['monthly_income'],
        input_data['overtime'],
        input_data['age'],
        input_data['total_working_years'],
        input_data['years_at_company'],
        input_data['stock_option_level'],
        input_data['job_level'],
        input_data['job_role'],
        input_data['distance_from_home'],
        input_data['work_life_balance']
    ]], columns=feature_names)
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1] * 100

    result = {
        'prediction': 'Will Leave' if prediction == 'Yes' else 'Will Stay',
        'probability': f"{probability :.2f}",
        'status': 'danger' if prediction == 'Yes' else 'success'
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)