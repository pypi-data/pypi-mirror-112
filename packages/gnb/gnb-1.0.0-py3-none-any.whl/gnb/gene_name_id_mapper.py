import pandas as pd
from resource_util import *
import logging

class GeneNameIDMapper():
    """
    Here ID denotes the col/line number that probe is in.
    And probe name is invisible for users.

    Define your own _get_dict_probe_gene_v1() and _get_dict_line_number_probe_v1() function

    """
    dict_probe_gene = None
    dict_id_probe = None
    _dict_id_probe_reverse = None
    n_dict_probe_gene = 0
    n_dict_id_probe = 0

    @classmethod
    def init_dict(cls):
        if not cls.dict_probe_gene:
            cls._get_dict_probe_gene_v1()

        if cls.dict_probe_gene:
            logging.info("size of dict_probe_gene: %s" % cls.n_dict_probe_gene)
        else:
            error_info = "loading failed. No data error."
            logging.exception(error_info)
            raise Exception(error_info)

        if not cls.dict_id_probe:
            cls._get_dict_id_probe_v1()

        if cls.dict_id_probe:
            logging.info("size of n_dict_id_probe: %s" % cls.n_dict_id_probe)
        else:
            error_info = "loading failed. No data error."
            logging.exception(error_info)
            raise Exception(error_info)

    @classmethod
    def get_gene_name(cls, id, default_str=None):
        """
        Define your own _get_dict_probe_gene() and _get_dict_line_number_probe() function
        """
        cls.init_dict()
        
        probe = cls.dict_id_probe.get(id, "")
        if default_str == "probe":
            gene = cls.dict_probe_gene.get(probe, probe)
        else:
            gene = cls.dict_probe_gene.get(probe, "")
        return gene

    @classmethod
    def get_id(cls, name):
        cls.init_dict()
        if cls._dict_id_probe_reverse is None:
            cls._dict_id_probe_reverse = dict(zip(cls.dict_id_probe.values(), cls.dict_id_probe.keys()))
        list_probes = []
        for key, value in cls.dict_probe_gene.items():
            if name in value:
                list_probes.append(key)
        list_id = []
        for probe in list_probes:
            id = cls._dict_id_probe_reverse.get(probe, None)
            if id is not None:
                list_id.append(id)
        return list_id

    @classmethod
    def _get_dict_probe_gene_v1(cls):
        """
        Loading gene info from chip annotation.

        dict_probe_gene[probe_name] = list(gene_names)
        """
        dict_probe_gene = cls.load_dict("probe_gene")
        if dict_probe_gene is None:
            dict_probe_gene = dict()
            cnt = 0
            with open(FILEPATH_ANNOTION) as fp:
                next(fp)
                for line in fp:
                    tokens = line.strip().split(",")
                    dict_probe_gene[tokens[0]] = tokens[3]
                    cnt += 1
            cls.save_dict(dict_probe_gene, "probe_gene")
        cls.dict_probe_gene = dict_probe_gene
        cls.n_dict_probe_gene = len(dict_probe_gene)

    @classmethod
    def _get_dict_id_probe_v1(cls):
        """
        User use line number and gene name for further analyzing.
        """
        dict_id_probe = cls.load_dict("id_probe")
        if dict_id_probe is None:
            dict_id_probe = dict()
            id = 0
            with open(FILEPATH_CHIP) as fp:
                for line in fp:
                    probe_names = line.strip().split("\t")[1:]
                    for probe_name in probe_names:
                        dict_id_probe[id] = probe_name
                        id += 1
                    break
            cls.save_dict(dict_probe_gene, "id_probe")

        cls.dict_id_probe = dict_id_probe
        cls.n_dict_id_probe = len(cls.dict_id_probe)

    @classmethod
    def save_dict(cls, d, dict_name):
        filepath = DIR_OUTPUT + NET_NAME + "_" + dict_name + ".dict"
        
        with open(filepath, "w") as wfp:
            for key, value in d.items():
                wfp.write(str(key) + "\t" + str(value) + "\n")

    @classmethod
    def load_dict(cls, dict_name):
        import os
        filepath = DIR_OUTPUT + NET_NAME + "_" + dict_name + ".dict"
        if not os.path.exists(filepath):
            print("dict not exists:", filepath)
            return None

        d = dict()
        with open(filepath) as fp:
            for line in fp:
                tokens = line.strip().split("\t")
                if len(tokens) < 2:
                    continue
                try:
                    key = int(tokens[0])
                except Exception as e:
                    key = tokens[0]
                value = tokens[1]
                d[key] = value
        return d


    @classmethod
    def  _get_dict_probe_id_gene_id(cls):
        """
        If needed, add code here for mapping probe data from the same gene into one vector

        Maybe extra files need adding to show how to mapping.
        """
        if dict_gene_id is None:
            dict_gene_id = dict()
            dict_probe_id_gene_id = dict()
            genes = cls.dict_probe_gene.values()
            cnt = 0
            for gene in genes:
                dict_gene_id[gene] = cnt
                cnt += 1
            probe_ids = cls.dict_id_probe.keys()
            for probe_id in probe_ids:
                dict_probe_id_gene_id[probe_id] = dict_gene_id[cls.get_gene_name(probe_id)]


        cls.dict_gene_id = dict_gene_id
        cls.dict_probe_id_gene_id = dict_probe_id_gene_id


if __name__ == '__main__':
    print(GeneNameIDMapper.get_id("ANXA2"))
    print(GeneNameIDMapper.get_gene_name(481901))