# -*- coding: utf-8 -*-
"""
Dropping unclean and correlated features from the dataframe. Taxonomy description (speciality of provider) can also be dropped
by setting the second argument to the function to 'yes' - this allows generating predictions without considering speciality information
"""

def drop_unclean_and_correlated_features(doc_info_frame, drop_taxonomy_description='no'):
    
    doc_info_frame.drop('i_issuer',axis=1, inplace=True)
    doc_info_frame.drop('b_credential',axis=1, inplace=True)
    
    doc_info_frame.drop('a_city',axis=1, inplace=True)
    doc_info_frame.drop('a_postal_code',axis=1, inplace=True)
    doc_info_frame.drop('b_status',axis=1, inplace=True)
    doc_info_frame.drop('t_state',axis=1, inplace=True)
    doc_info_frame.drop('i_state',axis=1, inplace=True)
    doc_info_frame.drop('t_code',axis=1, inplace=True)
    doc_info_frame.drop('i_code',axis=1, inplace=True)
    
    if (drop_taxonomy_description=='yes'):
        doc_info_frame.drop('t_desc',axis=1, inplace=True)  ############# Dropping Taxonomy desc here for experimentation purposes
    else:
        pass
    
    return doc_info_frame
