# -*- coding: utf-8 -*-
"""
"""

# 1. load xlxs ala readlines 
# create dictionaries per sheets 
# reg expres ^cw + 
# differentiate parts 
# visualize 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
class rege(object):
    def __init__(self):
        self.xls= pd.ExcelFile('TRN23.xlsx')
        self.xls_sheets = self.xls.sheet_names
        self.dct = {}
    def df_from_sheet(self, sheet_name):
        self.dct[sheet_name] = {}
        local_dct = self.dct[sheet_name]
        self.df = self.xls.parse(sheet_name)                # read a specific sheet to DataFrame
        self.df.replace(np.nan,0, inplace=True)
        return self.df
    def get_cwdf(self, sheet_name):
        # compile cw integers
        self.df_from_sheet(sheet_name)
        self.cw_df  = self.df[sheet_name].str.extract(r"^cw(\d+\d+):").dropna().astype(int)
    def get_massdf(self, sheet_name):
        self.get_cwdf( sheet_name)
        self.df_mass_prep = self.df[sheet_name].loc[self.cw_df.index]
        self.df_mass      = self.df_mass_prep.str.split(':', expand = True)
        sdf = self.df_mass.shape[1]
        df_last = self.df_mass.loc[:,sdf-1]
        where_None= df_last[df_last.isna()==True].index
        self.df_mass.loc[where_None,sdf-1] =  self.df_mass.loc[where_None,sdf-2]
        self.m =self.df_mass.loc[:,sdf-1].str.replace(',', '.')
    def compile_sheet(self, sheet_name):
        self.dct[sheet_name] = {}
        self.get_massdf(sheet_name)
        local_dct = self.dct[sheet_name]
        local_dct[ 'cw'] = self.cw_df.values 
        local_dct[  'm'] = self.m.values
        local_dct[ 'df'] = self.df
        # self.L = L
        return self.df
    def plot_sheet_mass(self, sheet_name, separated_graphs = False):
        if separated_graphs: plt.figure()
        x, y = self.dct[sheet_name]['cw'], self.dct[sheet_name]['m']
        plt.plot(x,y, label = sheet_name)
        plt.scatter(x,y, label = sheet_name)
        plt.legend()    
    def full_test(self, **kargs):
        self.__init__()
        for _ in self.xls_sheets:
            print(_)
            try:
                r.compile_sheet(_)
                r.plot_sheet_mass(_, **kargs)
            except: pass
        rd = r.dct


r = rege() 
r.full_test(separated_graphs=False)
# %%
# sheet_name = 'BINO'
# r.compile_sheet(sheet_name)
# %%
# %% Full test
# r = rege() 
# for _ in r.xls_sheets:
#     print(_)
#     try:
#         r.compile_sheet(_)
#         r.plot_sheet_mass(_)
#     except: pass
# rd = r.dct
# %%

# # def pool_exerci(self_df, sheet_name): #self_df pak jen prehodit pro classu
    
# # %%
# # df2 = df.loc[c3.index + 1]
# # df3 = df.loc[c3.index + 4]

