# -*- coding: utf-8 -*-
"""
This function plots the feature importance score of features which have a score greater than the importance_threshold.
The feature names can be set in the feature_names list to avoid using the column names as the feature names
"""

def plot_feature_importance(X, y, features, importance_threshold=0.035):

    from sklearn.ensemble import GradientBoostingClassifier
    import numpy as np
    import matplotlib as plt
    
    n_estimators=200 # number of decision trees to build

    # The features can be named here. No need to rely on the column names coming from the CMS database
    
    #    feature_names=['Accepts Medicaid',
    #                   'Primary Care', 
    #                   'Missing Insurance Info', 
    #                   'Family Medicine', 
    #                   'County Poverty', 
    #                   'Internal Medicine', 
    #                   'Diabetician'
    #                   ]

    clf2 = GradientBoostingClassifier(n_estimators=n_estimators, 
                                     min_samples_split= 16, 
                                     min_samples_leaf=4, 
                                     max_depth=3, 
                                     max_features=25, 
                                     random_state=1)
    
    clf2.fit(X, y) # feature importance is set here on the training set
    
    # Set threshold for which features to plot
    ind=np.where(clf2.feature_importances_>importance_threshold)
    
    features.columns[ind] ### feature names
    clf2.feature_importances_[ind]
    #plt.plot(clf2.feature_importances_[ind])
    
    x_values = list(clf2.feature_importances_[ind])
    y_values = features.columns[ind]
    y_values = list(y_values.values)
    
    x_y_values=np.stack((x_values,y_values),axis=1)
    x_y_values=sorted(x_y_values,key=lambda x: x[0])
    y_axis = np.arange(1, len(x_y_values)+1, 1)
    

    # The feature importance values can be set to -ve and +ve here, just for clearer visualization
     
    #x_y_values[0][0]=-1*float(x_y_values[0][0])
    #x_y_values[1][0]=-1*float(x_y_values[1][0])
    #x_y_values[2][0]=-1*float(x_y_values[2][0])
    #x_y_values[3][0]=-1*float(x_y_values[3][0])
    #x_y_values[4][0]=-1*float(x_y_values[4][0])
    #x_y_values[5][0]=-1*float(x_y_values[5][0])
    #x_y_values[6][0]=+1*float(x_y_values[6][0])
    
    plt.figure(figsize=(8,6))
    plt.barh(y_axis, np.asarray(x_y_values)[:,0].astype(float), align='center')
    plt.yticks(y_axis, np.asarray(x_y_values)[:,1].astype(str))
    
    #plt.yticks(y_axis, feature_names)
    plt.xlabel('Feature Importance Score', fontsize=18)
    
    plt.show()
    

