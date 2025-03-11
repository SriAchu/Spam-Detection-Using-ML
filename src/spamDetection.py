import joblib
from dataProcessing import Clean
from ModelLoading import predictSpam

# Load models and vectorizers
emailModel = joblib.load('Models/emailSpamModel.pkl')
smsModel = joblib.load('Models/smsSpamModel.pkl')
emailVectorizer = joblib.load('Models/emailVec.pkl')
smsVectorizer = joblib.load('Models/smsVec.pkl')

def detect(content, model_type="email"):
    """
    Detect spam for the given content.
    :param content: The text to classify.
    :param model_type: "email" for email spam detection, "sms" for SMS spam detection.
    :return: True if spam, False otherwise.
    """
    content_cleaned = Clean(content)
    if model_type == "email":
        content_vectorized = emailVectorizer.transform([content_cleaned])
        return emailModel.predict(content_vectorized)[0] == 1
    else:
        content_vectorized = smsVectorizer.transform([content_cleaned])
        return smsModel.predict(content_vectorized)[0] == 1

