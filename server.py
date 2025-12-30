import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

class SubmitRequest(BaseModel):
    message: str
    runner_id: str

@app.post("/submit")
def submit_result(req: SubmitRequest):
    sender = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    recipient = sender  # or change to any address you want

    msg = MIMEText(req.message)
    msg["Subject"] = f"Runner {req.runner_id} report"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())

    return {"status": "sent", "message": req.message, "runner_id": req.runner_id}