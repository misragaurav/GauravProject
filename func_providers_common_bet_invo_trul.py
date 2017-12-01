# -*- coding: utf-8 -*-
"""
Function for finding providers who prescribed both, Invokana and Trulicity drugs. This function also calculates 
the average time of first prescription by each provider, the average total number of prescriptions for each provider, 
and the average total volume of drugs prescribed by each provider.
"""

def providers_common_bet_invo_trul(prov_date_claims_vol_Invo,prov_date_claims_vol_Trul):
    import pandas as pd
    
    prov_date_claims_common=prov_date_claims_vol_Trul.merge(prov_date_claims_vol_Invo,how='inner', on='prov_prescribing_npi')
    prov_date_claims_common['avg_numb_of_claims']=prov_date_claims_common[['numb_of_claims_x','numb_of_claims_y']].mean(axis=1)
    prov_date_claims_common['avg_volume_of_drugs']=prov_date_claims_common[['volume_of_drugs_x','volume_of_drugs_y']].mean(axis=1)
    
    prov_date_claims_common['numeric_date_service_x']=pd.to_numeric(prov_date_claims_common['date_service_x'])
    prov_date_claims_common['numeric_date_service_y']=pd.to_numeric(prov_date_claims_common['date_service_y'])
    prov_date_claims_common['avg_numeric_date_service']=prov_date_claims_common[['numeric_date_service_x','numeric_date_service_y']].mean(axis=1)
    
    prov_date_claims_common['avg_date_service']=pd.to_datetime(prov_date_claims_common['avg_numeric_date_service']) ### For Plotting
    prov_date_claims_common.reset_index(drop=True,inplace=True)
    
    # dropping the temporary columns 
    prov_date_claims_common.drop(['date_service_x', 'numb_of_claims_x', 'volume_of_drugs_x', 'date_service_y', 'numb_of_claims_y', 'volume_of_drugs_y', 'numeric_date_service_x', 'numeric_date_service_y','avg_numeric_date_service'],axis=1,inplace=True)
    
    # renaming the calculated column names to the original column names
    prov_date_claims_common.rename(columns={'avg_date_service':'date_service', 'avg_numb_of_claims':'numb_of_claims','avg_volume_of_drugs':'volume_of_drugs'},inplace=True)
    prov_date_claims_common.sort_values(by='date_service',inplace=True) ### This sorting is critical for the code to work correctly
    
    return prov_date_claims_common