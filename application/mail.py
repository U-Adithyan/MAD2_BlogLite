import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "bloglite2@example.com"
SENDER_PASSWORD = ""

def send_mail(address,subject,message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = address
    msg["Subject"] = subject

    msg.attach(MIMEText(message,"html"))

    sender = smtplib.SMTP(host = SMPTP_SERVER_HOST,port = SMPTP_SERVER_PORT)
    sender.login(SENDER_ADDRESS,SENDER_PASSWORD)
    sender.send_message(msg)
    sender.quit()
    return True
