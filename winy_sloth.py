import os
import subprocess
from constants import *
from strategy_file import *

class WinySloth:
    def __init__(self, strategies_folder_path):
        self.strategies_folder_path = strategies_folder_path
        self.strategies_nb = self.WinySloth__FindNbStrategies()
        self.strategies = []
        init_return = self.WinySloth__Init()
        if (init_return):
            #send mail
            sys.exit()
        else:
            self.WinySloth__Main()

    def WinySloth__FindNbStrategies(self):
        shell_command = subprocess.run("ls " + self.strategies_folder_path + " | wc -l", shell=True, capture_output=True)
        number_files = shell_command.stdout.decode("utf-8").rstrip('\n')
        return number_files
    
    def WinySloth__FindAllStrategiesFiles(self):
        return (os.listdir(self.strategies_folder_path))
    
    def WinySloth__Init(self):
        try:
            strategies_files_list = self.WinySloth__FindAllStrategiesFiles()

            for strategy in strategies_files_list:
                strategy_path = self.strategies_folder_path + strategy
                print(strategy_path)
                
                with open(strategy_path, "r") as strategy_file:
                    content = strategy_file.readlines()
                    master_info = content[0].strip('\n').split(" ")
                    slave_info = content[2:]
                    strategy_file_object = StrategyFile(strategy_path, master_info, slave_info)
                    self.strategies.append(strategy_file_object)
                    print(master_info)
                    
                    strategy_file.close()
            return 0
        except:
            return 1
    def WinySloth__ComputeAccountSide(self, account_type, binance_response):
        if (isinstance(binance_response, int)):
            return 1
        else:
            if (account_type == SPOT):
                binance_response = binance_response[0]
                if binance_response[SIDE] == BUY: 
                    return LONG
                elif binance_response[SIDE] == SELL:
                    return OUT
                else:
                    return 1
            elif (account_type == FUTURES):
                if (len(binance_response) > 1):
                    entry_price_1 = binance_response[0][ENTRY_PRICE] 
                    entry_price_2 = binance_response[1][ENTRY_PRICE]
                    entry_price_3 = binance_response[2][ENTRY_PRICE]
                    if (entry_price_1 != float(0)) or (entry_price_2 != float(0)):
                        return LONG
                    elif (entry_price_1 == float(0) and entry_price_2 == float(0) and entry_price_3 == float(0)):
                        return OUT
                    elif (entry_price_3 != float(0)):
                        return SHORT
                    else:
                        return 1
                else:
                    pos_amt = float(binance_response[0][POSITION_AMT])
                    if (pos_amt == float(0)):
                        return OUT
                    elif (pos_amt < 0):
                        return SHORT
                    elif (pos_amt > 0):
                        return LONG
                    else: 
                        return 1
            else:
                return 1

    def WinySloth__UpdateStrategyFile(self, strategy_file_path, strategy_current_side):
        try :
            with open(strategy_file_path, 'r') as strategy_file:
                info = strategy_file.readlines()
                strategy_file.close()

            with open(strategy_file_path, "w") as strategy_file:
                master_info = info[0]
                master_info = master_info.strip('\n').split(" ")
                master_info[2] = strategy_current_side
                info[0] = master_info
                info[0] = " ".join(info[0]) + '\n'
                strategy_file.writelines(info)   
                strategy_file.close()
            return 0
        except:
            return 1
    
    def WinySloth__UpdatePositionSide(self, strategy, strategy_current_side):
        try:
            with open(strategy.strategy_file_path, "r") as strategy_file:
                content = strategy_file.readlines()
                master_info = content[0].strip('\n').split(" ")
                master_info_side = master_info[2]
                if (master_info_side == strategy_current_side):
                    strategy.master_api.side = master_info_side
                    return 0
                else:
                    return 1
                strategy_file.close()
        except:
            return 1

    def WinySloth__Update(self, strategy, strategy_current_side):
        """
        1 - Ecriture dans le fichier de strategy
        2 - Relecture du fichier pour MAJ de l'attribut master-api
        """
        update_file = 1
        update_object = 1

        update_file = self.WinySloth__UpdateStrategyFile(strategy.strategy_file_path, strategy_current_side)
        update_object = self.WinySloth__UpdatePositionSide(strategy, strategy_current_side)

        if (update_file == 1 or update_object == 1):
            return 1
        else:
            return 0


    def WinySloth__Main(self):
        for strategy in self.strategies:
            ret_update = 1
            binance_return = I__GET_ACCOUNT_HISTORY(Client(strategy.master_api.api_key, \
                                                    strategy.master_api.api_secret_key), \
                                                    strategy.master_api.account_type, strategy.master_api.symbol)
            print(binance_return)
            strategy_current_side = self.WinySloth__ComputeAccountSide(strategy.master_api.account_type, binance_return)
            if (strategy_current_side != strategy.master_api.side):
                print("Position not up to date")
                ret_update = self.WinySloth__Update(strategy, strategy_current_side)

            else:
                print("Position up to date")
        a = 0
            