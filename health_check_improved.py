#!/usr/bin/env python3

import psutil
import time
import socket
import os
import smtplib
import logging
from email.message import EmailMessage

# Set up basic logging configuration

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the thresholds for CPU, disk and virtual memory usage.

CPU_THRESHOLD = 80              # set your cpu usage threshold in percentage
DISK_THRESHOLD = 45831193600    # set your disk usage threshold in KB
MEMORY_THRESHOLD = 11524288000  # set your virtual memory threshold in KB

# email settings

EMAIL_SENDER_ACCOUNT = ''
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD', '')
EMAIL_RECIPIENT_ACCOUNT = ''


# Function to generate email

def send_email(subject: str) -> None:
    """Sends an email to the gmail recipient account with subject

    :param subject: subject of the email
    """

    # set email variables
    message = EmailMessage()
    message['From'] = EMAIL_SENDER_ACCOUNT
    message['To'] = EMAIL_RECIPIENT_ACCOUNT
    email_body = "Please check your system and resolve the issue as soon as possible."
    message.set_content(email_body)
    message['subject'] = subject

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start the TLS connection
        server.starttls()
        # Login to the Gmail account
        server.login(EMAIL_SENDER_ACCOUNT, EMAIL_SENDER_PASSWORD)
        # send email
        server.send_message(message)


# health checks

def main():
    """Checks system health. if issue, sends email notification."""

    while True:

        # report an error if CPU usage is over 80%
        cpu_percent = psutil.cpu_percent()
        if cpu_percent > CPU_THRESHOLD:
            logging.error('CPU usage is over 80%')
            send_email('Error - CPU usage is over 80%')

        # report an error if available disk space is lower than 20%
        disk_space = psutil.disk_usage('/')
        if disk_space.free < DISK_THRESHOLD:
            logging.error('Available disk is less than 45GB')
            send_email('Error - Available disk is less than 45GB')

        # report an error if available memory is less than 500MB
        memory = psutil.virtual_memory()
        if memory.available < MEMORY_THRESHOLD:
            logging.error('Available memory is less than 500MB')
            send_email('Error - Available memory is less than 500MB')

        # report an error if the hostname 'localhost' cannot be resolved to 127.0.0.1
        try:
            localhost_ip = socket.gethostbyname('localhost')
            if localhost_ip == '127.0.0.1':
                logging.info('localhost resolves to 127.0.0.1')
            else:
                logging.warning('localhost resolves to a different IP address')
        except socket.gaierror:
            logging.error('localhost can\'t resolve to 127.0.0.1')
            send_email('Error - localhost cannot be resolved to 127.0.0.1')

        time.sleep(30)


if __name__ == "__main__":
    main()