import os
import subprocess
from constants import *
from strategy_file import *

class WinySloth:
    def __init__(self, strategies_folder_path):
        self.strategies_folder_path = strategies_folder_path
        self.strategies_nb = self.WinySloth__FindNbStrategies()
        self.strategies = []
        self.WinySloth__Init()

    def WinySloth__FindNbStrategies(self):
        shell_command = subprocess.run("ls " + self.strategies_folder_path + " | wc -l", shell=True, capture_output=True)
        number_files = shell_command.stdout.decode("utf-8").rstrip('\n')
        return number_files
    
    def WinySloth__FindAllStrategiesFiles(self):
        return (os.listdir(self.strategies_folder_path))
    
    def WinySloth__Init(self):
        strategies_files_list = self.WinySloth__FindAllStrategiesFiles()

        for strategy in strategies_files_list:
            strategy_path = self.strategies_folder_path + strategy
            print(strategy_path)
            
            with open(strategy_path) as strategy_file:
                content = strategy_file.readlines()
                master_info = content[0].strip('\n').split(" ")
                slave_info = content[2:]
                strategy_file_object = StrategyFile(strategy_path, master_info, slave_info)
                self.strategies.append(strategy_file_object)
                print(master_info)
                
                strategy_file.close()
    