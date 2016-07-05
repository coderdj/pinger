from pexpect import pxssh
from datetime import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

last_ping = datetime.now()
target = '130.92.139.19'
uname = 'xedaq'
pw = 'secret'
email = "BernXenonNotification@gmail.com"

recepients = [
    "daniel.coderre@lhep.unibe.ch",
]

def SendEmail(subject, message):

    # Login to server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, pw)

    for address in recepients:

        # Build the message
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = address
        msg['Subject'] = subject

        body = message
        msg.attach(MIMEText(body, 'plain'))    

        text = msg.as_string()
        server.sendmail(email, address, text)
    server.quit()

SendEmail("test", "test_message")

while(1):

    s = pxssh.pxssh()
    if s.login(target, uname, pw):
        last_ping = datetime.now()
        print("Successful login at " + str(last_ping))
        s.logout()
    else:
        print("Couldn't login at " + str(last_ping) + ": " + str(s))

    # Check latency (60 seconds)
    nowtime = datetime.now()
    if (nowtime - last_ping).total_seconds() >60:
        print("Holy cow man, your computer is down!")
        SendEmail("Couldn't login to server " + target + " for the last " +
                  str((nowtime - last_ping).total_seconds()) + " seconds!"+
                  " Maybe check on that.")
        # do something

    time.sleep(15)
