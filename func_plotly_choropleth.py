#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Using Plotly online services to create choropleths.
This codes uses Gaurav Misra's online account with plotly.
Please replace the username and authentication key to use the code with your code.
Learn about API authentication here: https://plot.ly/pandas/getting-started
Find your api_key here: https://plot.ly/settings/api

This function accepts a dataframe, the column to plot, and the plot title as inputs.
"""
import pandas as pd
import plotly.plotly as py
import plotly

def plotly_choropleth(df,col_to_plot,title): 
    plotly.tools.set_credentials_file(username='gauravmisra', api_key='RbsO1Ybvi7TipPdLDjCG')
    
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
                [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
    
    df['text'] = 'State: '
    data = [ dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = False,
            locations = df['state'],
            z = df[col_to_plot].astype(float),
            locationmode = 'USA-states',
            text = df['text'],
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                )
            ),
            colorbar = dict(
                title = title
            )
        ) ]
    
    layout = dict(
            title = title+' <br>',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)',
            ),
        )
    
    fig = dict(data=data, layout=layout)    
    url = py.plot(fig, filename='d3-cloropleth-map')
