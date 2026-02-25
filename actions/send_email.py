# 📧 Send Email Alert
import smtplib

def send_email(subject, message, recipient):
    sender = "your@email.com"
    body = f"Subject: {subject}\n\n{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, "your_app_password")
        server.sendmail(sender, recipient, body)
