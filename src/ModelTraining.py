import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib
from dataProcessing import prepare_features

def train_model(data_path, model_path, vectorizer_path):
    data = pd.read_csv(data_path, encoding='utf-8', encoding_errors='ignore')
    
    features, vectorizer = prepare_features(data)
    
    labels = data['Category']  

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    
    model = MultinomialNB()
    model.fit(X_train, y_train)

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    accuracy = model.score(X_test, y_test)
    print(f'Model accuracy on test set: {accuracy * 100:.2f}%')

print("For email")
train_model("C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Data/balanced_email_dataset.csv", 
            "C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/emailSpamModel.pkl", 
            "C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/emailVec.pkl")

print("For sms")
train_model("C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Data/shuffled_balanced_sms_dataset.csv", 
            "C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/smsSpamModel.pkl", 
            "C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/smsVec.pkl")
