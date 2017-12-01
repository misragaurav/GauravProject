# -*- coding: utf-8 -*-
"""
Function for calculating the ratio of Early Prescriptions to Total Prescriptions for each state
"""
import pandas as pd

def calc_early_adopters_by_total_adopters(early_claims, late_claims, table):

    pd.isnull(early_claims['patient_state']).value_counts() # only 55/13600 NaNs for Invokana
    pd.isnull(late_claims['patient_state']).value_counts() # only 168/55700 NaNs for Invokana
    
    early_claims_clean_states=early_claims[pd.notnull(early_claims['patient_state'])]
    late_claims_clean_states=late_claims[pd.notnull(late_claims['patient_state'])]
    
    #early_claims_clean_states['patient_state'].value_counts().plot(figsize=(12,6), title='Invokana State-wise Early Rx')
    #late_claims_clean_states['patient_state'].value_counts().plot(figsize=(12,6), title='Invokana State-wise Late Rx')
    
    early_by_state=early_claims_clean_states['patient_state'].value_counts()
    early_by_state.sort_index(axis=0,inplace=True)
    early_by_state.drop(early_by_state.index[0],inplace=True)
    
    late_by_state=late_claims_clean_states['patient_state'].value_counts()
    late_by_state.sort_index(axis=0,inplace=True)
    late_by_state.drop(late_by_state.index[0],inplace=True)
    
    table_clean_state=table[pd.notnull(table['patient_state'])]
    
    total_by_state=table_clean_state['patient_state'].value_counts()
    total_by_state.sort_index(axis=0,inplace=True)
    total_by_state.drop(total_by_state.index[0],inplace=True)
    
    #(early_total_by_state/total_by_state).plot(figsize=(12,6), title='Fraction of Rx in the Early Adoption Period of Invokana')
    #(early_total_by_state/total_by_state).sort_values().plot(figsize=(8,6), title='Fraction of Rx in the Early Adoption Period of Invokana')
    
    early_by_total=(early_by_state/total_by_state).sort_values()
    
    early_by_total=early_by_total.to_frame()
    
    early_by_total['state'] = early_by_total.index
    early_by_total.rename(columns={'patient_state':'early_by_total'}, inplace=True)
    early_by_total.reset_index(drop=True,inplace=True)
    
    return early_by_total, total_by_state
        