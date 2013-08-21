#! /usr/bin/python
# -*- coding: utf-8 -*- 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(subject, addresser, passwd, recipients, text='', html=''):
    # get server name from username
    mail_server = 'smtp.' + addresser.split('@')[1]
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = addresser
    msg['To'] = ';'.join(recipients)

    # Create the body of the message (a plain-text and an HTML version).
    text = text.encode('utf8')
    html = html.encode('utf8')

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    try:
        s = smtplib.SMTP()
        s.connect(mail_server)
        s.login(addresser, passwd)
        s.sendmail(addresser, recipients, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
