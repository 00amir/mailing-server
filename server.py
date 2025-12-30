import os
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()

# Data model for incoming results
class Result(BaseModel):
    message: str
    runner_id: str | None = None

# Helper function to send email
def send_email(subject: str, body: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    recipient = os.getenv("EMAIL_RECIPIENT", sender)

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print("Email send failed:", e)
        raise

API_TOKEN = os.getenv("API_TOKEN")

@app.post("/submit")
def submit_result(payload: Result, x_api_token: str = Header(None)):
    if API_TOKEN and x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    subject = "Script Result Received"
    body = f"Message: {payload.message}\nRunner: {payload.runner_id or 'unknown'}"
    send_email(subject, body)
    return {"status": "ok"}