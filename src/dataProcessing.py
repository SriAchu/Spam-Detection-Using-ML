import re
import pandas as pd
import nltk 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')

stopWords = set(stopwords.words('english'))
stemmer = PorterStemmer()

def Clean(text):
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopWords])
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text

def prepare_features(data, vectorizer=None):
    data['cleaned_text'] = data['Message'].apply(Clean)
    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=10000)
        features = vectorizer.fit_transform(data['cleaned_text'])
    else:
        features = vectorizer.transform(data['cleaned_text'])
    return features, vectorizer


