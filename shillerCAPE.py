# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
from data import getData as gd
import plotly.express as px
import pandas as pd

df=gd.shillerPE().get()
df['Real GT10']=df.GT10-df.CPI

st.title('Shiller CAPE')
chartType=st.selectbox('Select Chart Type',['Scatter','Line','Histogram'])
col1,col2 = st.columns(2)

startDate=col2.date_input('Start Date',value=df.index.min(),
                      min_value=df.index.min(),
                      max_value=df.index.max()
                      )

endDate=col2.date_input('End Date',value=df.index.max(),
                      min_value=df.index.min(),
                      max_value=df.index.max()
                      )
df=df.reindex(pd.date_range(startDate,endDate,freq='MS'))

if chartType=='Scatter':
    xAxis=col1.selectbox('Select X-Axis',df.columns,index=4)
    yAxis=col1.selectbox('Select Y-Axis',df.columns,index=9)
    colorBar=col1.checkbox('Add Color Bar by Year',value=True)
    ols=col1.checkbox('Add Linear Regression',value=True)

    if (colorBar==True) and (ols==True):
        fig=px.scatter(df,x=xAxis,y=yAxis,color=df.index.year,
                       labels={'color':'year'},
                       trendline='ols'
                       )
    elif (colorBar==True) and (ols==False):
        fig=px.scatter(df,x=xAxis,y=yAxis,
                       color=df.index.year,
                       labels={'color':'year'}
                       )
    elif (colorBar==False) and (ols==False):
        fig=px.scatter(df,x=xAxis,y=yAxis
                       )
    elif (colorBar==False) and (ols==True):
        fig=px.scatter(df,x=xAxis,y=yAxis,
                       trendline='ols'
                       )
if chartType=='Line':
    yAxis=col1.selectbox('Select Y-Axis',df.columns,index=9)
    fig=px.line(df,x=df.index,y=yAxis,
                labels={'index':'Month'}
                )    

if chartType=='Histogram':
    xAxis=col1.selectbox('Select X-Axis',df.columns,index=9)
    colorBar=col1.checkbox('Add Color Bar by Year',value=True)
    if colorBar==True:
        fig=px.histogram(df,x=xAxis,y=df.index.year,
                         histfunc='count',
                         labels={'index':'Year','color':'Year'},
                         color=df.index.year
                         )
    else:
        fig=px.histogram(df,x=xAxis,y=df.index.year,
                         histfunc='count',
                         title='Count by Year'
                         )

st.plotly_chart(fig)   

df.index=df.index.strftime('%Y-%m')
st.dataframe(df.sort_index(ascending=False))

