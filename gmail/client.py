import smtplib
import os
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = "miniproject201bgu@gmail.com"
EMAIL_PASSWORD = "bgu12345"

contacts = [EMAIL_ADDRESS]  # Add more later

with open('BO.jpg', 'rb') as f:
    file_data = f.read()
    file_name = f.name
    file_subtype = imghdr.what(file_name)


def sendmail(protocol, subject, body, sender, receiver):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)

    print("setting msg filename: ", file_name)
    print("setting msg filedata: ", file_data)
    print("setting msg file subtype: ", file_subtype)

    #msg.add_attachment(file_data, maintype='image', subtype=file_subtype, filename=file_name)

    protocol.sendmail(sender, receiver, msg)


with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    sendmail(smtp,
             'Testing file transfer',
             'text file attached to this mail',
             EMAIL_ADDRESS,
             EMAIL_ADDRESS)

