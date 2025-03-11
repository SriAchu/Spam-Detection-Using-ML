import joblib
import pandas as pd
from dataProcessing import prepare_features

# Load models and vectorizers
email_model = joblib.load('C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/emailSpamModel.pkl')
email_vectorizer = joblib.load('C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/emailVec.pkl')

sms_model = joblib.load('C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/smsSpamModel.pkl')
sms_vectorizer = joblib.load('C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/smsVec.pkl')

def predictSpam(text, model, vectorizer):
    data = pd.DataFrame([text], columns=['Category'])
    features, _ = prepare_features(data, vectorizer)
    prediction = model.predict(features)
    return "Spam" if prediction[0] == 1 else "Not Spam"
