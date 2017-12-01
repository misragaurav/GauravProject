# -*- coding: utf-8 -*-
"""
Function for extracting features from the data downloaded from the CMS website.
The downloaded data is in a complex format of nested dicts and lists.
For some providers values in the dicts are missing, for some keys are missing.
This function ignores the missing keys and gets those from other providers.
The key names are modified to name them unique because the same key name exists elsewhere in the data. 
More explanation in the comments in the file.
"""
def clean_and_select_data_from_dict(adopters, label_col, npi_dict):
    
    doc_info=dict()
    for npi in adopters[:,0]:
        #print(type(npi))
        #return type(npi)
        try:
            keys_basi=sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['basic'].keys()))
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue
        try:            
            keys_taxo=sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0].keys()))
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue            
        try:
            keys_iden=sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0].keys()))
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue
        try:        
            keys_addr=sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0].keys()))
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue
        try:
            # 'b_' is added to the key name when it comes from the 'basic' field of the dict
            keys_basi_mod=['b_'+key for key in sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['basic'].keys()))]
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue
        try:    
            # 't_' is added to the key name when it comes from the 'taxonomies' field of the dict
            keys_taxo_mod=['t_'+key for key in sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0].keys()))]
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue
        try:
            # 'i_' is added to the key name when it comes from the 'identifiers' field of the dict
            keys_iden_mod=['i_'+key for key in sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0].keys()))]
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue
        try:
            # 'a_' is added to the key name when it comes from the 'addresses' field of the dict
            keys_addr_mod=['a_'+key for key in sorted(list(npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0].keys()))]
        except Exception as e:
            print(e)
            print('This is not a problem, continuing to read keys')
            continue
        if (len(keys_basi)<12): # If a provider is missing any of the keys, skip to the next one to get the key names
            continue
        else:                   # If no missing keys, break the loop and move to the next loop
            break
    
    #% Clean the downloaded dict
    # This loop deals with missing values and keys
    # Missing values are replaced with empty strings
    # Missing keys are replaced with the actual name of keys, followed by populating the values with empty strings
    for count, npi in enumerate(adopters[:,0]):
        if not 'results' in npi_dict[str(npi.astype(int))]:
            continue # These will get dropped later
                
        if not 'basic' in npi_dict[str(npi.astype(int))]['results'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['basic']=[]
    
        if len(npi_dict[str(npi.astype(int))]['results'][0]['basic'])==0:
            print('empty basic list')
            npi_dict[str(npi.astype(int))]['results'][0]['basic']=[{keys_basi[0]:''},{keys_basi[1]:''},{keys_basi[3]:''},{keys_basi[10]:''},{keys_basi[11]:''}]
            
        if not keys_basi[0] in npi_dict[str(npi.astype(int))]['results'][0]['basic']:
                npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[0]]=''
        
        if not keys_basi[1] in npi_dict[str(npi.astype(int))]['results'][0]['basic']:
            npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[1]]=''
            
        if not keys_basi[3] in npi_dict[str(npi.astype(int))]['results'][0]['basic']:
            npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[3]]=''
    
        if not keys_basi[10] in npi_dict[str(npi.astype(int))]['results'][0]['basic']:
            npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[10]]=''
            
        if not keys_basi[11] in npi_dict[str(npi.astype(int))]['results'][0]['basic']:
            npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[11]]=''
        
        if not 'taxonomies' in npi_dict[str(npi.astype(int))]['results'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['taxonomies']=[]
    
        if len(npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'])==0:
            print('empty taxonomies list')
            npi_dict[str(npi.astype(int))]['results'][0]['taxonomies']=[{keys_taxo[0]:''},{keys_taxo[1]:''},{keys_taxo[3]:''},{keys_taxo[4]:''}]
        
        if not keys_taxo[0] in npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[0]]=''
        
        if not keys_taxo[1] in npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[1]]=''
    
        if not keys_taxo[3] in npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[3]]=''
    
        if not keys_taxo[4] in npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[4]]=''
    
        if not 'identifiers' in npi_dict[str(npi.astype(int))]['results'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['identifiers']=[]
        
        if len(npi_dict[str(npi.astype(int))]['results'][0]['identifiers'])==0:
            print('empty identifiers list')
            npi_dict[str(npi.astype(int))]['results'][0]['identifiers']=[{keys_iden[0]:''},{keys_iden[1]:''},{keys_iden[3]:''},{keys_iden[4]:''}]
            
        if not keys_iden[0] in npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[0]]=''
        
        if not keys_iden[1] in npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[1]]=''
    
        if not keys_iden[3] in npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[3]]=''
    
        if not keys_iden[4] in npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[4]]=''
    
        if not 'addresses' in npi_dict[str(npi.astype(int))]['results'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['addresses']=[]
    
        if len(npi_dict[str(npi.astype(int))]['results'][0]['addresses'])==0:
            print('empty addresses list')
            npi_dict[str(npi.astype(int))]['results'][0]['addresses']=[{keys_addr[4]:''},{keys_addr[8]:''},{keys_addr[9]:''}]
    
        if not keys_addr[4] in npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0][keys_addr[4]]=''
        
        if not keys_addr[8] in npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0][keys_addr[8]]=''
        
        if not keys_addr[9] in npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0]:
            npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0][keys_addr[9]]=''
        
    
    # creating list of dicts from the data
    doc_info_list=[]
    counter_missing_records=0
    npi_missing_info=[]
    labels=[]
    for count, npi in enumerate(adopters[:,0]):
        try:        
            doc_info={'npi':str(npi.astype(int)),
            
            keys_basi_mod[0]:npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[0]],#'credential'
            keys_basi_mod[1]:npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[1]],#'enumeration_date'
            keys_basi_mod[3]:npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[3]],#'gender'
            keys_basi_mod[10]:npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[10]],#'sole_proprietor'
            keys_basi_mod[11]:npi_dict[str(npi.astype(int))]['results'][0]['basic'][keys_basi[11]],#'status'
            
            keys_taxo_mod[0]:npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[0]],#'code'
            keys_taxo_mod[1]:npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[1]],#'desc'
            keys_taxo_mod[3]:npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[3]],#'primary'
            keys_taxo_mod[4]:npi_dict[str(npi.astype(int))]['results'][0]['taxonomies'][0][keys_taxo[4]],#'state'
            
            keys_iden_mod[0]:npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[0]],#'code'#01 forprivate and 05 for medicare
            keys_iden_mod[1]:npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[1]],#'desc'#'other'for private Medicare for gov
            keys_iden_mod[3]:npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[3]],#'issuer'#filled for private empty for gov
            keys_iden_mod[4]:npi_dict[str(npi.astype(int))]['results'][0]['identifiers'][0][keys_iden[4]],#'state'
            
            keys_addr_mod[4]:npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0][keys_addr[4]],#'city'
            keys_addr_mod[8]:npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0][keys_addr[8]],#'postalcode'
            keys_addr_mod[9]:npi_dict[str(npi.astype(int))]['results'][0]['addresses'][0][keys_addr[9]]#'state'
            }
            doc_info_list.append(doc_info.copy())
            labels.append(adopters[count,label_col])
        except Exception as e:
            counter_missing_records+=1
            npi_missing_info.append(str(npi))
            print('Empty list is alright, no sweat. Carrying on.')
            continue
    
    return doc_info_list, labels, counter_missing_records, npi_missing_info
