#!/usr/bin/python3
# -*- coding: utf-8 -*-

from client_file import *

if __name__ == "__main__":
    """
    Main function
    """
    tree = ClientFile("history.txt")
    print(tree)

    for i in range(0,10):
        run(tree)
    #while (1):
    #    a = 0
    #    run(tree)