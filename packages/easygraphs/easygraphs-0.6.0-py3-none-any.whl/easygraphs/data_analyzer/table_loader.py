'''

Author: Zeng Siwei
Date: 2020-10-16 10:16:54
LastEditors: Zeng Siwei
LastEditTime: 2021-04-21 15:11:33
Description: 

'''

import os
import logging
import abc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.utils import get_abspath

class TableLoader():
    """
    Load one or several static networks and run tasks like analyzing.
    """

    def __init__(self, table_name, header = "infer", sep = "\t"):
        self.dir_input = "../input/"
        self.table_name = table_name

        filepath = get_abspath(self.dir_input + table_name)
        if not os.path.exists(filepath):
            filepath = filepath + ".txt"
        self.data = pd.read_csv(filepath, header = header, sep = sep)
        logging.info("Table Loaded.")
