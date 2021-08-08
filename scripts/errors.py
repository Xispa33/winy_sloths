#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants import *
from time import *
from datetime import *


class Errors():
    """
    Description :
        A class used to store errors information
    
    Attributes
    ----------
    error_messages : str
        Message giving information about the nature of the error
    
    error_function : str
        Function called that raised the error
    
    error_criticity : int
        Criticity of the error message : INFO_C = INFO = 1
                                         MEDIUM_C = WARNING = 2
                                         HIGH_C = ERROR = 3
    
    mode : str
        Mode of execution. If DEBUG mode is active, no emails should be sent.
    Methods
    -------
    Errors__AddMessages()
    Errors__ClearMessages()
    Errors__AddFunction()
    Errors__UpdateCriticity()
    Errors__FillErrors()

    Static
    Errors__GetRawExceptionInfo(info)
    Errors__SendEmail(errors_object)
    """
    def __init__(self, error_messages=None, error_function=None, error_criticity=None, mode=None):
        self.error_messages   = str() if error_messages == None else error_messages
        self.error_function   = str() if error_function == None else error_function
        self.error_criticity    = NO_C if error_criticity == None else error_criticity
        self.mode    = DEBUG if mode == None else mode

    def Errors__AddMessages(self, message):
        """
        Name : Errors__AddMessages()
    
        Parameters : 
                      message : str
                        Field storing the error information
    
        Description : This function fills the error_messages field 
                      of an Error object
        """
        self.error_messages += message

    def Errors__ClearMessages(self):
        """
        Name : Errors__ClearMessages()
    
        Parameters : 
    
        Description : This function clears the error_messages field 
                      of an Error object
        """
        self.error_messages = str()
    
    def Errors__AddFunction(self, function):
        """
        Name : Errors__AddFunction()
    
        Parameters : 
                     function : str
                        Function in which an error was raised 
    
        Description : This function fills the error_function field 
                      of an Error object
        """
        self.error_function = function

    def Errors__UpdateCriticity(self, criticity):
        """
        Name : Errors__UpdateCriticity()
    
        Parameters : criticity : int
                        Criticity of the error
    
        Description : This function fills the error_criticity field 
                      of an Error object.
        """
        if (criticity > self.error_criticity):
            self.error_criticity = criticity
    
    @staticmethod
    def Errors__GetRawExceptionInfo(info):
        """
        Name : Errors__GetRawExceptionInfo()
    
        Parameters : info : list
                        List containing all information about a raised 
                        exception
    
        Description : 
        """
        type_err =  info[0]
        error_info =  info[1]
        line_nb = info[2].tb_lineno
        return "Exception of type {} raised the following message at line {}: {} \n".format(type_err, line_nb, error_info)

    def Errors__FillErrors(self, function, message, error_criticity):
        """
        Name : Errors__FillErrors(function, message, error_criticity)
    
        Parameters : function : str
                        Function in which an error was raised 

                     message : str
                        Field storing the error information

                     error_criticity : int
                        Criticity of the error
    
        Description : Function filling all fields of an error object
        """
        self.Errors__AddFunction(function)
        self.Errors__AddMessages(message)
        self.Errors__UpdateCriticity(error_criticity)

    @staticmethod
    def Errors__SendEmail(errors_object):
        """
        Name : Errors__SendEmail(errors_object)
    
        Parameters : errors_object : Error
                        Object containing all information about the error
                        raised
    
        Description : This function sends an email featuring the errors'
                      information
        """
        if (errors_object.mode != DEBUG):
            msg = MIMEMultipart(ALTERNATIVE)
            msg[SUBJECT] = "WINY SLOTHS UPDATE: {} NOTIFICATION".format(CORRESPONDANCE_DICT[errors_object.error_criticity]) 
            msg[FROM] = EMITTOR

            text = errors_object.error_messages

            part1 = MIMEText(text, PLAIN)

            msg.attach(part1)

            ret = 1

            for receiver in RECEIVERS:
                msg[TO] = receiver
                context = ssl.create_default_context()
                print("Starting to send")
                while ret == 1:
                    try:
                        with smtplib.SMTP_SSL(STMP_URL, PORT, context=context) as server:
                            server.login(EMITTOR, EMITTOR_PASSWORD)
                            server.sendmail(EMITTOR, receiver, msg.as_string())
                        ret = 0
                    except:
                        ret = 1
                        sleep(1)
                ret = 1
                print("sent email!")
            
            errors_object.error_criticity = NO_C
            errors_object.error_messages = ""
        else:
            ret = 0
        return ret

