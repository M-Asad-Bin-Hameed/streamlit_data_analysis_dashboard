import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff
from matplotlib import pyplot as plt


class data_analysis_class:

    def __init__(self, file_path) -> None:
            self.df = pd.read_csv(str(file_path))

    def get_dtypes(self):
            return self.df.dtypes.to_dict()

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
        if color == ' ':
            color = None
        if graph_name.lower() == 'bar':
            fig = px.bar(self.df, x, y, color)
        elif graph_name.lower() == 'box':
            fig = px.box(self.df, x)
        elif graph_name.lower() == 'histogram':
            fig = px.histogram(self.df, x)
        elif graph_name.lower() == 'scatter':
            fig = px.scatter(self.df, x, y, color)
        elif graph_name.lower() == 'line':
            fig = px.line(self.df, x, y, color)
        elif graph_name.lower() == 'density heatmap':
            fig = px.density_heatmap(self.df, x, y,color)
        elif graph_name.lower() == 'correlation matrix':
            fig = px.imshow(self.df.select_dtypes(include='number').corr(), text_auto=True)

        return fig

    def show_column_info(self, column_name,col1, col2):
        col_d_type = self.df[column_name].dtype
        if col_d_type == 'float64' or col_d_type == 'int64':
            self._for_numerical_dtype(column_name, col1, col2)
        if col_d_type =='object':
            col1.write('Please convert the column into a specific type')
        if col_d_type =='category':
            self._for_categorical_dtypes(column_name, col1, col2)
        if col_d_type == 'bool':
            self._for_bool_dtype(column_name, col1, col2)
        if col_d_type == 'datetime64[ns]':
            self._for_datetime_dtypes(column_name, col1, col2)
    
    def _for_datetime_dtypes(self, column_name, col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)
        col2.write('Year distribution')
        col2.plotly_chart(px.histogram(x = self.df[column_name].dt.year))
        col1.write('Monthly distribution')
        col1.plotly_chart(px.histogram(x = self.df[column_name].dt.month))

    def _for_categorical_dtypes(self,column_name,col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)
        col1.write('Unique values')
        col1.write(self.df[column_name].value_counts())
        col2.write('Histogram')
        col2.plotly_chart(px.histogram(self.df,column_name))
        col2.write('Pie chart')
        col2.plotly_chart(px.pie(self.df,column_name))

    def _for_bool_dtype(self, column_name, col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)  
        col2.write('Histogram')
        col2.plotly_chart(px.histogram(self.df,column_name))
    
    def _for_numerical_dtype(self,column_name,col1, col2):
        null_value_count = self.df[column_name].isnull().sum()
        col1.write(f'Null values = {null_value_count}')
        if null_value_count>0:
            if col1.button('Drop nulls'):
                self.df.dropna(subset=[column_name],inplace=True)

        col1.write('Describe')
        col1.write(self.df[column_name].describe())
        col2.write('Histogram')
        col2.plotly_chart(px.histogram(self.df,column_name))
        col2.write('Box plot')
        col2.plotly_chart(px.box(self.df,column_name))
        col1.write('Dist plot')
        col1.plotly_chart(ff.create_distplot([self.df[column_name]],[column_name]))

    def change_dtype(self, column_name, change_to, date_time_format = None):
        print(date_time_format)
        if change_to == 'datetime64':
            self.df[column_name] = pd.to_datetime(self.df[column_name],format=date_time_format)
        else:
            self.df[column_name] = self.df[column_name].astype(change_to)