FROM python:3.11

WORKDIR /opt/mail_sender_app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

ADD config/erg.crt /usr/local/share/ca-certificates/erg.crt
RUN update-ca-certificates

RUN pip install -r requirements.txt
COPY . .
