import pandas as pd
import numpy as np
import lightgbm
import pickle

# this should be your standarClass
class transform_predict:
    #put your methods here
    def __load_file__(self,nome_arquivo):
        with open(nome_arquivo, 'rb') as input:
            objeto = pickle.load(input)
        return objeto

    def __init__(self,path='./'):
        # all of your pickled models/hdf5 must be stored in the same folder as your elts class
        self.path = path
        self.modelRisk = self.__load_file__(self.path+'model.pkl')
        self.varsRisk = self.__load_file__(self.path+'variables.pkl')

    #This method MUST exist in your class
    def transform_predict(self,x):

        __dic__ = {}
        
        y = x.copy()
        for feat in self.varsRisk+['revenueAmount']:
            if feat not in y.columns:
                y.loc[:,feat] = np.nan
        y[self.varsRisk] = y[self.varsRisk].fillna(0).div(y['revenueAmount'], axis=0)
        y = y[self.varsRisk]
        y[self.varsRisk] = y[self.varsRisk].div(y[self.varsRisk].max(axis=1), axis=0)
        __dic__['dummyExample'] = self.modelRisk.predict(y[self.varsRisk])[0]
        __dic__['dummyExampleVersion'] = 'itWorks!'

        return __dic__