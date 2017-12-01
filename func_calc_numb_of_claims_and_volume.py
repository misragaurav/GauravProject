# -*- coding: utf-8 -*-
"""
Function for calculating the total number of prescriptions and the total volume of drugs moved by each provider
"""

def calc_numb_of_claims_and_volume(table):
    
    # Calculating number of claims prescribed
    claims_submitted_by_docs=(table[['prov_prescribing_npi','claim_id']].groupby(['prov_prescribing_npi'],as_index=False).count()).sort_values('claim_id',axis=0)
    claims_submitted_by_docs.reset_index(drop=True,inplace=True)
    claims_submitted_by_docs.is_copy=False
    claims_submitted_by_docs.rename(columns={'claim_id':'numb_of_claims'}, inplace=True)
    
    # Calculating volume of drug prescribed
    table['volume_of_drugs']=(table['refill_auth_amount'] + 1) * table['dispensed_quantity']
    vol_prescribed_by_docs=(table[['prov_prescribing_npi','volume_of_drugs']].groupby(['prov_prescribing_npi'],as_index=False).sum()).sort_values('volume_of_drugs',axis=0)
    vol_prescribed_by_docs.reset_index(drop=True,inplace=True)
    vol_prescribed_by_docs.is_copy=False
    
    first_instance_claim=table[['prov_prescribing_npi','date_service']].groupby(['prov_prescribing_npi'], as_index=False).first()
    first_instance_claim.sort_values('date_service', axis=0, inplace=True)
    #claims_submitted_by_docs['prov_prescribing_npi']=[str(int(item)) for item in claims_submitted_by_docs['prov_prescribing_npi']]
    prov_date_claims=first_instance_claim.merge(claims_submitted_by_docs, how='inner',on='prov_prescribing_npi')
    prov_date_claims_vol=prov_date_claims.merge(vol_prescribed_by_docs, how='inner',on='prov_prescribing_npi')
    
    ### High vol and low vol adopters
    high_vol_adopters=claims_submitted_by_docs[claims_submitted_by_docs['numb_of_claims']>=50]
    high_vol_adopters['prov_prescribing_npi']=[str(int(item)) for item in high_vol_adopters['prov_prescribing_npi']]

    low_vol_adopters=claims_submitted_by_docs[claims_submitted_by_docs['numb_of_claims']<=8]
    low_vol_adopters['prov_prescribing_npi']=[str(int(item)) for item in low_vol_adopters['prov_prescribing_npi']]

    return prov_date_claims_vol