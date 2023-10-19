import smtplib
import pytest
from unittest.mock import patch
from starlette.testclient import TestClient
from email_service import services
from fastapi import Depends
from config import config
from functools import lru_cache
from typing_extensions import Annotated

client = TestClient(services.email_service)


@lru_cache()
def get_settings():
    return config.Settings()


@patch('smtplib.SMTP_SSL')
def test_send_email_success(mock_smtp_ssl, settings: Annotated[config.Settings, Depends(get_settings)]):
    mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp_ssl

    email_data = {"to": "pihowo6543@klanze.com", "subject": "Test Subject", "message": "Test Message"}
    response = client.post("/send-email/", json=email_data)

    mock_smtp_ssl.assert_called_with(settings.SMTP_SERVER, settings.SMTP_PORT)
    mock_smtp_ssl.login.assert_called_with(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
    mock_smtp_ssl.send_message.assert_called()

    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully"}


@patch('smtplib.SMTP_SSL')
def test_send_email_failure(mock_smtp_ssl):
    mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp_ssl
    mock_smtp_ssl.login.side_effect = smtplib.SMTPAuthenticationError(500, "Email sending failed")

    with pytest.raises(Exception) as e_info:
        email_data = {"to": "pihowo6543@klanze.com", "subject": "Test Subject", "message": "Test Message"}
        client.post("/send-email/", json=email_data)

    assert e_info.value.status_code == 500
    assert "Email sending failed" in e_info.value.detail
