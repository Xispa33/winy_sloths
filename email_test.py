import smtplib, ssl
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465

recieve = 'briceleal@hotmail.fr'

#message = """\
#Subject: Python Email Tutorial
#
#This is from python!
#toto
#"""
# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = 'towardsecolonomy@gmail.com'
msg['To'] = 'briceleal@hotmail.fr'
a = "RRR"
# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)

context = ssl.create_default_context()

print("Starting to send")
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #server.login('towardsecolonomy@gmail.com', 'uqkluvmbszzfykkf')
    server.login('towardsecolonomy@gmail.com', 'ricqltndktzitayp')
    server.sendmail('towardsecolonomy@gmail.com', recieve, msg.as_string())

print("sent email!")