#!/usr/bin/python3
# -*- coding: utf-8 -*-

from client_file import *
from constants import *

if __name__ == "__main__":
    """
    Main function
    """
    tree = ClientFile(TREE_FILE)
    run(tree)
    """
    while (1):
        run(tree)
    """