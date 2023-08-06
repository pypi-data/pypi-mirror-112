import pandas as pd
import numpy as np
import logging
from resource_util import *
from collections import defaultdict
import gc

class GeneDataloader():
    _dict_line_number_data = None
    n_patient = None
    n_gene = None

    @classmethod
    def get_gene_data_dict(cls):
        """
        define you own dataloader
        """
        if not cls._dict_line_number_data:
            cls._dict_line_number_data, cls.n_patient, cls.n_gene = cls.get_dict_line_number_data()
        return cls._dict_line_number_data

    @classmethod
    def get_dict_line_number_data(cls):
        """
        User use line number and gene name for further analyzing.

        If needed, add code in GeneNameIDMapper for mapping probe data from the same gene into one vector
        1. build two dicts :
            dict[col_index] = reorder_gene_index
            dict[reorder_gene_index] = gene_name
        2. sum probes into one gene (no need normalizing)
            for lines:
                for cols:
                    x_data[dict[col_index]] += col
        """
        dict_line_number_data = defaultdict(list)
        line_number = 0
        dim_data = 0
        with open(FILEPATH_CHIP) as fp:
            next(fp) # skip header
            for line in fp:
                data = line.split("\t")[1:]
                if dim_data and dim_data != len(data):
                    raise Exception("data dim not match")
                for i in range(len(data)):
                    dict_line_number_data[line_number].append(float(data[i]))
                if not dim_data:
                    dim_data = len(dict_line_number_data[line_number])
                line_number += 1
                del data
                gc.collect() # the line has more than 800K element

        if dict_line_number_data:
            logging.info("loading data: %s, %s" % (line_number, dim_data))
        else :
            error_info = "loading data failed. No data error."
            logging.exception(error_info)
            raise Exception(error_info)
        return dict_line_number_data, line_number, dim_data
