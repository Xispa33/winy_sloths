#!/usr/bin/python3
# -*- coding: utf-8 -*-

from winy_sloth import *

if __name__ == "__main__":
    
    """
    Init
    1 - On va dans STRATEGIES dossier, et on compte le nombre de fichier .txt
    2 - Pour chaque fichier .txt, on créé un objet de type StrategyFile
    3 - On stocke chacun des StrategyFile dans une liste
    """
    a = WinySloth(STRATEGIES_FOLDER)