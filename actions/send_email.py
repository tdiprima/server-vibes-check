import os
import socket
import smtplib
import logging

logger = logging.getLogger(__name__)

def send_email(subject, message, recipient):
    """Send an email alert via Gmail SMTP."""
    sender = os.environ["GMAIL_SENDER"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    hostname = socket.gethostname()
    body = f"Subject: {subject}\n\nHost: {hostname}\n\n{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(sender, recipient, body)
    logger.info("Email sent", extra={"subject": subject, "recipient": recipient})
