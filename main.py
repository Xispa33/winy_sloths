#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
from winy_sloth import *

if __name__ == "__main__":
    """
    Main function
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, choices=["test", "release"], help="winy_sloths execution mode")
    parser.add_argument("-e", "--emails", type=str, choices=["yes", "no", "y", "n"], help="notify changes by email", default="no")
    args = parser.parse_args()
    parser.parse_args()
    """
    main_obj = WinySloth(STRATEGIES_FOLDER)