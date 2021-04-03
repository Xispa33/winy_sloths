#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
from winy_sloth import *

if __name__ == "__main__":
    while (1):
        try:
            main_obj = WinySloth(STRATEGIES_FOLDER)
        except:
            with open("errors.txt", "a") as error_file:
                errors = Errors()
                error_file.write(Errors.Errors__GetRawExceptionInfo(sys.exc_info()))
                error_file.write('\n')
                error_file.close()
            sleep(10)