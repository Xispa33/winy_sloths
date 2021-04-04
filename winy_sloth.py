#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import os
import subprocess
from time import *
from datetime import *
from constants import *
from strategy_file import *
from errors import *

class WinySloth:
    """
    A class used to represent WinySloth main object
    Attributes
    ----------
    strategies_folder_path : str
        Path of the folder containing all strategies
    
    strategies_nb : int
        Number of strategies in strategies_folder_path ( = number of .txt file in this folder)
    
    strategies : list
        List containing StrategyFile objects
    
    Methods
    -------
    WinySloth__FindNbStrategies()

    Static

    """
    def __init__(self, strategies_folder_path):
        self.strategies_folder_path = strategies_folder_path
        self.strategies_nb = self.WinySloth__FindNbStrategies()
        self.strategies = []
        init_return = self.WinySloth__Init()
        if (init_return):
            print("Init was not good.\n")
            sys.exit()
        else:
            print("Init was good.\n")
            print("There are {} strategies running.\n".format(len(self.strategies)))
            while (1):
                try:
                    self.WinySloth__Main()
                except:
                    print("An error occured. An email should have been sent around {}\n".format(str(datetime.now())))
                    with open("errors.txt", "a") as error_file:
                        errors = Errors()
                        errors.err_criticity = HIGH_C
                        error_file.write(Errors.Errors__GetRawExceptionInfo(sys.exc_info()))
                        error_file.write('\n')
                        Errors.Errors__SendEmail(errors)
                        error_file.close()
                    sleep(10)
                    self.strategies = []
                    self.__init__(strategies_folder_path)

    def WinySloth__FindNbStrategies(self):
        """
        Name : WinySloth__FindNbStrategies()
    
        Parameters : 
    
        Description : ...
        """
        shell_command = subprocess.run("ls " + self.strategies_folder_path + " | wc -l", shell=True, capture_output=True)
        number_files = shell_command.stdout.decode("utf-8").rstrip('\n')
        return number_files
    
    def WinySloth__FindAllStrategiesFiles(self):
        """
        Name : WinySloth__FindAllStrategiesFiles()
    
        Parameters : 
    
        Description : 
        """
        return (os.listdir(self.strategies_folder_path))
    
    def WinySloth__Init(self):
        """
        Name : WinySloth__Init()
    
        Parameters : 
    
        Description : 
        """
        try:
            strategies_files_list = self.WinySloth__FindAllStrategiesFiles()

            for strategy in strategies_files_list:
                strategy_path = self.strategies_folder_path + strategy
                
                with open(strategy_path, "r") as strategy_file:
                    content = strategy_file.readlines()
                    master_info = content[0].strip('\n').split(" ")
                    slave_info = content[2:]
                    strategy_file_object = StrategyFile(strategy_path, master_info, slave_info)
                    self.strategies.append(strategy_file_object)
                    strategy_file.close()
            return 0
        except:
            return 1
    
    def WinySloth__ComputeAccountSide(self, master_api, binance_response):
        """
        Name : WinySloth__ComputeAccountSide(master_api, binance_response)
    
        Parameters : 
    
        Description : 
        """
        if (isinstance(binance_response, int)):
            return 1
        else:
            if (master_api.account_type == SPOT):
                binance_response = binance_response[0]
                if binance_response[SIDE] == BUY: 
                    return LONG
                elif binance_response[SIDE] == SELL:
                    return OUT
                else:
                    return 1
            elif (master_api.account_type == FUTURES):
                
                if (len(binance_response) > 1):
                    entry_price_1 = float(binance_response[0][ENTRY_PRICE])
                    entry_price_2 = float(binance_response[1][ENTRY_PRICE])
                    entry_price_3 = float(binance_response[2][ENTRY_PRICE])
                    if (entry_price_1 != float(0)) or (entry_price_2 != float(0)):
                        master_api.markPrice = round(float(binance_response[1][MARK_PRICE]), 0)
                        master_api.entryPrice = round(float(binance_response[1][ENTRY_PRICE]), 0)
                        master_api.leverage = binance_response[1][LEVERAGE]
                        master_api.positionAmt = float(binance_response[1][POSITION_AMT])
                        master_api.balance = float(I__GET_FUTURES_ACCOUNT_BALANCE(Client(master_api.api_key, master_api.api_secret_key))[0]['balance'])
                        master_api.computeEngagedBalance()
                        return LONG
                    elif (entry_price_1 == float(0) and entry_price_2 == float(0) and entry_price_3 == float(0)):
                        return OUT
                    elif (entry_price_3 != float(0)):
                        master_api.markPrice = round(float(binance_response[2][MARK_PRICE]), 0)
                        master_api.entryPrice = round(float(binance_response[2][ENTRY_PRICE]), 0)
                        master_api.leverage = binance_response[2][LEVERAGE]
                        master_api.positionAmt = float(binance_response[2][POSITION_AMT])
                        master_api.balance = float(I__GET_FUTURES_ACCOUNT_BALANCE(Client(master_api.api_key, master_api.api_secret_key))[0]['balance'])
                        master_api.computeEngagedBalance()
                        return SHORT
                    else:
                        return 1
                else:
                    # Store needed information for FUTURES account
                    master_api.markPrice = round(float(binance_response[0][MARK_PRICE]), 0)
                    master_api.entryPrice = round(float(binance_response[0][ENTRY_PRICE]), 0)
                    master_api.leverage = binance_response[0][LEVERAGE]
                    master_api.positionAmt = float(binance_response[0][POSITION_AMT])
                    #TODO: A modifier pour grer les cas derreur
                    master_api.balance = float(I__GET_FUTURES_ACCOUNT_BALANCE(Client(master_api.api_key, master_api.api_secret_key))[0]['balance'])
                    master_api.computeEngagedBalance()
                    
                    if (master_api.positionAmt == float(0)):
                        return OUT
                    elif (master_api.positionAmt < 0):
                        return SHORT
                    elif (master_api.positionAmt > 0):
                        return LONG
                    else: 
                        return 1
            else:
                return 1

    def WinySloth__UpdateStrategyFile(self, strategy_file_path, strategy_current_side, idx=0):
        """
        Name : WinySloth__UpdateStrategyFile(strategy_file_path, strategy_current_side, idx=0)
    
        Parameters : 
    
        Description : 
        """
        if (idx != 0):
            idx = 1+idx

        try :
            with open(strategy_file_path, 'r') as strategy_file:
                info = strategy_file.readlines()
                strategy_file.close()

            with open(strategy_file_path, "w") as strategy_file:
                master_info = info[idx]
                master_info = master_info.strip('\n').split(" ")
                master_info[2] = strategy_current_side
                info[idx] = master_info
                info[idx] = " ".join(info[idx]) + '\n'
                strategy_file.writelines(info)   
                strategy_file.close()
            return 0
        except:
            return 1
    
    def WinySloth__UpdatePositionSide(self, strategy, strategy_current_side, idx=0):
        """
        Name : WinySloth__UpdatePositionSide(strategy, strategy_current_side, idx=0)
    
        Parameters : 
    
        Description : 
        """
        if (idx != 0):
            idx = 1+idx
        
        try:
            with open(strategy.strategy_file_path, "r") as strategy_file:
                content = strategy_file.readlines()
                master_info = content[idx].strip('\n').split(" ")
                master_info_side = master_info[2]
                if (master_info_side == strategy_current_side):
                    if (idx == 0):
                        strategy.master_api.side = master_info_side
                    else:
                        strategy.slave_apis[idx - 2].side = strategy_current_side
                    return 0
                else:
                    return 1
                strategy_file.close()
        except:
            return 1

    def WinySloth__UpdateMaster(self, strategy, strategy_current_side):
        """
        Name : WinySloth__UpdateMaster(strategy, strategy_current_side)
    
        Parameters : 
    
        Description : 
        """
        update_file = 1
        update_object = 1

        update_file = self.WinySloth__UpdateStrategyFile(strategy.strategy_file_path, strategy_current_side)
        update_object = self.WinySloth__UpdatePositionSide(strategy, strategy_current_side)

        if (update_file == 1 or update_object == 1):
            return 1
        else:
            return 0
    
    def WinySloth__UpdateSlave(self, strategy, strategy_current_side, idx):
        """
        Name : WinySloth__UpdateSlave(strategy, strategy_current_side, idx)
    
        Parameters : 
    
        Description : 
        """
        update_file = 1
        update_object = 1

        update_file = self.WinySloth__UpdateStrategyFile(strategy.strategy_file_path, strategy_current_side, idx)
        update_object = self.WinySloth__UpdatePositionSide(strategy, strategy_current_side, idx)

        if (update_file == 1 or update_object == 1):
            return 1
        else:
            return 0
                                           
    def WinySloth__SlaveManagement(self, strategy):
        """
        Name : WinySloth__SlaveManagement(strategy)
    
        Parameters : 
    
        Description : 
        """
        idx = 1
        for slave in strategy.slave_apis:
            ret_update_slave = 1
            side_possibilities_dict = {(OUT,LONG):slave.close_long, (OUT,SHORT):slave.close_short, \
                                       (LONG,OUT):slave.open_long, (SHORT,OUT):slave.open_short, \
                                       (LONG,SHORT):slave.open_long_from_short, (SHORT,LONG):slave.open_short_from_long}
            
            if (slave.side != strategy.master_api.side):
                exec_trade_function = side_possibilities_dict[strategy.master_api.side, slave.side](strategy.master_api)
                if exec_trade_function == 0:
                    ret_update_slave = self.WinySloth__UpdateSlave(strategy, strategy.master_api.side, idx)
                    if ret_update_slave == 0:
                        return 0
                    else:
                        return 1
                else:
                    #send mail
                    errors = Errors()
                    errors.err_criticity = HIGH_C
                    errors.error_messages = "Trade function returned an error"
                    Errors.Errors__SendEmail(errors)
                    return 1
            else:
                return 0
            
            idx = idx + 1
            sleep(1)
 
        return 0

    def WinySloth__Main(self):
        """
        Name : WinySloth__Main()
    
        Parameters : 
    
        Description : Main function of a Winy_Sloth object. This function is going through each strategy
        in the strategy list. For each strategy, the master's position in the strategy file is compared with
        the master's position given from Binance. In case of difference, the position of each slave is updated
        copying the master's position. If a position changes or if an error occurs, an email is sent
        """
        for strategy in self.strategies:
            ret_update_master = 1
            ret_update_slave = 1
            binance_return = I__GET_ACCOUNT_HISTORY(Client(strategy.master_api.api_key, \
                                                    strategy.master_api.api_secret_key), \
                                                    strategy.master_api.account_type, strategy.master_api.symbol)
            #print(binance_return)
            strategy_current_side = self.WinySloth__ComputeAccountSide(strategy.master_api, binance_return)
            if (strategy_current_side != strategy.master_api.side):
                #print("Position not up to date")
                ret_update_master = self.WinySloth__UpdateMaster(strategy, strategy_current_side)
                #gESTION DES SLAVES 
                if (ret_update_master == 0):
                    ret_update_slave = self.WinySloth__SlaveManagement(strategy)
                    if (ret_update_slave == 0):
                        #sendemail
                        errors = Errors()
                        errors.err_criticity = INFO_C
                        errors.error_messages = "Master + Slave update successful"
                        Errors.Errors__SendEmail(errors)
                    else:
                        #sendemail
                        errors = Errors()
                        errors.err_criticity = HIGH_C
                        errors.error_messages = "Slave update unsuccessful"
                        Errors.Errors__SendEmail(errors)
                        sys.exit()
                else:
                    #sendemail
                    errors = Errors()
                    errors.err_criticity = HIGH_C
                    errors.error_messages = "Master update unsuccessful. "
                    Errors.Errors__SendEmail(errors)
                    sys.exit()
            else:
                sleep(2)
                #print("Position up to date\n")