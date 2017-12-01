# -*- coding: utf-8 -*-
"""
Analytics for Prediction of Early Adopters of T2D Drugs
For use by Foresite Capital
Created on Wed Oct  4 08:39:49 2017
@author: Gaurav Misra
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pickle
import importlib
import sys

# Setting basics options
split_providers_by_volume_of_drug='no' # 'no' splits them by number of prescriptions written

# read in the raw data files into dataframes
table_invokana=pd.read_csv('pharmacy_claims_invokana.zip', sep='|',compression='zip')
table_trulicity=pd.read_csv('pharmacy_claims_trulicity.zip', sep='|',compression='zip')
schema=pd.read_excel('schema_gaurav.xlsx')

# Generic Plot Settings
matplotlib.rcParams.update({'font.size': 22})
matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 

# Display options
np.set_printoptions(threshold=np.nan) # To prevent summarization of long arrays while printing
pd.options.display.max_rows = 400     # To prevent summarization of long dataframes while printing
pd.options.display.max_columns = 40   # To prevent summarization of wide dataframes while printing

# importing cleaning function
from func_clean_and_define_classes import clean_table
# The following 3 commented lines can be uncommented if one wants to make changes to the imported function and re-import it.
#import func_clean_and_define_classes 
#func_clean_and_define_classes=importlib.reload(func_clean_and_define_classes)
#clean_table=func_clean_and_define_classes.clean_table

#% Call cleaning function on both tables
table_invokana=clean_table(table_invokana)
table_trulicity=clean_table(table_trulicity)

# importing function to calculate number of claims prescribed and total volume prescribed by each provider
from func_calc_numb_of_claims_and_volume import calc_numb_of_claims_and_volume

# calculating number of claims prescribed and total volume prescribed by each provider
prov_date_claims_vol_Invo=calc_numb_of_claims_and_volume(table_invokana)
prov_date_claims_vol_Trul=calc_numb_of_claims_and_volume(table_trulicity)


#%% Identifying the common providers between trulicity and invokana claims datasets
from func_providers_common_bet_invo_trul import providers_common_bet_invo_trul

prov_date_claims_common=providers_common_bet_invo_trul(prov_date_claims_vol_Invo,prov_date_claims_vol_Trul)

#%% Splitting the providers into Innovator and Traditional classes based on the chosen criteria

if (split_providers_by_volume_of_drug=='yes'):
    # importing functions that define the "innovator" and "traditional" classes by assigning the providers to one or the other class
    from func_clean_and_define_classes import innovators_traditionals_adopters_by_volume
    
    ## Define Innovators and Traditionals based on volume of drugs moved
    early_fraction=0.25 # definition of "early" in time fraction.
    late_fraction=0.25  # definition of "late" in time fraction.
    vol_high=1200       # definition of large volume of drug prescribed.
    vol_low=500         # definition of low volume of drug prescribed.
    
    common_innovators_traditionals=innovators_traditionals_adopters_by_volume(
            prov_date_claims_common, 
            early_fraction, 
            late_fraction, 
            vol_high, 
            vol_low)
    common_innovators_traditionals.drop('date_service',axis=1,inplace=True)
    common_innovators_traditionals=common_innovators_traditionals.as_matrix()
    
    common_innovators_traditionals[:,3].sum()                                       # Number in the +ve class
    len(common_innovators_traditionals)-common_innovators_traditionals[:,3].sum()   # Number in the -ve class
    len(common_innovators_traditionals)                                             # Total Number in the +ve and the -ve classes
    
    pickle_file='common_innovators_traditionals_by_volume.pkl'        

elif (split_providers_by_volume_of_drug=='no'):
    # importing functions that define the "innovator" and "traditional" classes by assigning the doctors to one or the other class
    from func_clean_and_define_classes import innovators_traditionals_adopters_by_numb_of_claims
    
    ## Define Innovators and Traditionals based on number of claims
    early_fraction=0.25 # definition of "early" in time fraction.
    late_fraction=0.25  # definition of "late" in time fraction.
    claims_high=12      # definition of large number of claims prescribed.
    claims_low=8        # definition of low number of claims prescribed.
    
    common_innovators_traditionals=innovators_traditionals_adopters_by_numb_of_claims(
            prov_date_claims_common, 
            early_fraction, 
            late_fraction, 
            claims_high, 
            claims_low)
    common_innovators_traditionals.drop('date_service',axis=1,inplace=True)
    common_innovators_traditionals=common_innovators_traditionals.as_matrix()
    
    common_innovators_traditionals[:,3].sum()                                                             # Number in the +ve class
    len(common_innovators_traditionals)-common_innovators_traditionals[:,3].sum()       # Number in the -ve class
    len(common_innovators_traditionals)                                                                   # Total Number in the +ve and the -ve classes
    
    pickle_file='common_innovators_traditionals_by_prescriptions.pkl'        

else:
    sys.exit('Please set the split_providers_by_volume_of_drug variable to \'yes\' or \'no\' and start over. Bailing out')

#%%
#% Calling Parallel download of NPI data from the CMS website
from func_parallel_download import parallel_download

npi_dict=parallel_download(common_innovators_traditionals,0) # the second argument to the call is the columns number of NPI info in the matrix common_innovators_traditionals

f = open(pickle_file,"wb")
pickle.dump(npi_dict,f)
f.close()
#%%
# Loading pickled data in case downloading the data again is not required
with open(pickle_file, 'rb') as f:
    npi_dict = pickle.load(f)

from func_clean_and_select_data_from_dict import clean_and_select_data_from_dict

doc_info_list, labels, counter_missing_records, npi_missing_info=clean_and_select_data_from_dict(common_innovators_traditionals, 3, npi_dict) # The second argument is the column number for the class labels in the matrix   

doc_info_frame=pd.DataFrame(doc_info_list)

# Adding labels to datafrome here
doc_info_frame['labels']=labels              

# Extracting and saving the zip code info here because 'a_postal_code' column will be dropped from the feature list as it is not really a feature.
doc_npi_zipcode=doc_info_frame[['npi','a_postal_code']]
doc_npi_zipcode.is_copy=False
doc_npi_zipcode.rename(columns={'a_postal_code': 'zip'}, inplace=True)
for ind, zipcode in enumerate(doc_npi_zipcode['zip']):
    doc_npi_zipcode.iloc[ind,1]= zipcode[:5]

# Clean downloaded data in dataframe
from func_drop_unclean_and_correlated_features import drop_unclean_and_correlated_features
doc_info_frame=drop_unclean_and_correlated_features(doc_info_frame)

# Binarize the enumeration date feature
year_int=pd.DatetimeIndex(pd.to_datetime(doc_info_frame['b_enumeration_date'])).year
doc_info_frame['b_enumeration_date']=pd.cut(year_int,2,precision=0,labels=["old","yng"]) # This feature has a problem - the providers that started before 2005 have their enumeration date as 2005 

# importing function for adding features from other datasets
# features like countywise poverty index
from func_add_features_from_other_datasets import add_features_from_other_datasets
doc_info_frame,income_frame_subset, zip_frame=add_features_from_other_datasets(doc_info_frame, doc_npi_zipcode)
#%%

###### Analytics - New to brand 
from func_clean_and_define_classes import unique_adopters_plot

frac_timeline,new_to_invokana_providers=unique_adopters_plot(table_invokana,'prov_prescribing_npi', 'New to Brand Providers of Invokana')
frac_timeline,new_to_invokana_patients=unique_adopters_plot(table_invokana,'hvid', 'New to Brand Patients of Invokana')

frac_timeline,new_to_trulicity_providers=unique_adopters_plot(table_trulicity,'prov_prescribing_npi', 'New to Brand Providers of Trulicity')
frac_timeline,new_to_trulicity_patients=unique_adopters_plot(table_trulicity,'hvid', 'New to Brand Patients of Trulicity')

### Analytics - Total volumne dispensed by month
# The columns "dispensed_quantity" and "days_supply" are the same
plt.figure(figsize=(8,6))
table_invokana[['date_service','dispensed_quantity']].groupby([pd.Grouper(freq='1M',key='date_service')]).sum().plot(figsize=(6,4), title='Total Volume for Invokana',legend=False, fontsize=12)
table_trulicity[['date_service','dispensed_quantity']].groupby([pd.Grouper(freq='1M',key='date_service')]).sum().plot(figsize=(6,4), title='Total Volume for Trulicity',legend=False, fontsize=12)

##### Analytics Counts of Refills authorized
plt.figure(figsize=(8,6))
refill_auth=table_invokana.refill_auth_amount.value_counts()
plt.scatter(refill_auth.index,refill_auth.values, label='Drug I')
refill_auth_Trul=table_trulicity.refill_auth_amount.value_counts()
plt.scatter(refill_auth_Trul.index,refill_auth_Trul.values, label='Drug T')
plt.xlabel('Refills Authorized',fontsize=18)
plt.ylabel('Counts',fontsize=18)
plt.title('Counts of Refills Authorized',fontsize=22)
plt.yscale('log')
plt.legend(prop={'size': 16})

# Some extra plots
#sns.distplot(temp['numb_of_claims'], bins=600, kde=False, rug=False, axlabel='Number of Claims')
#claims_submitted_by_docs_Invo['numb_of_claims'].hist(bins=600,figsize=(12,12), range=(0,50),histtype='bar',rwidth=2)

#%table_invokana['prov_prescribing_npi']=[str(int(item)) for item in table_invokana['prov_prescribing_npi']]
#high_adop_timeline=high_vol_adopters.merge(table_invokana[['prov_prescribing_npi','date_service']],how='inner',on='prov_prescribing_npi')
#for i,npi in enumerate(high_vol_adopters['prov_prescribing_npi']):
#for i in list(range(0,10,6)):
#    single_provider=table_invokana[high_vol_adopters['prov_prescribing_npi'].iloc[i]==table_invokana['prov_prescribing_npi']][['date_service','claim_id']]
#    single_provider.groupby(pd.Grouper(freq='1M',key='date_service')).count().plot(kind='bar')

#%% Choropleths of Prescriptions
from func_plotly_choropleth import plotly_choropleth 
from func_clean_and_define_classes import unique_adopters_early_late

# Defining early and late adopters by the time fraction
early_fraction=0.15 # Those to made the first prescription in the first x fraction of the year
late_fraction=0.05  # Those to made the first prescription in the last y fraction of the year

# Splitting Invokana providers
invo_early_adopters, invo_late_adopters, invo_early_claims, invo_late_claims=unique_adopters_early_late(table_invokana, early_fraction, late_fraction)
# Splitting Trulicity providers
trul_early_adopters, trul_late_adopters, trul_early_claims, trul_late_claims=unique_adopters_early_late(table_trulicity, early_fraction, late_fraction)

from func_calc_early_adopters_by_total_adopters import calc_early_adopters_by_total_adopters
import func_calc_early_adopters_by_total_adopters
func_calc_early_adopters_by_total_adopters=importlib.reload(func_calc_early_adopters_by_total_adopters)
calc_early_adopters_by_total_adopters=func_calc_early_adopters_by_total_adopters.calc_early_adopters_by_total_adopters

# Calculating the ratio of Early to Total Prescriptions Across States
invo_early_by_total, invo_total_by_state=calc_early_adopters_by_total_adopters(invo_early_claims, invo_late_claims, table_invokana)

trul_early_by_total, trul_total_by_state=calc_early_adopters_by_total_adopters(trul_early_claims, trul_late_claims, table_trulicity)

# Plotting choropleths for Invokana and Trulicity
plotly_choropleth(invo_early_by_total,'early_by_total',title='Invokana: Early to Total Prescriptions Ratio Across States')

plotly_choropleth(trul_early_by_total,'early_by_total',title='Trulicity: Early to Total Prescriptions Ratio Across States')

# Plotting total Invokana Prescriptions by State
invo_total_by_state=invo_total_by_state.to_frame()
invo_total_by_state['state'] = invo_total_by_state.index
invo_total_by_state.rename(columns={'patient_state':'total_Rx'}, inplace=True)
invo_total_by_state.reset_index(drop=True,inplace=True)
plotly_choropleth(invo_total_by_state,'total_Rx',title='Invokana: Total Prescriptions')

# Plotting total Trulicity Prescriptions by State
trul_total_by_state=trul_total_by_state.to_frame()
trul_total_by_state['state'] = trul_total_by_state.index
trul_total_by_state.rename(columns={'patient_state':'total_Rx'}, inplace=True)
trul_total_by_state.reset_index(drop=True,inplace=True)
plotly_choropleth(trul_total_by_state,'total_Rx',title='Trulicity: Total Prescriptions')

#%% Choropleths of other data

# Reading the state name to state codes mapping from saved csv file
state_codes=pd.read_csv('state_codes.csv',header=0)

# Reading the diabetes incidence rates from saved csv file
incidence=pd.read_csv('diabetes_incidence.csv',encoding = "ISO-8859-1", skiprows=1, header=0)
incidence.replace('No Data',np.nan, inplace=True)
incidence.rename(columns={'State':'state_name', 'County':'county'}, inplace=True)
state_name_FIPS_codes_county_name=incidence[incidence.columns[:3]]

incidence_rates=incidence[incidence.columns[7:71:7]]
temp=list(incidence_rates)
year_names_dict={temp[0]:'2004',temp[1]:'2005',temp[2]:'2006',temp[3]:'2007',temp[4]:'2008',temp[5]:'2009',temp[6]:'2010',temp[7]:'2011',temp[8]:'2012',temp[9]:'2013'}
incidence_rates.is_copy=False
incidence_rates.rename(columns=year_names_dict, inplace=True)
incidence_rates=incidence_rates.apply(pd.to_numeric)
incidence_rates.fillna(method='pad', inplace=True) # Padding missing rates

incidence_all=pd.concat([state_name_FIPS_codes_county_name, incidence_rates],axis=1)
#incidence_all['growth_rate']=growth_rate_of_diabetes

incidence_all=incidence_all.merge(state_codes,how='inner',on='state_name')

incidence_all_pov=incidence_all.merge(income_frame_subset[['county','state','percent_pov']],how='inner',on=['county','state'])

population_by_state=zip_frame[['irs_estimated_population_2014','state']].groupby('state',as_index=False).sum()

hybrid_index=pd.to_numeric(incidence_all_pov['percent_pov'])*pd.to_numeric(incidence_all_pov['2013'])

incidence_all_pov['percent_pov']=pd.to_numeric(incidence_all_pov['percent_pov'])
incidence_all_pov['2013']=pd.to_numeric(incidence_all_pov['2013'])
percent_pov_by_state=incidence_all_pov.groupby('state',as_index=False).mean()
percent_pov_by_state_pop=percent_pov_by_state.merge(population_by_state,how='inner',on='state')

percent_pov_by_state_pop['irs_estimated_population_2014']=pd.to_numeric(percent_pov_by_state_pop['irs_estimated_population_2014']).astype(float)

# Calculating the number of patients per state
percent_pov_by_state_pop['num of patients']=(percent_pov_by_state_pop['irs_estimated_population_2014']/1000.0)*percent_pov_by_state_pop['2013']

# Calculating the number of target patients per state
percent_pov_by_state_pop['num of target patients']=((((100.0-percent_pov_by_state_pop['percent_pov'])/100.0)*percent_pov_by_state_pop['irs_estimated_population_2014'])/1000.0)*percent_pov_by_state_pop['2013']

# Plotting various interesting data - run these lines one by one otherwise only the last one will be displayed in the browser window
plotly_choropleth(percent_pov_by_state_pop,'2013',title='Diabetes Incidence Rate per 1000')
plotly_choropleth(percent_pov_by_state_pop,'percent_pov',title='Poverty Rate')
plotly_choropleth(percent_pov_by_state_pop,'irs_estimated_population_2014',title='Total Population')
plotly_choropleth(percent_pov_by_state_pop,'num of patients',title='Patient Population')
plotly_choropleth(percent_pov_by_state_pop,'num of target patients',title='Number of Target Patients')

#plotly_choropleth(high_vol_adopters_grp_by_state,'npi',title='High Vol Adopters')
#plotly_choropleth(low_vol_adopters_grp_by_state,'npi',title='Low Vol Adopters')
#choropleth(percent_pov_by_state_pop,'growth_rate',title='Growth Rate T2D')
#doc_npi_zip_county_income_inci=doc_npi_zip_county_income.merge(incidence_all[['2013','county','state']], how='inner', on=['county','state'])