#!/usr/bin/env python3

import psutil
import time
import socket
from email.message import EmailMessage
import smtplib
import logging

#set up basic logging configuration

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Set the thresholds for CPU,disk and virtual memory usage.

cpu_threshold = 80     #set your cpu usage threshold in percentage
disk_threshold = 45831193600  # set your disk usage threshold in KB
memory_threshold = 11524288000 # set your virtual memory threshold in KB

#Function to generate email

def send_email(subject):

    #set email variables
    message = EmailMessage()
    gmail_user = ''     #enter the email account to send emails from
    message['From'] = gmail_user
    message['To'] = ''  #enter your the recepient's email account
    gmail_password = '' #enter your password or app password in case you have 2FA activated 
    email__body = "Please check your system and resolve the issue as soon as possible."
    message.set_content(email__body)
    message['subject'] = subject
   

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start the TLS connection
        server.starttls()
        # Login to the Gmail account
        server.login(gmail_user, gmail_password)
        #send email
        server.send_message(message)


#health checks

while True:

    #report an error if CPU usage is over 80%
    cpu_percent = psutil.cpu_percent()
    if cpu_percent > cpu_threshold:
        logging.error('CPU usage is over 80%')
        send_email('Error - CPU usage is over 80%')
    

     #report an error if available disk space is lower than 20%
    disk_space = psutil.disk_usage('/')
    if disk_space.free < disk_threshold:
        logging.error('Available disk is less than 45GB')
        send_email('Error - Available disk is less than 45GB')
       

    #report an error if available memory is less than 500MB
    memory = psutil.virtual_memory()
    if memory.available < memory_threshold:
        logging.error('Available memory is less than 500MB')
        send_email('Error - Available memory is less than 500MB')


    #report an error if the hostname 'localhost' cannot be resolved to 127.0.0.1
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
    