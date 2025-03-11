from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pandas as pd

def fetch_emails(dataset_path):
    creds = Credentials.from_authorized_user_file('credentials.json')  # Ensure you have Gmail API credentials
    service = build('gmail', 'v1', credentials=creds)

    # Get the current time and time 24 hours ago
    now = datetime.utcnow()
    yesterday = now - timedelta(hours=24)

    # Search for emails from the last 24 hours
    query = f"after:{int(yesterday.timestamp())}"

    # Get messages
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    new_data = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg.get('payload', {}).get('headers', [])
        snippet = msg.get('snippet', '')  # Extract email snippet

        new_data.append({'Category': snippet, 'Message': 'unknown'})  # Add as 'unknown' for detection

    # Append to the dataset
    df = pd.read_csv("C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Data/email_dataset.csv")
    new_df = pd.DataFrame(new_data)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv("C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Data/email_dataset.csv", index=False)
