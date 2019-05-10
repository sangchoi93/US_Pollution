#!/usr/bin/env python
# coding: utf-8

# Importing datasets into pandas

# In[101]:


import matplotlib as plt
import kaggle
import zipfile
import pandas as pd
import numpy as np
import os
import pickle


print('downloading kaggle dataset')
#downloading pollution_us dataset if doesnt exist locally
us_pollution_filename = 'pollution_us_2000_2016.csv'
if not(os.path.isfile(us_pollution_filename)):
    kaggle.api.dataset_download_file('sogun3/uspollution', us_pollution_filename)
    zip_ref = zipfile.ZipFile(us_pollution_filename+'.zip', 'r')
    zip_ref.extractall()
    zip_ref.close()
df_us_pollution = pd.read_csv(us_pollution_filename)

#assuming resp dataset already exists locally
resp_data_path = 'IHME_USA_COUNTY_RESP_DISEASE_MORTALITY_1980_2014_NATIONAL_Y2017M09D26.XLSX'
list_sheet_names = ['Chronic respiratory diseases', 'Chronic obstructive pulmonary ', 'Pneumoconiosis', 'Silicosis',
                   'Asbestosis', 'Coal workers pneumoconiosis', 'Other pneumoconiosis', 'Asthma', 'Interstitial lung disease',
                   'Other chronic respiratory ']
df_resp_disease = pd.read_excel(resp_data_path, skiprows=1, sheet_name=list_sheet_names)


print('cleaning up respiratory disease mortality dataset and dumping the result into df_resp_mortality.pkl')
for x in list_sheet_names:
    #dropping mortality rate measured below year 2000
    #dropping any na values
    df_resp_disease[x].drop(['Mortality Rate, 1980*', 'Mortality Rate, 1985*', 'Mortality Rate, 1990*', 'Mortality Rate, 1995*'],
                           inplace=True, errors='ignore', axis=1)
    df_resp_disease[x].dropna(inplace=True)
    #dropping county data, state mortality rate is average of all counties
    df_resp_disease[x].drop(df_resp_disease[x][df_resp_disease[x].FIPS>57].index, inplace=True)
#     #Extracting state out of Location
#     df_resp_disease[x]['state'] = df_resp_disease[x]['Location']\
#     .apply(lambda x: x.split(',')[1].strip() if len(x.split(',')) > 1 else x.strip())
    df_resp_disease[x]['mortality_2000'] = df_resp_disease[x]['Mortality Rate, 2000*'].\
        apply(lambda x: x.split(' ')[0].strip())
    df_resp_disease[x]['mortality_2005'] = df_resp_disease[x]['Mortality Rate, 2005*'].\
        apply(lambda x: x.split(' ')[0].strip())
    df_resp_disease[x]['mortality_2010'] = df_resp_disease[x]['Mortality Rate, 2010*'].\
        apply(lambda x: x.split(' ')[0].strip())
    df_resp_disease[x]['mortality_2014'] = df_resp_disease[x]['Mortality Rate, 2014*'].\
        apply(lambda x: x.split(' ')[0].strip())
    df_resp_disease[x].drop(['Mortality Rate, 2000*','Mortality Rate, 2005*','Mortality Rate, 2010*',\
                             'Mortality Rate, 2014*','% Change in Mortality Rate, 1980-2014'], \
                            axis=1, inplace=True)

#stacking all sheets into one dataframe
df_resp_mortality_cleaned = pd.DataFrame()
for x in list_sheet_names:
    for column in ['mortality_2000','mortality_2005','mortality_2010','mortality_2014']:
        df_tmp = pd.DataFrame(df_resp_disease[x][column]).rename(columns={column : 'mortality_rate'})
        df_tmp['year']=int(column[-4:])
        df_tmp['disease']=x
        df_tmp['state']=df_resp_disease[x].Location
        df_resp_mortality_cleaned = df_resp_mortality_cleaned.append(df_tmp)

df_resp_mortality_cleaned.reset_index(inplace=True, drop=True)
pickle.dump( df_resp_mortality_cleaned, open( 'df_resp_mortality.pkl', "wb" ) )


print('cleaning up pollution dataset and dumping the result into df_us_pollution.pkl')

#df_us_pollution does not have data for all counties, therefore need to do it based on state
#need to aggregate by year in date local field to match with mortality data ([2000, 2005, 2010, 2014])
df_us_pollution['year'] = pd.DatetimeIndex(df_us_pollution['Date Local']).year
series_year_data = df_us_pollution['year']
df_us_pollution['year_bin'] = np.where(series_year_data<=2000, 2000,
                                      np.where(np.logical_and(series_year_data>2000, series_year_data<=2005), 2005,
                                      np.where(np.logical_and(series_year_data>2005, series_year_data<=2010), 2010, 
                                      np.where(np.logical_and(series_year_data>2010, series_year_data<=2014), 2014, np.nan))))
df_us_pollution_cleaned = df_us_pollution.drop(['State Code', 'County Code', 'Site Num', 'Address', 'County', 'City', 
                                                'Date Local'], axis=1)
pickle.dump( df_us_pollution_cleaned, open( 'df_us_pollution.pkl', "wb" ) )