import smtplib
import ssl
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

verification_store = {}

# function to generate random password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def send_verification_code(receiver_email):

    # email details
    sender_email = "arpita.sam2k4@gmail.com"
    # receiver_email = "user_email@gmail.com"
    app_password = "anec ysmw optz dlby"   # gmail app password

    # generate random password
    new_password = generate_password()

    verification_store[receiver_email] = new_password

    # email message
    subject = "Verification Code"
    body = f"Your Verification Code is: {new_password}"
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Sent code:", new_password)

    return new_password

def verify_code(receiver_email, entered_code):
    stored_code = verification_store.get(receiver_email)
    if stored_code == entered_code:
        return True
    else:
        return False