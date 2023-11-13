import os
import smtplib
from email.message import EmailMessage

EMAIL_SENDER_ACCOUNT = ''
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD', '')
EMAIL_RECIPIENT_ACCOUNT = ''
SMTP_SERVER_URL = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587

class EmailNotifier():

    def __init__(self, sender, sender_password) -> None:

        self.sender = sender
        self.sender_password = sender_password

        self.authenticate()

        
    def authenticate(self):
        # authenticate credentials
        with smtplib.SMTP(SMTP_SERVER_URL, SMTP_SERVER_PORT) as server:
            # Start the TLS connection
            server.starttls()
            # Login to the Gmail account
            server.login(self.sender, self.sender_password)
    

    def sendEmail(self, recipient: str, subject: str):
        """_summary_

        :param recipient: _description_
        :type recipient: _type_
        :param subject: _description_
        :type subject: _type_
        """        

        # set email variables
        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = recipient
        email_body = "Please check your system and resolve the issue as soon as possible."
        message.set_content(email_body)
        message['subject'] = subject

        # send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            # Start the TLS connection
            server.starttls()
            # Login to the Gmail account
            server.login(self.sender, self.sender_password)
            # send email
            server.send_message(message)
