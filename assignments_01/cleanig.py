""" 
Module used:
os: To work with paths
pandas: To manipulate data
"""
import os
import pandas as pd

# C:\Treinamentos\faast-foundations\data\eu_life_expectancy_raw.tsv

FILE_NAME = 'eu_life_expectancy_raw.tsv'
data_dir_path = f"{os.path.dirname(os.getcwd())}\\data\\"

eu_life_expectancy_raw = pd.read_csv(f"{data_dir_path}{FILE_NAME}", delimiter = '\t')

eu_life_expectancy_raw = pd.melt(
    eu_life_expectancy_raw,
    id_vars = 'unit,sex,age,geo\\time',

    var_name = 'year',

    value_name = 'value'
)


eu_life_expectancy_raw = eu_life_expectancy_raw[
    eu_life_expectancy_raw['unit,sex,age,geo\\time'].str.split(',').str[-1] == 'PT'
]
eu_life_expectancy_raw = eu_life_expectancy_raw.rename(
    columns={'unit,sex,age,geo\\time': 'unit,sex,age,region'}
)
eu_life_expectancy_raw = eu_life_expectancy_raw[
    eu_life_expectancy_raw['value'].str.strip() != ':'
]
eu_life_expectancy_raw['value'] = eu_life_expectancy_raw['value'].str.split(' ').str[0]

cast_dic = {'year': int, 'value': float}
eu_life_expectancy_raw = eu_life_expectancy_raw.astype(cast_dic)

eu_life_expectancy_raw['unit'] = eu_life_expectancy_raw['unit,sex,age,region'].str.split(',').str[0]

new_columns = eu_life_expectancy_raw.columns[0].split(',')

for column_intex, column in enumerate(new_columns):
    column_value = eu_life_expectancy_raw['unit,sex,age,region'].str.split(',').str[column_intex]
    eu_life_expectancy_raw[column] = column_value
eu_life_expectancy_raw = eu_life_expectancy_raw.drop(['unit,sex,age,region'], axis=1)

new_order = ['unit','sex','age','region','year','value']
eu_life_expectancy_raw = eu_life_expectancy_raw.reindex(columns=new_order)
eu_life_expectancy_raw.head()

eu_life_expectancy_raw.to_csv(
    f"{data_dir_path}eu_life_expectancy_raw.csv", 
    index=False,

    escapechar=''
)
