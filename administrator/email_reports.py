# email_reports.py
# Minimal placeholder for sending reports. Configure SMTP as needed.
import smtplib
from email.message import EmailMessage

def send_email_report(to_address, subject, body, smtp_cfg):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_cfg["from"]
    msg["To"] = to_address
    msg.set_content(body)
    with smtplib.SMTP(smtp_cfg["host"], smtp_cfg.get("port", 25)) as s:
        if smtp_cfg.get("starttls"):
            s.starttls()
        if smtp_cfg.get("username"):
            s.login(smtp_cfg["username"], smtp_cfg["password"])
        s.send_message(msg)
