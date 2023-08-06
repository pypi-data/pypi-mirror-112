'''

Author: Zeng Siwei
Date: 2020-09-16 19:34:45
LastEditors: Zeng Siwei
LastEditTime: 2020-11-03 18:33:01
Description: 

'''

from resource_util import *
from gene_name_id_mapper import GeneNameIDMapper

def get_detection_set(filepath, is_save=True):
    set_gene = set()
    list_id = []
    with open(filepath) as fp:
        for line in fp:
            id = int(line.strip())
            list_id.append(id)
            gene_name = GeneNameIDMapper.get_gene_name(id)
            gene_name = gene_name.split(";")
            for gene in gene_name:
                set_gene.add(gene)

    if is_save:
        with open(filepath + ".gene", "w") as wfp:
            for id in list_id:
                gene_name = GeneNameIDMapper.get_gene_name(id)
                gene_name = gene_name.split(";")
                for gene in gene_name:
                    if len (gene) > 0:
                        wfp.write(str(id) + "\t" + gene + "\n")
                        break
    return set_gene

if __name__ == '__main__':
    set_gene = set()

    # for i in range(10):
    filepath = "/Users/endlesslethe/PycharmProjects/gene-network-builder/data/spp2.txt"
    set_gene = set_gene & get_detection_set(filepath)

    # filepath = DIR_INPUT + "g3.txt"
    # set_gene = set_gene & get_detection_set(filepath)

    # filepath = DIR_INPUT + "stage1_outliers_image0_0.025.txt"
    # set_gene = set_gene & get_detection_set(filepath)

    # filepath = DIR_INPUT + "stage1_outliers_image1_-0.03.txt"
    # set_gene = set_gene & get_detection_set(filepath)

    # filepath = DIR_INPUT + "/fraudar0/my_fraudar_model.rows"
    # set_gene = set_gene & get_detection_set(filepath)
    #
    # filepath = DIR_INPUT + "/fraudar1/my_fraudar_model.rows"
    # set_gene = set_gene & get_detection_set(filepath)

    # filepath = DIR_INPUT + "/holoscope0/my_holoscope_model.blk1.levelcols"
    # set_gene = set_gene & get_detection_set(filepath)

    # filepath = DIR_INPUT + "/holoscope0/my_holoscope_model.blk2.rows"
    # set_gene = set_gene & get_detection_set(filepath)
    #
    # filepath = DIR_INPUT + "/holoscope0/my_holoscope_model.blk3.rows"
    # set_gene = set_gene & get_detection_set(filepath)
    #
    # filepath = DIR_INPUT + "/holoscope1/my_holoscope_model.blk1.levelcols"
    # set_gene = set_gene & get_detection_set(filepath)
    #
    # filepath = DIR_INPUT + "/holoscope1/my_holoscope_model.blk2.rows"
    # set_gene = set_gene & get_detection_set(filepath)
    #
    # filepath = DIR_INPUT + "/holoscope1/my_holoscope_model.blk3.rows"
    # set_gene = set_gene & get_detection_set(filepath)
    #
    # filepath = DIR_INPUT + "eigen0.txt"
    # set_gene = set_gene & get_detection_set(filepath)
    #
    # filepath = DIR_INPUT + "eigen1.txt"
    # set_gene = set_gene & get_detection_set(filepath)

    # print(len(set_gene))
    # with open(DIR_OUTPUT + "gene.out", "w") as wfp:
    #     for gene in set_gene:
    #         wfp.write(gene + "\n")
