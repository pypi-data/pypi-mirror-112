from gensim import similarities
import os, logging
import numpy as np

class NeighborSampler():
    def __init__(self, chip_name, stage, x_data=None):
        self.index = None
        self.chip_name = chip_name
        self.stage = stage
        self.build(x_data)

    def build(self, x_data=np.array([])):
        corpus = []
        for i in range(x_data.shape[0]):
            gensim_format_vec = []
            for j in range(x_data.shape[1]):
                gensim_format_vec.append((j, x_data[i][j]))
            corpus.append(gensim_format_vec)
        logging.info("#sample to build index: %s" % x_data.shape[0])
        self.get_index(corpus,x_data.shape[1])


    def get_index(self, corpus=None, n_feature=None):
        filepath_index = "./output/%s_%s_neighbor.index" % (self.chip_name, self.stage)
        filepath_temp = "./temp/%s_%s_neighbor.index.tmp" % (self.chip_name, self.stage)

        if not self.index:
            if os.path.exists(filepath_index):
                self.index = similarities.Similarity.load(filepath_index)
            else:
                self.index = similarities.Similarity(filepath_temp, corpus, num_features=n_feature)
                self.index.save(filepath_index)
        return self.index

    def get_topk(self, vec, k, reverse=False):
        gensim_format_vec = []
        for i in range(len(vec)):
            gensim_format_vec.append((i, vec[i]))
        sims = self.index[gensim_format_vec]

        # 按相似度降序排序
        if reverse:
            sim_sort = sorted(list(enumerate(sims)), key=lambda item: item[1], reverse=False)
        else :
            sim_sort = sorted(list(enumerate(sims)), key=lambda item: item[1], reverse=True)
        top_k = sim_sort[0:k]
        return top_k