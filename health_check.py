#! /usr/bin/env python3

import psutil
import time
import socket
from email.message import EmailMessage
import smtplib

#Email variables


message = EmailMessage()
sender = 'automation@example.com'
recipient = 'username@example.com'  # replace with username in the connection details panel
message['From'] = sender
message['To'] = recipient
email_body = "Please check your system and resolve the issue as soon as possible."
message.set_content(email_body)

#Setting up the mail server

mail_server = smtplib.SMTP('localhost')


# Set the thresholds for high CPU usage, low disk space and high virtual memory usage. 

cpu_threshold = 80
disk_threshold = 20
memory_threshold = 524288000


while True:


#report an error if CPU usage is over 80%

	cpu_percent = psutil.cpu_percent()

	if cpu_percent > cpu_threshold:
		print("Error - CPU usage is over 80%")
		message['subject'] = "Error - CPU usage is over 80%"
		mail_server.send_message(message)


#report an error if available disk space is lower than 20%


	disk_space = psutil.disk_usage('/')

	if disk_space.total < disk_threshold:
		print("Error - Available disk space is less than 20%")
		message['subject'] = "Error - Available disk space is less than 20%"
		mail_server.send_message(message)

#report an error if available memory is less than 500MB


	memory = psutil.virtual_memory() 

	if memory.available < memory_threshold:
		print("Error - Available memory is less than 500MB")
		message['subject'] = "Error - Available memory is less than 500MB"
		mail_server.send_message(message)


#report an error if the hostname 'localhost' cannot be resolved to '127.0.0.1'


	try:
		localhost_ip = socket.gethostbyname('localhost')


		if localhost_ip == '127.0.0.1':
			print("localhost resolves to 127.0.0.1")
		else:
			print("localhost resolvers to a different IP address")

	except socket.gaierror:
		print("Error - localhost cannot be resolved to 127.0.0.1")
		message['subject'] = "Error - localhost cannot be resolved to 127.0.0.1"
		mail_server.send_message(message)
 

	#Sleep for 60 seconds before the next check 
	time.sleep(60)








