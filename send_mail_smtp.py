from smtplib import SMTP_SSL as smtp
class Mail_Sender:
    sender = 'ivanchyshyn14@gmail.com'
    receivers = ['ivanchyshyn14@gmail.com']

    message = """From: <ivanchyshyn14@gmail.com>
To: <ivanchyshyn14@gmail.com>
Subject: SMTP e-mail test

This is an e-mail message. 
"""
    @staticmethod
    def send_mail(email, password):
        try:
            mail = smtp('smtp.gmail.com', 465)
            mail.login(email, password)
            mail.sendmail(email, Mail_Sender.receivers, Mail_Sender.message)         
            print("Successfully sent email")
        except Exception as e:
            print("Error: unable to send email")
            print(e)
