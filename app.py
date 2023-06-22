from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model and vectorizer
with open("model.pickle", "rb") as f:
    model = pickle.load(f)

# Define the list of questions and their corresponding column names
questions = {
    'Age': "What is the participant's age?",
    'Gender': "What is the participant's gender?",
    'Family History': "Does the participant have a family history of panic disorder? (Yes/No)",
    'Personal History': "Does the participant have a personal history of panic disorder? (Yes/No)",
    'Current Stressors': "How would you rate the current stressors in the participant's life? (Low/Moderate/High)",
    'Symptoms': "What symptoms does the participant experience? (Specify the symptoms)",
    'Severity': "How severe are the participant's panic disorder symptoms? (Mild/Moderate/Severe)",
    'Impact on Life': "How much does the participant's panic disorder impact their daily life? (Mild/Moderate/Significant)",
    'Demographics': "What is the participant's demographic? (Urban/Rural)",
    'Medical History': "Does the participant have any medical history? If yes, please specify.",
    'Psychiatric History': "Does the participant have any psychiatric history? If yes, please specify.",
    'Substance Use': "Does the participant use any substances? If yes, please specify.",
    'Coping Mechanisms': "What coping mechanisms does the participant use? (Specify the coping mechanisms)",
    'Social Support': "How would you rate the participant's social support? (Low/Moderate/High)",
    'Lifestyle Factors': "What lifestyle factors are relevant to the participant's panic disorder? (Specify the factors)"
}

@app.route('/')
def index():
    return render_template("index.html", questions=questions)

@app.route('/predict', methods=['POST'])
def predict():
    # Get user's answers from the form
    answers = {}
    for column in questions.keys():
        answers[column] = request.form.get(column)

    # Convert the answers into a DataFrame
    data = pd.DataFrame(answers, index=[0])

    # Preprocess the data using the same vectorizer used during training
    columns = ['Age', 'Gender_Male', 'Family History_Yes', 'Personal History_Yes',
       'Current Stressors_Low', 'Current Stressors_Moderate',
       'Symptoms_Dizziness', 'Symptoms_Fear of losing control',
       'Symptoms_Panic attacks', 'Symptoms_Shortness of breath',
       'Severity_Moderate', 'Severity_Severe', 'Impact on Life_Moderate',
       'Impact on Life_Significant', 'Demographics_Urban',
       'Medical History_Diabetes', 'Medical History_Heart disease',
       'Medical History_None', 'Psychiatric History_Bipolar disorder',
       'Psychiatric History_Depressive disorder', 'Psychiatric History_None',
       'Substance Use_Drugs', 'Substance Use_None',
       'Coping Mechanisms_Meditation', 'Coping Mechanisms_Seeking therapy',
       'Coping Mechanisms_Socializing', 'Social Support_Low',
       'Social Support_Moderate', 'Lifestyle Factors_Exercise',
       'Lifestyle Factors_Sleep quality']
    X = pd.get_dummies(data)
    X =  X.reindex(columns = columns, fill_value=0)

    # Make predictions using the trained model
    prediction = model.predict(X)[0]
    if prediction == 1:
        prediction = "High Chances of Panic Disorder"
    else:
        prediction = "Low Chances of Panic Disorder"

    # Render the result template with the prediction
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)


