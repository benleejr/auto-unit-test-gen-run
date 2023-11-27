#################################################################
### Title     :     SMTP
### Filename  :     smtp.py
### Created   :     2012
### Author    :     Joel Horowitz
### Type      :     Library
### Summary   :
###
###
#################################################################

import smtplib, os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_server, _email, _login = None, None, None
def set_credentials(server,email,login):
    global _login, _server, _email
    _login = login
    _server = server
    _email = email
    print(_server,_email,_login,'********')

def set_password(pw):
    os.environ['SMTP_PWD'] = pw

def get_password():
    return os.environ['SMTP_PWD']


def sendHTMLmailwithattachments(sender,to,subject,body,attachments = [], cc = []):
    COMMASPACE = ', '
    
    # Create the container (outer) email message.
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = _email
    if type(to)==str:
        to = [to]
    msg['To'] = COMMASPACE.join(to)
    
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    
    msgText = MIMEText(body, 'html')
    msgAlternative.attach(msgText)
    
    for FileInfo in attachments:
        fp = open(FileInfo['filename'], 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<%s>' % FileInfo['name'])
        msg.attach(msgImage)
    
    try:
        with smtplib.SMTP(_server, 587) as server:
            server.starttls()
            print(f"Logging into {_server} as {_login}...")
            server.login(_login,get_password())
            print(f"EHLO...", end="")
            server.ehlo()
            print(f"Sending mail...", end="")
            server.sendmail(sender, to, msg.as_string())
            print(f"Closing connection")
            server.quit()
        print(f"Email sent to {to}: {subject}")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    email = 'user@domain.com'
    pw = 'blah'
    set_credentials('smtp.gmail.com', email, email, pw)    
    sendHTMLmailwithattachments(email,[recipient],'Test','Body')
