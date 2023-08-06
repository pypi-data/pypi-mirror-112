import pandas
from collections import defaultdict
from resource_util import *


class PatientStageMapper(object):
    dict_patient_list = None

    @classmethod
    def get_get_patient_line_number_by_stage(cls, stage):
        cls.get_dict() # init dict
        return cls.dict_patient_list[stage]

    @classmethod
    def get_dict(cls):
        """
            define your own mapper

        1. load patient stage info from FILEPATH_PATIENT_INFO
        2. build map_stage_patient_name to store patient name
        3. loading data matrix from FILEPATH_CHIP
        4. build map_stage_line_number to divide data by stage
        """
        if not cls.dict_patient_list:
            cls.dict_patient_list = cls.get_dict_stage_line_number()
        return cls.dict_patient_list

    @classmethod
    def sorted_keys(cls):
        cls.get_dict() # init dict
        return sorted(cls.dict_patient_list.keys())

    @classmethod
    def get_dict_stage_line_number(cls):
        raise NotImplementedError("Define your own stage to line_number mapper")

class Meth300StageMapper(PatientStageMapper):
    @classmethod
    def get_dict_stage_line_number(cls):
        dict_stage_name = dict([("1", 1), ("2", 2), ("3", 3)])
        # dict_stage_name = dict([("Ia", 1), ("Ib", 2), ("IIb", 3), ("IIIa", 4)])
        dict_stage_patient_list = defaultdict(list)
        line_number = 0
        with open(FILEPATH_PATIENT_INFO) as fp:
            next(fp) # skip header
            for line in fp:
                tokens = line.split("\t")[0].strip().split("-")
                stage = tokens[0]
                stage = dict_stage_name[stage]
                # patient_id = int(patient_id[1])
                dict_stage_patient_list[stage].append(line_number)
                line_number += 1
        return dict_stage_patient_list

class Meth300PlusStageMapper(PatientStageMapper):
    @classmethod
    def get_dict_stage_line_number(cls):
        dict_stage_patient_list = defaultdict(list)
        dict_stage_patient_list[1] = [100, 101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 113, 114, 117, 118, 120, 121, 122, 124, 126, 127, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 143, 144, 145, 146, 147, 148, 150, 151, 152, 154, 155, 156, 158, 159, 160, 161, 162, 163, 164, 165, 169, 171, 172, 173, 174, 175, 176, 177, 178, 180, 181, 182, 183, 184, 185, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 198, 199]
        dict_stage_patient_list[2] = [109, 112, 115, 116, 119, 123, 125, 128, 135, 142, 149, 153, 157, 166, 167, 168, 170, 179, 186, 197]
        return dict_stage_patient_list


if __name__ == '__main__':
    dict_stage_patient_list = Meth300StageMapper.get_get_patient_line_number_by_stage(1)
    print(dict_stage_patient_list)
    dict_stage_patient_list = Meth300StageMapper.get_get_patient_line_number_by_stage(2)
    print(dict_stage_patient_list)
    dict_stage_patient_list = Meth300StageMapper.get_get_patient_line_number_by_stage(3)
    print(dict_stage_patient_list)
    print(Meth300StageMapper.sorted_keys())