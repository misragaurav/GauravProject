# -*- coding: utf-8 -*-
"""
These functions allow plotting columns from the dataframe and color them by class labels for easy first look at the features.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def normalize_values(myList):
    return map(lambda x: (float(x)-min(myList))/(max(myList)-min(myList)), myList )

def plot_stacked_histogram(stacked_data,labels,title='',xlabel='',normalize=False):
    """
    Plots a stacked histogram. Does not work for categorical features
    Input: 
        data -- list of stacked categories
        labels -- labels corresponding to classes
    """
    fontsize =[24,18,16,10]
    fig,ax = plt.subplots()
    ax.hist(stacked_data,normed=normalize,label=labels) # bins=10 is default, can specify otherwise here
    ax.set_title(title,fontsize=fontsize[0])
    ax.legend(fontsize=fontsize[1])
    if normalize:
        ax.set_ylabel('Percentage',fontsize=fontsize[1])
    else:
        ax.set_ylabel('Count',fontsize=fontsize[1])
    ax.set_xlabel(xlabel,fontsize=fontsize[1])
    plt.tight_layout()
    
def plot_feature_histograms(data,features,classes,labels,xlabel=None,normalize=False):
    """
    Plots a stacked histogram for each continuous feature in a dataframe. Does not work for categorical features
    Input: 
        data -- dataframe
        features -- feature columns to plot (one feature per figure)
        classes -- 2D list; outer dimension of classes, inner dimension rows in data corresponding to the class
        labels -- labels corresponding to classes
    """
    for f in features:
        stacked = [[data.loc[classes[c],f].values] for c in classes]
        plot_stacked_histogram(stacked,labels,xlabel=xlabel,title=f,normalize=normalize)