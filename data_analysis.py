import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt


class data_analysis_class:
    
    def __init__(self, file_path) -> None:
            self.df = pd.read_csv(str(file_path))
            self.df_dtypes =  self.df.dtypes.to_dict()
    
    def get_dtypes(self):
         return self.df_dtypes

    def correlation_heatmap(self):
        fig = px.imshow(self.df.select_dtypes(include=np.number).corr(),text_auto=True)
        return fig
    def describe_data(self):
         st.markdown('### Data Description: Numeric')
         st.write(self.df.describe())
         st.markdown('### Null values')
         st.write(self.df.isnull().sum().to_dict())

    def get_column_names(self):
         return self.df.columns.tolist()

    def basic_plots(self, column):
         box_plot = px.box(self.df,column)
         hist_plot = px.histogram(self.df,column)
         
         return box_plot, hist_plot

    def custom_plot(self, graph_name=None, x=None, y=None ,color=None):
        
        if graph_name.lower() == 'bar':
             fig = px.bar(self.df, x, y, color)
        elif graph_name.lower() == 'box':
             fig = px.box(self.df, x)
        elif graph_name.lower() == 'histogram':
             fig = px.histogram(self.df, x)
        
        return fig

