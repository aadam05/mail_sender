import smtplib
import logging
from fastapi import APIRouter, HTTPException, Depends
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from starlette.responses import JSONResponse
from email_service.models import EmailSchema
from config import config
from functools import lru_cache
from typing_extensions import Annotated

logging.basicConfig(filename='logger/sendMail.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

email_service = APIRouter()


@lru_cache()
def get_settings():
    return config.Settings()


@email_service.post("/send-email/", tags=["send-email"])
def send_email(email_data: EmailSchema, settings: Annotated[config.Settings, Depends(get_settings)]) -> JSONResponse:

    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email_data.to
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = email_data.subject
    msg["Message"] = email_data.message

    text = MIMEText(email_data.message)
    msg.attach(text)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg, from_addr=sender_email)

        logging.info(f"Email sent to {email_data.to} with subject '{email_data.subject}'")
        return JSONResponse(content={"message": "Email sent successfully"})
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
