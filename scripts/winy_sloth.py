#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import os
import subprocess
from time import *
from datetime import *
from constants import *
from strategy_file import *
from crypto_exchange_platform import *
from errors import *
import traceback
import argparse
import time
import csv

class WinySloth:
    """
    A class used to represent WinySloth main object. The general behaviour \
    of Winy Sloth is described in Documentation.

    Attributes
    ----------
    strategies_folder_path : str
        Path of the folder containing all strategies
    
    strategies : list
        List containing StrategyFile objects
    
    mode : str
        Variable specifiying WS mode of execution.
        In DEBUG mode, WS is executed during 40s only.
        In RUN mode, WS runs nominally.

    init_return outputs the return of initialization. If init_return is equal to 1, \
    it means a problem occurred during initialization and the program exits. \
    If 0, init was OK and WS enters in main. 
    
    Methods
    -------
    WinySloth__ReadArguments()
    WinySloth__FindNbStrategies()
    WinySloth__FindAllStrategiesFiles()
    WinySloth__Init()
    WinySloth__UpdateStrategyFile()
    WinySloth__UpdatePositionSide()
    WinySloth__Update()
    Winy_Sloth__SendEmail()
    WinySloth__SlaveManagement()
    WinySloth__Main()
    """
    def __init__(self):
        (self.mode, \
        self.strategies_folder_path, \
        self.history_file) = self.WinySloth__ReadArguments()
        self.strategies = []
        init_return = self.WinySloth__Init()
        if (init_return):
            print("Init was not good.\n")
            sys.exit()
        else:
            print("Init was good.\nThere are {} strategies running.\
            \n".format(len(self.strategies)))
            if (self.mode == RUN):
                while (1):
                    try:
                        self.WinySloth__Main()
                    except:
                        message = "An error occured. An email should have been sent around {}\n \
                        {}\n {}\n".format(str(datetime.now()), sys.exc_info(), \
                        traceback.format_exc())
                        print(message)
                        
                        with open(ERRORS_FILE, "a+") as error_file:
                            mail_msg = "WARNING : \
                                Winy Sloth had to restart.\nThe error raised the following \
                                message: \nsys.exc_info() = {}. traceback.format_exc() = {}. \
                                ".format(sys.exc_info(), traceback.format_exc())

                            error = Errors(error_messages=mail_msg, error_criticity=HIGH_C, \
                                            mode = self.mode)
                            Errors.Errors__SendEmail(error)
                            error_file.write(message)
                            error_file.close()
                        sleep(2)
                        self.strategies = []
                        self.__init__()

            elif (self.mode == DEBUG):
                start_time = time.time()
                end_time = time.time()

                while (end_time - start_time < 40.0):
                    self.WinySloth__Main()
                    end_time = time.time()
                print("0")

    def WinySloth__ReadArguments(self):
        """
        Name : WinySloth__ReadArguments()
    
        Parameters : 
    
        Description : 
        """
        mode = ERROR_MODE
        strat_folder_path = ""
        stat_folder_path = ""

        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mode", type=str, choices=['d', DEBUG, RUN], default='run', help="Mode of execution")
        parser.add_argument("-f", "--folder", type=str, default='strategies', help="Path of the folder containing strategy files")
        parser.add_argument("-p", "--history", type=str, default='stats', help="Path of the folder containing statistics files")
        
        args = parser.parse_args()
        if (args.mode == 'run'):
            mode = RUN
        elif ((args.mode == 'd') or (args.mode == DEBUG)):
            mode = DEBUG
        else:
            mode = ERROR_MODE
        
        if (os.path.exists(os.path.join(os.getcwd(), args.folder))):
            strat_folder_path = args.folder
        else:
            strat_folder_path = ERROR_STRATEGY_PATH_FOLDER
        
        if (os.path.exists(os.path.join(os.getcwd(), args.history))):
            stat_folder_path = args.history + "/" + HISTORY_FILE_NAME
        else:
            stat_folder_path = ERROR_STATISTICS_PATH_FOLDER
        
        return (mode, strat_folder_path, stat_folder_path)
    
    def WinySloth__FindNbStrategies(self):
        #NOT USED
        """
        Name : WinySloth__FindNbStrategies()
    
        Parameters : 
    
        Description : Function that returns the number of strategies of a
                      WinySloth object. 
        """
        if (self.strategies_folder_path != ERROR_STRATEGY_PATH_FOLDER):
            shell_command = subprocess.run("ls " + self.strategies_folder_path \
                                    + " | wc -l", shell=True, capture_output=True)
            number_files = shell_command.stdout.decode("utf-8").rstrip('\n')
            return int(number_files)
        else:
            return -1
    
    def WinySloth__FindAllStrategiesFiles(self):
        """
        Name : WinySloth__FindAllStrategiesFiles()
    
        Parameters : 
    
        Description : Function that returns all strategy file of a
                      WinySloth object. 
        """
        files_list = os.listdir(self.strategies_folder_path)
        out_list = []
        for _file in files_list:
            if (_file[-len(TXT):] == TXT):
                out_list.append(_file)
        return (out_list)
    
    def WinySloth__Init(self):
        """
        Name : WinySloth__Init()
    
        Parameters : 
    
        Description : Initialisation of a WinySloth object
        """
        if ((self.strategies_folder_path != ERROR_STRATEGY_PATH_FOLDER) and \
            (self.mode != ERROR_MODE) and (self.history_file != ERROR_STATISTICS_PATH_FOLDER)):
            try:
                strategies_files_list = self.WinySloth__FindAllStrategiesFiles()

                for strategy in strategies_files_list:
                    strategy_path = self.strategies_folder_path + '/' + strategy
                    
                    with open(strategy_path, "r") as strategy_file:
                        content = strategy_file.readlines()
                        master_info = content[0].strip('\n').split(" ")
                        slave_info = content[OFFSET_SLAVE_IN_STRATEGY_FILE:]
                        strategy_file_object = StrategyFile(strategy_path, master_info, slave_info)
                        self.strategies.append(strategy_file_object)
                        strategy_file.close()
                return 0
            except:
                print("An error during the reading of strategy file {}.\n \
                {} {}".format(strategy_path.split('/')[-1][:-len(TXT)], sys.exc_info(), \
                traceback.format_exc()))
                return 1
        else:
            return 1

    def WinySloth__UpdateStrategyFile(self, strategy_file_path, strategy_current_side, idx=0):
        # TODO: Changer peut etre cette fonction en supprimant le strategy_current_side
        """
        Name : WinySloth__UpdateStrategyFile(strategy_file_path, strategy_current_side, idx=0)
    
        Parameters : 
                      strategy_file_path : str
                        Path of the folder containing all strategies
                    
                      strategy_current_side : str
                        New side of the strategy 

                      idx : int (optionnal)
                        Index of the strategy. This parameter indicates the line
                        to modify in the strategy file. If the master has to be
                        updated, idx = 0, else, idx = 1 + slave_idx

        Description : Function updating a strategy file
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
                master_info[OFFSET_SIDE] = strategy_current_side
                info[idx] = master_info
                info[idx] = " ".join(info[idx]) + '\n'
                strategy_file.writelines(info)
                strategy_file.close()
            return 0
        except:
            print("An error during the update of strategy file {}.\n \
                {} {}".format(strategy_file_path.split('/')[-1][:-len(TXT)], sys.exc_info(), \
                traceback.format_exc()))
            return 1
    
    def WinySloth__UpdatePositionSide(self, strategy, strategy_current_side, idx=0):
        """
        Name : WinySloth__UpdatePositionSide(strategy, strategy_current_side, idx=0)
    
        Parameters : 
                      strategy : StrategyFile
                        StrategyFile object to be updated
                    
                      strategy_current_side : str
                        New side of the strategy 
                      
                      idx : int (optionnal)
                        Index of the strategy. This parameter indicates the line
                        of the strategy file in which the master/slave is. If the 
                        master has to be updated, idx = 0, else, idx = 1 + slave_idx
    
        Description : Function updating the position side of a strategy object
                      during the code execution
        """
        if (idx != 0):
            idx = 1+idx
        
        try:
            with open(strategy.strategy_file_path, "r") as strategy_file:
                content = strategy_file.readlines()
                info_account = content[idx].strip('\n').split(" ")
                info_side = info_account[OFFSET_SIDE]
                # Update of master OR slave
                if (info_side == strategy_current_side):
                    if (idx == 0):
                        strategy.master_api.side = info_side
                    else:
                        strategy.slave_apis[idx - OFFSET_SLAVE_IN_STRATEGY_FILE].side = strategy_current_side
                    strategy_file.close()
                    return 0
                else:
                    strategy_file.close()
                    return 1
        except:
            print("An error during the update of the position side of {}.\n \
                {} {}".format(strategy.strategy_file_path.split('/')[-1][:-len(TXT)], sys.exc_info(), \
                traceback.format_exc()))
            return 1

    def WinySloth__Update(self, strategy, strategy_current_side, idx=0):
        """
        Name : WinySloth__Update(strategy, strategy_current_side, idx=0)
    
        Parameters : 
                      strategy : StrategyFile
                        StrategyFile object to be updated
                    
                      strategy_current_side : str
                        New side of the strategy for the master
    
        Description : Function that updates all needed information for a 
                      master
        """
        update_file = 1
        update_object = 1

        if (idx == 0):
            # If Master has to be updated
            update_file = self.WinySloth__UpdateStrategyFile(strategy.strategy_file_path, \
                                                                strategy_current_side)
            update_object = self.WinySloth__UpdatePositionSide(strategy, \
                                                                strategy_current_side)
        else:
            # If Slaves have to be updated
            update_file = self.WinySloth__UpdateStrategyFile(strategy.strategy_file_path, strategy_current_side, idx)
            update_object = self.WinySloth__UpdatePositionSide(strategy, strategy_current_side, idx)
        if (update_file == 1 or update_object == 1):
            return 1
        else:
            return 0

    def Winy_Sloth__SendEmail(self, account_type, strategy, \
                              side, exec_trade_function=0, \
                              idx=0, ret_update_master=0, \
                              ret_update_slave=0, ep_platform_found=1):
        
        
        errors = Errors(mode=self.mode)

        if (account_type == SLAVE):
            errors.error_criticity = HIGH_C
            if exec_trade_function != 0:
                    
                errors.error_messages = \
                "Strategy {} tried to go in {} but slave {} trade function returned an error. \
                ".format(strategy, side, idx)
            else:
                errors.error_messages = \
                "Strategy {} tried to go in {} but slave {} was not updated successfully. \
                ".format(strategy, side, idx)
                
            return Errors.Errors__SendEmail(errors)

        elif (account_type == MASTER):
            if (ret_update_master != 0):
                errors.error_criticity = HIGH_C
                errors.error_messages = "Master update of strategy {} unsuccessful.".format(strategy)
                Errors.Errors__SendEmail(errors)
            else:
                if (ep_platform_found == False):
                    errors.error_criticity = HIGH_C
                    errors.error_messages = "Echange platform of strategy {} was not found.".format(strategy)
                    Errors.Errors__SendEmail(errors)
                else:
                    if (ret_update_slave == 0):
                        result = SUCCESSFUL
                        errors.error_criticity = INFO_C
                        message = "New position is now : {}".format(side)
                    else:
                        result = UNSUCCESSFUL
                        errors.error_criticity = HIGH_C
                        message = "ret_update_slave = 1"
                        
                    errors.error_messages = \
                        "Update of strategy {} {}.\n{}.\
                        ".format(strategy, result, message)
                        #".format(strategy.strategy_file_path.split('/')[-1][:-len(TXT)], result, message)
                            
                return Errors.Errors__SendEmail(errors)
        else:
            return 1

    def WinySloth__SlaveManagement(self, strategy):
        """
        Name : WinySloth__SlaveManagement(strategy)
    
        Parameters : 
                      strategy : StrategyFile
                        StrategyFile object to manage
    
        Description : This function determines the appropriate function
                      to call to change the slave's side.  
        """
        idx = 1
        ret_update_slave = 1
        update_list = [1]*len(strategy.slave_apis)
        out_mail = 0
        for slave in strategy.slave_apis:
            side_possibilities_dict = {(OUT,LONG):slave.close_long, (OUT,SHORT):slave.close_short, \
                                       (LONG,OUT):slave.open_long, (SHORT,OUT):slave.open_short, \
                                       (LONG,SHORT):slave.open_long_from_short, \
                                       (SHORT,LONG):slave.open_short_from_long}
            
            if (slave.side != strategy.master_api.side):

                slave.leverage = strategy.master_api.leverage
                slave.engaged_balance = strategy.master_api.engaged_balance
                slave.entryPrice = strategy.master_api.entryPrice
                
                exec_trade_function = side_possibilities_dict[strategy.master_api.side, slave.side]()
                if exec_trade_function == 0:
                    ret_update_slave = self.WinySloth__Update(strategy, strategy.master_api.side, idx)
                    update_list[idx - 1] = ret_update_slave
                    if ret_update_slave == 0:
                        ret_update_slave = 1
                    else:
                        out_mail = self.Winy_Sloth__SendEmail(SLAVE, \
                                    strategy.strategy_file_path.split('/')[-1][:-len(TXT)], \
                                    strategy.master_api.side, \
                                    idx=idx)
                else:
                    update_list[idx - 1] = 1

                    self.Winy_Sloth__SendEmail(SLAVE, \
                        strategy.strategy_file_path.split('/')[-1][:-len(TXT)], \
                        strategy.master_api.side, \
                        exec_trade_function=exec_trade_function, idx=idx)      
            else:
                update_list[idx - 1] = 0
            
            idx = idx + 1
            sleep(WAIT_DEFAULT)
        
        for out_slave in update_list:
            if out_slave == 1:
                return 1
        
        return 0
    
    #TODO: Rendre cette fonction générique
    @staticmethod
    def ConfigureStopLoss(client, symbol, account_type, engaged_balance, entryPrice, side, mode=HEDGE, risk=RISK):
        if ((account_type == SPOT)):
            return 0
        elif (abs(engaged_balance) > 1 and ((side == LONG) or (side == SHORT))) or (side == OUT):
            ret = I__MANAGE_STOP_LOSS(client, symbol, abs(engaged_balance), entryPrice, side, mode, risk)
            return ret
        else:
            return 0
    
    """
    def WinySloth__FindExchangePlatform(self, elt):
        return elt.find_exchange_platform_class()
    """
    def WinySloth__SaveTrade(self, strategy, timestamp, symbol, \
                                    side, engaged_balance, price):
        if (self.mode != DEBUG):
            try:
                leverage = engaged_balance
                strategy_name = strategy.strategy_file_path.split('/')[-1][:-len(TXT)]
                if (price == 0):
                    master_ep_obj = strategy.master_api.api_key.exchange_platform_obj
                    price = master_ep_obj.CEP__GET_SYMBOL_PRICE(master_ep_obj.CEP__CLIENT(strategy.master_api.api_key._api_key, \
                                strategy.master_api.api_key._api_secret_key, strategy.master_api.account_contract_type), \
                                strategy.master_api.symbol)
                with open(self.history_file, "a+", encoding=UTF8, newline='') as trade_history_file:
                    data = [[strategy_name, timestamp, symbol, side, leverage, price]]
                    writer = csv.writer(trade_history_file)
                    writer.writerows(data)

                    trade_history_file.close()
                return 0
            except:
                print("An error during the writing of statistics file. \
                {}.\n {} {}".format(self.history_file, sys.exc_info(), \
                traceback.format_exc()))
                return 1
        else: 
            return 0

    def WinySloth__Main(self):
        """
        Name : WinySloth__Main()
    
        Parameters : 
    
        Description : Main function of a Winy_Sloth object. This function is going through each strategy
        in the strategy list. For each strategy, the master's position in the strategy file is compared with
        the master's position given from Binance. In case of difference, the position of each slave is updated
        copying the master's position. If a position changes or if an error occurs, an email is sent.
        """
        for strategy in self.strategies:
            ret_update_master = 1
            ret_update_slave = 1

            master_ep_obj = strategy.master_api.api_key.exchange_platform_obj

            ep_return = master_ep_obj.CEP__GET_ACCOUNT_HISTORY( \
                        master_ep_obj.CEP__CLIENT(strategy.master_api.api_key._api_key, \
                        strategy.master_api.api_key._api_secret_key, strategy.master_api.account_contract_type), \
                        strategy.master_api.account_contract_type, \
                        strategy.master_api.symbol)

            strategy_current_side = master_ep_obj.CEP__COMPUTE_ACCOUNT_SIDE( \
                                        strategy.master_api, ep_return)
            
            #strategy_current_side = WinySloth.WinySloth__ComputeAccountSide(strategy.master_api, ep_return)
            if (strategy_current_side != strategy.master_api.side):
                if (self.mode != DEBUG):
                    print("===\nBinance return = {}\nNew position = {}\n===".format(ep_return, \
                                                strategy_current_side))

                self.WinySloth__SaveTrade(strategy, \
                                        str(int(time.time()*1000)), strategy.master_api.symbol, \
                                        strategy.master_api.side, strategy.master_api.engaged_balance, \
                                        strategy.master_api.markPrice)

                ret_update_master = self.WinySloth__Update(strategy, strategy_current_side)
                
                #GESTION DES SLAVES 
                if (ret_update_master == 0):
                    ret_update_slave = self.WinySloth__SlaveManagement(strategy)
                
                self.Winy_Sloth__SendEmail(MASTER, \
                        strategy.strategy_file_path.split('/')[-1][:-len(TXT)], \
                        strategy.master_api.side, ret_update_master=ret_update_master, \
                        ret_update_slave=ret_update_slave)
                
            else:
                sleep(WAIT_DEFAULT)
                #print("Position up to date\n")
