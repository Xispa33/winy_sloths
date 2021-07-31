#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import os
import subprocess
from time import *
from datetime import *
from constants import *
from strategy_file import *
from interface_binance import *
from errors import *
import traceback
import argparse
import time

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
    def __init__(self):
        (self.mode, self.strategies_folder_path) = self.WinySloth__ReadArguments()
        self.strategies_nb = self.WinySloth__FindNbStrategies()
        self.strategies = []
        init_return = self.WinySloth__Init()
        if (init_return):
            print("Init was not good.\n")
            sys.exit()
        else:
            if (self.mode == RUN):
                print("Init was good.\n")
                print("There are {} strategies running.\n".format(len(self.strategies)))
                while (1):
                    try:
                        self.WinySloth__Main()
                    except:
                        print("An error occured. An email should have been sent around {}\n".format(str(datetime.now())))
                        print(sys.exc_info())
                        print(traceback.format_exc())
                        with open("errors.txt", "a") as error_file:
                            errors = Errors()
                            errors.err_criticity = HIGH_C
                            error_file.write(Errors.Errors__GetRawExceptionInfo(sys.exc_info()))
                            error_file.write('\n')
                            Errors.Errors__SendEmail(errors)
                            error_file.close()
                        sleep(2)
                        self.strategies = []
                        self.__init__()
            elif (self.mode == DEBUG):
                print("There are {} strategies running.\n".format(len(self.strategies)))
                
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

        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mode", type=str, choices=['d', DEBUG, RUN], default='run', help="Mode of Execution")
        parser.add_argument("-f", "--folder", type=str, default='strategies', help="Path of the folder containing strategy files")
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
        
        return (mode, strat_folder_path)
    
    def WinySloth__FindNbStrategies(self):
        """
        Name : WinySloth__FindNbStrategies()
    
        Parameters : 
    
        Description : Function that returns the number of strategies of a
                      WinySloth object. 
        """
        if (self.strategies_folder_path != ERROR_STRATEGY_PATH_FOLDER):
            shell_command = subprocess.run("ls " + self.strategies_folder_path + " | wc -l", shell=True, capture_output=True)
            number_files = shell_command.stdout.decode("utf-8").rstrip('\n')
            return number_files
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
            if (_file[-4:] == ".txt"):
                out_list.append(_file)
        return (out_list)
    
    def WinySloth__Init(self):
        """
        Name : WinySloth__Init()
    
        Parameters : 
    
        Description : Initialisation of a WinySloth object
        """
        if ((self.strategies_nb != -1) and (self.mode != ERROR_MODE)):
            try:
                strategies_files_list = self.WinySloth__FindAllStrategiesFiles()

                for strategy in strategies_files_list:
                    strategy_path = self.strategies_folder_path + '/' + strategy
                    
                    with open(strategy_path, "r") as strategy_file:
                        content = strategy_file.readlines()
                        master_info = content[0].strip('\n').split(" ")
                        slave_info = content[2:]
                        strategy_file_object = StrategyFile(strategy_path, master_info, slave_info)
                        self.strategies.append(strategy_file_object)
                        strategy_file.close()
                return 0
            except:
                print("An error during the reading of the file occured here line 111. 1\n")
                print(sys.exc_info())
                print(traceback.format_exc())
                return 1
        else:
            return 1
    
    @staticmethod
    def WinySloth__ComputeAccountSide(master_api, binance_response):
        """
        Name : WinySloth__ComputeAccountSide(master_api, binance_response)
    
        Parameters : 
                      master_api : ApiKey
                        Api key of the account 

                      binance_response : list
                        list returned by Binance after asking the account's
                        history
    
        Description : Function that computes the side of a Binance account
        """
        if (isinstance(binance_response, int)):
            print("Binance return was crap ! \n")
            return master_api.side
            #return 1
        else:
            if (master_api.account_type == SPOT):
                if (len(binance_response) == 0):
                    return master_api.side
                else:
                    asset_dict = I__GET_ASSET_BALANCE(I__CLIENT(master_api.api_key, master_api.api_secret_key))
                
                    if (not isinstance(asset_dict, dict)):
                        return master_api.side
                    else:
                        binance_response = binance_response[0]
                        asset_usdt=float(asset_dict[FREE])

                        if binance_response[SIDE] == BUY and round(float(asset_usdt),1) < MIN_WALLET_IN_USDT: 
                            return LONG
                        elif binance_response[SIDE] == SELL and round(float(asset_usdt),1) > MIN_WALLET_IN_USDT:
                            return OUT
                        else:
                            return master_api.side
                    
            elif (master_api.account_type == FUTURES):
                if (len(binance_response) > 1):
                    master_api.account_mode = HEDGE
                    for dic in binance_response:
                        if dic[POSITION_SIDE] == BOTH:
                            both_list = dic
                        elif dic[POSITION_SIDE] == LONG:
                            long_list = dic
                        else:
                            short_list = dic
                    
                    entry_price_both = float(both_list[ENTRY_PRICE])
                    entry_price_long = float(long_list[ENTRY_PRICE])
                    entry_price_short = float(short_list[ENTRY_PRICE])

                    if (entry_price_both != float(0)) or (entry_price_long != float(0)):
                        master_api.markPrice = round(float(long_list[MARK_PRICE]), 0)
                        master_api.entryPrice = round(float(long_list[ENTRY_PRICE]), 0)
                        master_api.leverage = long_list[LEVERAGE]
                        master_api.positionAmt = float(long_list[POSITION_AMT])
                        master_api.balance = float(I__GET_FUTURES_ACCOUNT_BALANCE(I__CLIENT(master_api.api_key, master_api.api_secret_key))[BALANCE])
                        ret = master_api.computeEngagedBalance(157, binance_response)
                        if ret == 1:
                            return OUT
                        else:
                            return LONG
                    elif (entry_price_both == float(0) and entry_price_long == float(0) and entry_price_short == float(0)):
                        return OUT
                    elif (entry_price_short != float(0)):
                        master_api.markPrice = round(float(short_list[MARK_PRICE]), 0)
                        master_api.entryPrice = round(float(short_list[ENTRY_PRICE]), 0)
                        master_api.leverage = short_list[LEVERAGE]
                        master_api.positionAmt = float(short_list[POSITION_AMT])
                        master_api.balance = float(I__GET_FUTURES_ACCOUNT_BALANCE(I__CLIENT(master_api.api_key, master_api.api_secret_key))[BALANCE])
                        ret = master_api.computeEngagedBalance(167, binance_response)
                        if ret == 1:
                            return OUT
                        else:
                            return SHORT
                    else:
                        #return 1
                        return master_api.side
                else:
                    # Store needed information for FUTURES account
                    master_api.account_mode = ONE_WAY
                    master_api.markPrice = round(float(binance_response[0][MARK_PRICE]), 0)
                    master_api.entryPrice = round(float(binance_response[0][ENTRY_PRICE]), 0)
                    master_api.leverage = binance_response[0][LEVERAGE]
                    master_api.positionAmt = float(binance_response[0][POSITION_AMT])
                    #TODO: A modifier pour grer les cas derreur
                    bin_ret = I__GET_FUTURES_ACCOUNT_BALANCE(I__CLIENT(master_api.api_key, master_api.api_secret_key))
                    if (isinstance(bin_ret, int)):
                        return master_api.side
                    else:
                        master_api.balance = float(bin_ret[BALANCE])
                    
                    #master_api.balance = float(I__GET_FUTURES_ACCOUNT_BALANCE(I__CLIENT(master_api.api_key, master_api.api_secret_key))[BALANCE])
                    ret = master_api.computeEngagedBalance(179, binance_response)
                    
                    if (master_api.positionAmt == float(0) or ret == 1):
                        return OUT
                    elif (master_api.positionAmt < 0):
                        return SHORT
                    elif (master_api.positionAmt > 0):
                        return LONG
                    else: 
                        #return 1
                        return master_api.side
            else:
                #return 1
                return master_api.side

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
                master_info[2] = strategy_current_side
                info[idx] = master_info
                info[idx] = " ".join(info[idx]) + '\n'
                strategy_file.writelines(info)
                strategy_file.close()
            return 0
        except:
            print("An error during the reading of the file occured here line 230. 1\n")
            print(sys.exc_info())
            print(traceback.format_exc())
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
            print("An error during the reading of the file occured here line 270. 1\n")
            print(sys.exc_info())
            print(traceback.format_exc())
            return 1

    def WinySloth__UpdateMaster(self, strategy, strategy_current_side):
        """
        Name : WinySloth__UpdateMaster(strategy, strategy_current_side)
    
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
                      strategy : StrategyFile
                        StrategyFile object to be updated
                    
                      strategy_current_side : str
                        New side of the strategy for the slave
    
        Description : Function that updates all needed information for a 
                      slave
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
                      strategy : StrategyFile
                        StrategyFile object to manage
    
        Description : This function determines the appropriate function
                      to call to change the slave's side.  
        """
        idx = 1
        ret_update_slave = 1
        update_list = [1]*len(strategy.slave_apis)
        ret_stop_loss_slave = 1
        update_list_stop_loss = [1]*len(strategy.slave_apis)
        for slave in strategy.slave_apis:
            side_possibilities_dict = {(OUT,LONG):slave.close_long, (OUT,SHORT):slave.close_short, \
                                       (LONG,OUT):slave.open_long, (SHORT,OUT):slave.open_short, \
                                       (LONG,SHORT):slave.open_long_from_short, (SHORT,LONG):slave.open_short_from_long}
            
            if (slave.side != strategy.master_api.side):
                exec_trade_function = side_possibilities_dict[strategy.master_api.side, slave.side](strategy.master_api)
                if exec_trade_function == 0:
                    ret_update_slave = self.WinySloth__UpdateSlave(strategy, strategy.master_api.side, idx)
                    if ret_update_slave == 0:
                        ret_update_slave = 1
                        update_list[idx - 1] = 0
                        
                    else:
                        update_list[idx - 1] = 1
                        if (self.mode != DEBUG):
                            errors = Errors()
                            errors.err_criticity = HIGH_C
                            errors.error_messages = "Slave {} of strategy {} was not updated successfully".format(idx, strategy.strategy_file_path)
                            Errors.Errors__SendEmail(errors)
                        
                else:
                    update_list[idx - 1] = 1
                    if (self.mode != DEBUG):
                        #send mail
                        errors = Errors()
                        errors.err_criticity = HIGH_C
                        errors.error_messages = "Trade function returned an error for slave {} of strategy {}".format(idx, strategy.strategy_file_path)
                        Errors.Errors__SendEmail(errors)
                        
            else:
                update_list[idx - 1] = 0
            
            idx = idx + 1
            sleep(1)
        
        for out_slave in update_list:
            if out_slave == 1:
                return 1
        
        return 0
    
    @staticmethod
    def ConfigureStopLoss(client, symbol, account_type, engaged_balance, entryPrice, side, mode=HEDGE, risk=RISK):
        if ((account_type == SPOT)):
            return 0
        elif (abs(engaged_balance) > 1 and ((side == LONG) or (side == SHORT))) or (side == OUT):
            ret = I__MANAGE_STOP_LOSS(client, symbol, abs(engaged_balance), entryPrice, side, mode, risk)
            return ret
        else:
            return 0
    
    def WinySloth__Main(self, timeout=0):
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
            binance_return = I__GET_ACCOUNT_HISTORY(I__CLIENT(strategy.master_api.api_key, \
                                                    strategy.master_api.api_secret_key), \
                                                    strategy.master_api.account_type, strategy.master_api.symbol)
            #print(binance_return)
            strategy_current_side = WinySloth.WinySloth__ComputeAccountSide(strategy.master_api, binance_return)
            if (strategy_current_side != strategy.master_api.side):
                #print("Position not up to date")
                if (self.mode != DEBUG):
                    print("Binance return = ")
                    print(binance_return)
                    print("New position computed = ")
                    print(strategy_current_side)

                ret_update_master = self.WinySloth__UpdateMaster(strategy, strategy_current_side)
                
                #GESTION DES SLAVES 
                if (ret_update_master == 0):
                    ret_update_slave = self.WinySloth__SlaveManagement(strategy)
                    if (ret_update_slave == 0):
                        if (self.mode != DEBUG):
                            #sendemail
                            errors = Errors()
                            errors.err_criticity = INFO_C
                            errors.error_messages = "Master + Slave update successful of strategy : {}".format(strategy.strategy_file_path)
                            Errors.Errors__SendEmail(errors)
                    else:
                        if (self.mode != DEBUG):
                            #sendemail
                            errors = Errors()
                            errors.err_criticity = HIGH_C
                            errors.error_messages = "Slave update unsuccessful of strategy : {}".format(strategy.strategy_file_path)
                            Errors.Errors__SendEmail(errors)
                            sys.exit()
                else:
                    if (self.mode != DEBUG):
                        #sendemail
                        errors = Errors()
                        errors.err_criticity = HIGH_C
                        errors.error_messages = "Master update unsuccessful of strategy : {}".format(strategy.strategy_file_path)
                        Errors.Errors__SendEmail(errors)
                        sys.exit()

            else:
                sleep(1)
                #print("Position up to date\n")

