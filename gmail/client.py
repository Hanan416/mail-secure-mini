import smtplib
import os
import hashlib
import random
import mimetypes
from email.message import EmailMessage

EMAIL_ADDRESS = 'miniproject201bgu@gmail.com'
EMAIL_PASSWORD = 'bgu12345'
ATTACHMENTS_FOLDER = '\\toSend'
KNOWN_VIRUSES = ['00446F6D', '50616E646F7261', '00466C616D65']
hash_code = hashlib.sha1()


def attach_virus(f):
    buf = f.read()
    hash_code.update(buf)
    hex_ret = hash_code.hexdigest()
    rand = random.random()
    if rand <= 0.4:
        rand_ind = round(random.random() * (len(KNOWN_VIRUSES)-1))
        hex_ret = hash_code.hexdigest() + KNOWN_VIRUSES[rand_ind]

    return hex_ret, buf


def get_attachment_paths():
    os.chdir(os.getcwd() + ATTACHMENTS_FOLDER)
    dir_list = os.listdir()
    print('dir list:', dir_list, '\n')
    return dir_list


def sendmail(protocol, subject, body, sender, receiver, attachment_name, attachment_subtype):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)

    attachment_maintype = mimetypes.guess_type(file_name)[0].split('/')[0]
    msg.add_attachment(file_data, maintype=attachment_maintype, subtype=attachment_subtype, filename=attachment_name)
    protocol.send_message(msg)


with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    list_of_files = get_attachment_paths()
    counter = 1
    for file_name in list_of_files:
        print('working on file:', file_name)
        with open(file_name, 'rb') as file:
            file_ext = os.path.splitext(file_name)[1]
            hex_val, file_data = attach_virus(file)

            if any(virus in str(hex_val) for virus in KNOWN_VIRUSES):
                print('!!!! ALERT !!!!!\n'
                      'a virus was found in file', file_name,'\n'
                      'not sending..\n')
                file.close()
            else:
                print('file is ok, sending to mail\n')
                sendmail(smtp, 'File transfer test' + str(counter), 'Some Generic Body',
                         EMAIL_ADDRESS, EMAIL_ADDRESS, file_name, file_ext)
                counter = counter + 1
    print('initial file amount:', (len(list_of_files)),
          '\ntotal filtered:', (len(list_of_files) - counter + 1),
          '\ntotal sent:', counter - 1)
    smtp.quit()
