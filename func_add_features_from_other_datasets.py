# -*- coding: utf-8 -*-
"""
This function adds features to the data from other free datasets downloaded from Census, ADA etc.
"""

def add_features_from_other_datasets(doc_info_frame, doc_npi_zipcode):
    import pandas as pd
    #% Zip code to county and county level income/poverty index
    zip_frame=pd.read_csv('zip_code_database.csv',encoding = "ISO-8859-1")
    zip_frame=zip_frame[zip_frame['zip']>10000] #selecting only counties 
    
    # Padding missing zipcodes because the missing values are mostly likely the same as the surrounding values
    zip_frame['county'].fillna(method='pad', inplace=True) 
    
    # Print missing state rows
    zip_frame[pd.isnull(zip_frame['state'])]['state']
    # Padding missing state info
    zip_frame['state'].fillna(method='pad', inplace=True) 
    
    doc_npi_zipcode['zip']=[int(item) for item in doc_npi_zipcode['zip']]
    
    doc_npi_zip_county=doc_npi_zipcode.merge(zip_frame[['zip','county','state']], how='inner', on='zip')
    
    # Reading in the county level income data
    income_frame=pd.read_csv('county_income_data.csv', header=None)
    income_frame_subset=income_frame[[4,22,23]]
    income_frame_subset.is_copy=False
    income_frame_subset.rename(columns={23:'state', 22:'county', 4:'percent_pov'}, inplace=True)
    list(income_frame_subset)
    
    doc_npi_zip_county_income=doc_npi_zip_county.merge(income_frame_subset, how='inner', on=['county','state'])
    doc_npi_zip_county_income.reset_index(drop=True,inplace=True)
            
    doc_info_frame=doc_info_frame.merge(doc_npi_zip_county_income[['npi','percent_pov']], how='inner', on='npi')
    
    doc_info_frame['percent_pov_cate']=pd.cut(doc_info_frame['percent_pov'],5,precision=0,labels=["vpoor","poor","mid","rich","vrich"])
    
    return doc_info_frame, income_frame_subset, zip_frame