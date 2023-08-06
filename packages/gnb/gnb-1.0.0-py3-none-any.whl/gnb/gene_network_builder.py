import pandas as pd
import numpy as np
import logging, os
from gene_dataloader import *
from gene_name_id_mapper import *
from patient_stage_mapper import Meth300PlusStageMapper, Meth300StageMapper
from neighbor_sampler import *

logging.getLogger("smart_open").setLevel(logging.WARNING)
logging.getLogger("gensim").setLevel(logging.WARNING)

class GeneNetworkBuilder():
    @classmethod
    def build_coexpression_matrix(cls, stage_mapper):
        """
        To build a co-expression matrix,
        1. load data
        2. divide whole sample set by several stages, build gene x patient matrix
        3. in each stage, compute matrix

        Here we provide two way to build matrix:
        1. build full matrix (#node is no more than 50k)
        2. build matrix by neighbor sample
        """

        # cls.build_full_coexpression_matrix(stage_mapper)
        cls.build_sampled_coexpression_matrix(stage_mapper)

        logging.info("Co-expression matrix save process finishs.\n")
        return

    @classmethod
    def build_full_coexpression_matrix(cls, stage_mapper):
        ## load data
        ## each line is patient's all probe data (or you can merge some cols)
        dict_line_number_data = GeneDataloader.get_gene_data_dict()
        list_x_data = []
        list_valid_stage = []
        for t in stage_mapper.sorted_keys():
            list_line_number = stage_mapper.get_get_patient_line_number_by_stage(t)
            if not list_line_number:
                continue
            list_stage_data = [dict_line_number_data[x] for x in list_line_number]
            x_data = np.array(list_stage_data)
            list_x_data.append(x_data.T)
            list_valid_stage.append(t)

        ## build numpy matrix by stage
        ## for each stage, a n_col x n_col matrix will be built.
        logging.info("Co-expression matrix save process starts.")
        for t in range(len(list_valid_stage)):
            now_stage = list_valid_stage[t]
            with open(DIR_OUTPUT + "matrix_" + str(now_stage) + ".txt", "w") as f:
                logging.info("Now processing stage " + str(t))
                for i in range(GeneDataloader.n_gene):
                    for j in range(GeneDataloader.n_gene):
                        if (i < j):
                            X = list_x_data[t][i]
                            Y = list_x_data[t][j]
                            f.write(str(cls.pearson(X, Y)))
                        if (j != GeneDataloader.n_gene-1):
                            f.write("\t")
                        else :
                            f.write("\n")
                    f.flush()
                    os.fsync(f.fileno())

    @classmethod
    def build_sampled_coexpression_matrix(cls, stage_mapper, k = 2000):
        dict_line_number_data = GeneDataloader.get_gene_data_dict()
        logging.info("Co-expression matrix building process starts.")
        for t in stage_mapper.sorted_keys():
            logging.info("processing stage %s" % (t) )
            ## load data
            list_line_number = stage_mapper.get_get_patient_line_number_by_stage(t)
            if not list_line_number:
                continue
            list_stage_data = [dict_line_number_data[x] for x in list_line_number]
            x_data = np.array(list_stage_data).T
            logging.info("data shape: %s %s" % (x_data.shape[0], x_data.shape[1]))

            # build numpy matrix by stage
            now_stage = t
            neighbor_sampler = NeighborSampler("Meth300", t, x_data)
            with open(DIR_OUTPUT + "matrix_" + str(now_stage) + ".txt", "w") as f:
                logging.info("Now processing stage " + str(t))
                for i in range(GeneDataloader.n_gene):
                    list_neighbor = neighbor_sampler.get_topk(x_data[i], k)
                    list_neighbor.extend(neighbor_sampler.get_topk(x_data[i], k, True))
                    list_neighbor = list(set(list_neighbor))
                    logging.info("sample %s's topk neighbor: %s" % (i, list_neighbor))
                    for j, value in list_neighbor:
                        f.write("%s\t%s\t%s\n" % (i, j, value))
                    f.flush()
                    os.fsync(f.fileno())

    @classmethod
    def pearson(cls, X, Y):
        """
        given two random variable X and Y, compute their pearon coffient
        Args:
            x : numpy array, shape (n_feature, )
            y : numpy array, shape (n_feature, )
        Returns:
            pearson corrcoef of X and Y
        """
        return np.corrcoef(X, Y)[0][1]


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    if not os.path.exists("./output"):
        os.makedirs("./output")
    GeneNetworkBuilder.build_coexpression_matrix(Meth300PlusStageMapper)
    # print(GeneNetworkBuilder.pearson(np.array([1, 2, 3]), np.array([-1, -7, -9])))