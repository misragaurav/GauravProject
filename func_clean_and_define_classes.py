# -*- coding: utf-8 -*-
"""
This file contains a few functions for splitting the providers into two classes - Innovators and Traditionals
The function innovators_traditionals_adopters_by_numb_of_claims splits them by the number of claims written and time to writing the first prescription
The function innovators_traditionals_adopters_by_volume splits them by the volume of drugs prescribed and time to writing the first prescription
The function unique_adopters_early_late splits them by time to writing the first prescription
The function unique_adopters_strong_weak them by volume of total prescriptions written

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def clean_table(table):
    pd.isnull(table['date_service']).value_counts()
    table.dropna(axis=1, how='all', inplace=True)
    table['date_service']=pd.to_datetime(table['date_service'])
    table.sort_values(by=['date_service'],inplace=True)
    table.reset_index(drop=True,inplace=True)
    
    # Dropping records with null NPI
    table=table[pd.notnull(table['prov_prescribing_npi'])]
    table.reset_index(drop=True,inplace=True)
    return table

def innovators_traditionals_adopters_by_numb_of_claims(prov_date_claims, early_fraction, late_fraction, claims_high, claims_low):
    unique_dates=prov_date_claims['date_service'].unique()
    
    early_adop_thresh=round(len(unique_dates)*early_fraction)
    early_adop_deadline=unique_dates[early_adop_thresh]
    
    innovators=prov_date_claims[(prov_date_claims['date_service']<=early_adop_deadline) & (prov_date_claims['numb_of_claims']>=claims_high)]
    innovators.is_copy=False
    innovators['labels']=np.ones(len(innovators))
    
    late_adop_thresh=round(len(unique_dates)*(1-late_fraction))
    late_adop_deadline=unique_dates[late_adop_thresh]
    traditionals=prov_date_claims[(prov_date_claims['date_service']>=late_adop_deadline) & (prov_date_claims['numb_of_claims']<=claims_low)]
    traditionals.is_copy=False
    traditionals['labels']=np.zeros(len(traditionals))
    
    innovators_traditionals=pd.concat([innovators,traditionals])
    return innovators_traditionals

def innovators_traditionals_adopters_by_volume(prov_date_claims, early_fraction, late_fraction, vol_high, vol_low):
    unique_dates=prov_date_claims['date_service'].unique()
    
    early_adop_thresh=round(len(unique_dates)*early_fraction)
    early_adop_deadline=unique_dates[early_adop_thresh]
    
    innovators=prov_date_claims[(prov_date_claims['date_service']<=early_adop_deadline) & (prov_date_claims['volume_of_drugs']>=vol_high)]
    innovators.is_copy=False
    innovators['labels']=np.ones(len(innovators))
    
    late_adop_thresh=round(len(unique_dates)*(1-late_fraction))
    late_adop_deadline=unique_dates[late_adop_thresh]
    traditionals=prov_date_claims[(prov_date_claims['date_service']>=late_adop_deadline) & (prov_date_claims['volume_of_drugs']<=vol_low)]
    traditionals.is_copy=False
    traditionals['labels']=np.zeros(len(traditionals))
    
    innovators_traditionals=pd.concat([innovators,traditionals])
    return innovators_traditionals

def unique_adopters_early_late(table, early_fraction, late_fraction):
    unique_dates=table['date_service'].unique()

    early_adop_thresh=round(len(unique_dates)*early_fraction)
    early_adop_deadline=unique_dates[early_adop_thresh]
    table_early_claims=table[table['date_service'] <= early_adop_deadline]
    uniq_early_adopters=table_early_claims['prov_prescribing_npi'].unique()
    uniq_early_adopters=np.stack((uniq_early_adopters,np.ones(len(uniq_early_adopters))),axis=1) # np.stack joins along new dimension

    late_adop_thresh=round(len(unique_dates)*(1-late_fraction))
    late_adop_deadline=unique_dates[late_adop_thresh]
    table_late_claims=table[table['date_service'] >= late_adop_deadline]
    table_not_late_claims=table[table['date_service'] < late_adop_deadline]

    uniq_prescribers_in_end=table_late_claims['prov_prescribing_npi'].unique()
    uniq_prescribers_before_end=table_not_late_claims['prov_prescribing_npi'].unique()
    intersection=np.intersect1d(uniq_prescribers_in_end,uniq_prescribers_before_end)
    uniq_late_adopters=np.setdiff1d(uniq_prescribers_in_end,intersection)
    uniq_late_adopters=np.stack((uniq_late_adopters,np.zeros(len(uniq_late_adopters))),axis=1) 
    
    return uniq_early_adopters, uniq_late_adopters, table_early_claims, table_late_claims
    
def unique_adopters_strong_weak(table, strong_threshold, weak_threshold=1):
    claims_submitted_by_docs=(table[['prov_prescribing_npi','claim_id']].groupby(['prov_prescribing_npi'],as_index=False).count()).sort_values('claim_id',axis=0)
    claims_submitted_by_docs.is_copy=False
    claims_submitted_by_docs['strong_adop']=np.NaN
    claims_submitted_by_docs['strong_adop'].iloc[np.where(claims_submitted_by_docs['claim_id']>=strong_threshold)]=1
    claims_submitted_by_docs['strong_adop'].iloc[np.where(claims_submitted_by_docs['claim_id']<=weak_threshold)]=0
    claims_submitted_by_docs['strong_adop'].value_counts()
    table_strong_weak_adop=claims_submitted_by_docs[(claims_submitted_by_docs['strong_adop']==1)|(claims_submitted_by_docs['strong_adop']==0)]
    table_strong_weak_adop.rename(columns={'claim_id':'numb_of_claims'}, inplace=True)
    table_strong_weak_adop.sort_values(['strong_adop'],ascending=False, inplace=True)
    table_strong_weak_adop.reset_index(drop=True,inplace=True)
    table_strong_weak_labeled_claims=table.merge(table_strong_weak_adop,how='inner',on='prov_prescribing_npi')    
    return table_strong_weak_adop, table_strong_weak_labeled_claims

def unique_adopters_plot(table, column_name, legend):
    otherFontsize=22
    max_frac=100
    numb_uniq_adopters=[]
    frac_timeline=list(range(1,max_frac))

    for numb in frac_timeline:
        frac_definition=numb/max_frac
        early_adop_thresh=round(len(table['date_service'].unique())*frac_definition)        
        temp=table['date_service'].unique()        
        early_adop_deadline=temp[early_adop_thresh]        
        table_early_adop=table[table['date_service'] <= early_adop_deadline]        
        numb_uniq_adopters.append(table_early_adop[column_name].nunique())
    plt.figure(figsize=(8,6))
    plt.plot(frac_timeline,numb_uniq_adopters)
    plt.xlabel('Percentage of Year', fontsize=otherFontsize)
    plt.ylabel('Number of Unique Individuals', fontsize=otherFontsize)
    plt.title(legend, fontsize=otherFontsize)
    
    return frac_timeline,numb_uniq_adopters    
