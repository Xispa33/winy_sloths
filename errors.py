#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from history import *
from constants import *
from header import *


class Errors():
    def __init__(self, nb_strategies = 0):
        self.error_messages   = str()
        self.error_function   = str()
        self.mail_sent        = [0] * nb_strategies
        self.err_criticity    = NO_C

    def Errors__AddMessages(self, message):
        self.error_messages += message

    def Errors__ClearMessages(self):
        self.error_messages = str()
    
    def Errors__AddFunction(self, function):
        self.error_function = function

    def Errors__UpdateCriticity(self, criticity):
        if (criticity > self.err_criticity):
            self.err_criticity = criticity
    
    @staticmethod
    def Errors__GetRawExceptionInfo(info):
        type_err =  info[0]
        error_info =  info[1]
        line_nb = info[2].tb_lineno
        return "Exception of type {} raised the following message at line {}: {} \n".format(type_err, line_nb, error_info)

    def Errors__FillErrors(self, function, message, err_criticity):
        self.Errors__AddFunction(function)
        self.Errors__AddMessages(message)
        self.Errors__UpdateCriticity(err_criticity)

    @staticmethod
    def Errors__Init(nb_strategies):
        return (Errors(nb_strategies))

    @staticmethod
    def Errors__SendEmail(errors_object):
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart(ALTERNATIVE)
        msg[SUBJECT] = "WINY SLOTHS {} NOTIFICATION".format(CORRESPONDANCE_DICT[errors_object.err_criticity]) 
        msg[FROM] = EMITTOR
        # Create the body of the message (a plain-text and an HTML version).
        #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
        text = errors_object.error_messages

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, PLAIN)

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)

        for receiver in RECEIVERS:
            msg[TO] = receiver
            context = ssl.create_default_context()
            print("Starting to send")
            with smtplib.SMTP_SSL(STMP_URL, PORT, context=context) as server:
                server.login(EMITTOR, EMITTOR_PASSWORD)
                server.sendmail(EMITTOR, receiver, msg.as_string())

            print("sent email!")
        
        errors_object.err_criticity = NO_C
        errors_object.error_messages = ""

