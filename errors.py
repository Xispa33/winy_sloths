#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants import *


class Errors():
    """
    A class used to ...
    Attributes
    ----------
    client_file_path : list
        List of the last 5 trades made for each and every API key
    header : Header
        List of the last 5 trades made for each and every API key
    
    history : History
        List of the last 5 trades made for each and every API key
    
    init_status : list
        List of the last 5 trades made for each and every API key
    Methods
    -------
    
    """
    def __init__(self, nb_strategies = 0):
        self.error_messages   = str()
        self.error_function   = str()
        self.mail_sent        = [0] * nb_strategies
        self.err_criticity    = NO_C

    def Errors__AddMessages(self, message):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        self.error_messages += message

    def Errors__ClearMessages(self):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        self.error_messages = str()
    
    def Errors__AddFunction(self, function):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        self.error_function = function

    def Errors__UpdateCriticity(self, criticity):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        if (criticity > self.err_criticity):
            self.err_criticity = criticity
    
    @staticmethod
    def Errors__GetRawExceptionInfo(info):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        type_err =  info[0]
        error_info =  info[1]
        line_nb = info[2].tb_lineno
        return "Exception of type {} raised the following message at line {}: {} \n".format(type_err, line_nb, error_info)

    def Errors__FillErrors(self, function, message, err_criticity):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        self.Errors__AddFunction(function)
        self.Errors__AddMessages(message)
        self.Errors__UpdateCriticity(err_criticity)

    @staticmethod
    def Errors__Init(nb_strategies):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        return (Errors(nb_strategies))

    @staticmethod
    def Errors__SendEmail(errors_object):
        """
        Name : 
    
        Parameters : 
    
        Description : 
        """
        msg = MIMEMultipart(ALTERNATIVE)
        msg[SUBJECT] = "WINY SLOTHS {} NOTIFICATION".format(CORRESPONDANCE_DICT[errors_object.err_criticity]) 
        msg[FROM] = EMITTOR

        text = errors_object.error_messages

        part1 = MIMEText(text, PLAIN)

        msg.attach(part1)

        for receiver in RECEIVERS:
            msg[TO] = receiver
            context = ssl.create_default_context()
            #print("Starting to send")
            with smtplib.SMTP_SSL(STMP_URL, PORT, context=context) as server:
                server.login(EMITTOR, EMITTOR_PASSWORD)
                server.sendmail(EMITTOR, receiver, msg.as_string())
            #print("sent email!")
        
        errors_object.err_criticity = NO_C
        errors_object.error_messages = ""

