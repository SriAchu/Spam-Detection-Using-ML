import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
import random
from spamDetection import detect
import pandas as pd
import joblib

TWILIO_ACCOUNT_SID = 'AC52d39d7fc28f6dc559f76f08b85f1343'
TWILIO_AUTH_TOKEN = '544de53a1fb92b3687cdc200db29f2f8'
TWILIO_PHONE_NUMBER = '+14845529112'

USERNAME = "admin"
PASSWORD = "password123"

otp_sent_to = None  
generated_otp = None

ePath="C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Data/email_dataset.csv"
sPath="C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Data/sms_dataset.csv"

def load_dataset(model_type):
    if model_type == "email":
        return pd.read_csv(ePath)
    elif model_type == "sms":
        return pd.read_csv(sPath, encoding='ISO-8859-1')
    
    
# Function to validate email format
def validate_email(email):
    if "@" in email and "." in email:
        return True
    return False



def send_sms_otp(mobile_number):
    global generated_otp, otp_sent_to
    generated_otp = str(random.randint(1000, 9999))
    otp_sent_to = "sms"
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            to=f"+91{mobile_number}",
            from_=TWILIO_PHONE_NUMBER,
            body=f"Your OTP is: {generated_otp}",
        )
        messagebox.showinfo("Success", "OTP sent to your mobile number!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP:\n{e}")


def verify_otp(entered_otp, root):
    if entered_otp == generated_otp:
        messagebox.showinfo("Success", "OTP Verified!")
        root.destroy() 
        open_spam_detection_screen("sms") 
    else:
        messagebox.showerror("Error", "Incorrect OTP. Please try again.")

def load_trained_model(model_path, vectorizer_path):
    # Load the trained model and vectorizer from disk
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def open_spam_detection_screen(modelType):
    detection_window = tk.Toplevel()
    detection_window.title("Spam Detection")

    tk.Label(detection_window, text="Enter Message Content:").pack(pady=5)
    content_box = tk.Text(detection_window, height=10, width=50)
    content_box.pack(pady=10)

    if modelType == 'email':
        model, vectorizer = load_trained_model("C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/emailSpamModel.pkl",
                                               "C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/emailVec.pkl")
    elif modelType == 'sms':
        model, vectorizer = load_trained_model("C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/smsSpamModel.pkl",
                                               "C:/Users/Krishna/Desktop/Engg/Sem - 3/Fundamentals of AI/SpamDetectionUsingML/Models/smsVec.pkl")

    def run_detection():
        content = content_box.get("1.0", tk.END).strip()
        if content:
            # Transform the input message using the same vectorizer
            transformed_content = vectorizer.transform([content])
            
            # Predict if the message is spam or not
            result = model.predict(transformed_content)[0]  # get the first prediction

            # Show the result
            if result == 'spam':  # Adjust according to how your model labels spam
                messagebox.showinfo("Result", "Spam")
            else:
                messagebox.showinfo("Result", "Not Spam")
    tk.Button(detection_window, text="Detect Spam", command=run_detection).pack(pady=10)


def open_sms_verification():
    sms_window = tk.Toplevel()
    sms_window.title("SMS Verification")

    tk.Label(sms_window, text="Enter Mobile Number:").pack(pady=5)
    mobile_entry = tk.Entry(sms_window, width=30)
    mobile_entry.pack(pady=5)

    def send_and_verify():
        mobile_number = mobile_entry.get().strip()
        if mobile_number.isdigit() and len(mobile_number) == 10:
            send_sms_otp(mobile_number)
            otp_window = tk.Toplevel(sms_window)
            otp_window.title("Enter OTP")

            tk.Label(otp_window, text="Enter OTP:").pack(pady=5)
            otp_entry = tk.Entry(otp_window, width=10)
            otp_entry.pack(pady=5)

            tk.Button(otp_window, text="Verify OTP", command=lambda: verify_otp(otp_entry.get(), sms_window)).pack(pady=10)
        else:
            messagebox.showerror("Error", "Invalid mobile number.")

    tk.Button(sms_window, text="Send OTP", command=send_and_verify).pack(pady=10)


def open_email_verification():
    email_window = tk.Toplevel()
    email_window.title("Email Verification")

    tk.Label(email_window, text="Enter Email:").pack(pady=5)
    email_entry = tk.Entry(email_window, width=30)
    email_entry.pack(pady=5)

    def validate_and_open_spam():
        email = email_entry.get().strip()
        if validate_email(email):
            messagebox.showinfo("Success", "Valid email format detected! Proceeding to spam detection.")
            email_window.destroy()  # Close email window
            open_spam_detection_screen("email")  # Open spam detection screen
        else:
            messagebox.showerror("Error", "Invalid email address.")

    tk.Button(email_window, text="Validate Email", command=validate_and_open_spam).pack(pady=10)

# Main Menu (after login)
def main_menu():
    menu_window = tk.Toplevel()
    menu_window.title("Main Menu")

    tk.Label(menu_window, text="Choose an Option:").pack(pady=5)

    tk.Button(menu_window, text="Email", command=open_email_verification).pack(pady=10)
    tk.Button(menu_window, text="SMS", command=open_sms_verification).pack(pady=10)

# Login Screen
def login_screen():
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root, width=20)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, width=20, show="*")
    password_entry.pack(pady=5)

    def check_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username == USERNAME and password == PASSWORD:
            messagebox.showinfo("Success", "Login Successful!")
            root.destroy()  # Close login window
            main_menu()  # Open main menu
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    tk.Button(root, text="Login", command=check_login).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    login_screen()
