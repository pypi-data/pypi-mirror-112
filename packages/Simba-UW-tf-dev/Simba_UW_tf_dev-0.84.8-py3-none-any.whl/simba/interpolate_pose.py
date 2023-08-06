import pandas as pd
from configparser import ConfigParser, NoOptionError, NoSectionError
from simba.drop_bp_cords import *
import numpy as np


class Interpolate(object):
    def __init__(self, config_file_path, in_file):
        self.in_df = in_file #in file is a pandas dataframe
        configFile = str(config_file_path)
        config = ConfigParser()
        config.read(configFile)
        Xcols, Ycols, Pcols = getBpNames(config_file_path)
        self.columnHeaders = getBpHeaders(config_file_path)
        noAnimals = config.getint('General settings', 'animal_no')
        try:
            multiAnimalIDList = config.get('Multi animal IDs', 'id_list')
            multiAnimalIDList = multiAnimalIDList.split(",")
            if multiAnimalIDList[0] != '':
                multiAnimalStatus = True
            else:
                multiAnimalStatus = False
                for animal in range(noAnimals):
                    multiAnimalIDList.append('Animal_' + str(animal + 1))
        except NoSectionError:
            multiAnimalIDList = []
            for animal in range(noAnimals):
                multiAnimalIDList.append('Animal_' + str(animal + 1))
            multiAnimalStatus = False
        self.multiAnimalIDList = [x for x in multiAnimalIDList if x]
        self.animalBpDict = create_body_part_dictionary(multiAnimalStatus, multiAnimalIDList, noAnimals, Xcols, Ycols, Pcols, [])

    def detect_headers(self):
        self.multi_index_headers = self.in_df.iloc[0:2]
        self.multi_index_headers_list = []
        for column in self.multi_index_headers:
            self.multi_index_headers_list.append((column, self.multi_index_headers[column][0], self.multi_index_headers[column][1]))
        self.in_df.columns = self.columnHeaders
        self.current_df = self.in_df.iloc[2:].apply(pd.to_numeric).reset_index(drop=True)

    def fix_missing_values(self, method):
        self.animal_df_list, self.header_list_p = [], []
        for animal in self.multiAnimalIDList:
            currentAnimalX, currentAnimalY, currentAnimalP = self.animalBpDict[animal]['X_bps'], self.animalBpDict[animal]['Y_bps'], self.animalBpDict[animal]['P_bps']
            header_list_xy = []
            for col1, col2, col3, in zip(currentAnimalX, currentAnimalY, currentAnimalP):
                header_list_xy.extend((col1, col2))
                self.header_list_p.append(col3)
            self.animal_df_list.append(self.current_df[header_list_xy])

        for loop_val, animal_df in enumerate(self.animal_df_list):
            repeat_bol = animal_df.eq(animal_df.iloc[:, 0], axis=0).all(axis='columns')
            indices_to_replace_animal = repeat_bol.index[repeat_bol].tolist()
            print('Detected ' + str(len(indices_to_replace_animal)) + ' missing pose-estimation frames for ' + str(self.multiAnimalIDList[loop_val]) + '...')
            animal_df.loc[indices_to_replace_animal] = np.nan
            if method == 'Linear':
                self.animal_df_list[loop_val] = animal_df.interpolate(method='linear', axis=0).ffill().bfill()
            if method == 'Nearest':
                self.animal_df_list[loop_val] = animal_df.interpolate(method='nearest', axis=0).ffill().bfill()
            if method == 'Quadratic':
                self.animal_df_list[loop_val] = animal_df.interpolate(method='quadratic', axis=0).ffill().bfill()
        self.new_df = pd.concat(self.animal_df_list, axis=1)

    def reorganize_headers(self):
        loop_val = 2
        for p_col_name in self.header_list_p:
            p_col = list(self.in_df[p_col_name].iloc[2:])
            self.new_df.insert(loc=loop_val, column=p_col_name, value=p_col)
            loop_val += 3
        self.new_df.columns = pd.MultiIndex.from_tuples(self.multi_index_headers_list, names=('scorer', 'bodyparts', 'coords'))


